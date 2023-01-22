import json
import os
from twilio.rest import Client as TwilioClient
from datetime import datetime

# Paths where things are stored
CREDENTIAL_FILE = 'twiliod/credentials.json'    # Twilio credentials
REMINDER_CONFIG_FILE = 'reminders.json'         # Reminders to send
REMINDERS_SENT_FILE = 'remindersSent.json'      # Log the reminders that get sent

# Load the Twilio credentials
with open(CREDENTIAL_FILE) as file:
    twilioCredentials = json.JSONDecoder().decode(file.read())
    twilioClient = TwilioClient(
        twilioCredentials['sid'], twilioCredentials['token'])


def sendSMS(target, message):
    # Send a message
    message = twilioClient.messages.create(
        body=message,
        from_=twilioCredentials['from'],
        to=target
    )
    # print(message.sid)


with open(REMINDERS_CONFIG_FILE) as file:
    reminders = json.JSONDecoder().decode(file.read())
    remindersSent = json.JSONDecoder().decode(REMINDERS_SENT_FILE)

schedule = {}


def getFirstDate(reminder):
    # Get the unix timestamp of the first date that the reminder occurs
    return datetime(
        reminder['year'],
        reminder['month'],
        reminer['date'],
        reminder['hour'],
        reminder['minute'],
        0
    ).timestamp()


def getNextDate(reminder, lastDate):
    # Given a reminder and the last time it was sent, determine the next time it should be sent
    pass


def deleteReminder(reminderID):
    del reminders


remindersToDelete = []
for reminderID in reminders.keys():
    reminder = reminders[reminderID]

    # If the reminder does not recur:
    if reminder['recurrence'] == 'once':
        # If it should have been sent already, it should be sent then deleted. (We don't bother logging non-recurring reminders in reminersSent because they should be deleted immediately.)
        if getFirstDate(reminder) < datetime().now().timestamp():
            sendSMS(reminder['phone'], reminder['message'])
            remindersToDelete.append(reminderID)
        # If it should be sent in the future, schedule it to be sent in the future
        else:
            schedule[getFirstDate(reminder)] = reminderID

    # If the reminder does recur:
    else:
        # For every time that the reminder should have occurred in the past, send it if it has to be sent
        # Start with the first date that the reminder should have been sent
        curTime = getFirstDate(reminder)
        while (curTime < datetime().now().timestamp()):
            # If the reminder has no record in remindersSent, create one
            if reminderID not in remindersSent.keys():
                remindersSent[reminderID] = []

            # If this occurrence has not been sent, send it and log that we sent it
            if curTime not in remindersSent[reminderID]:
                sendSMS(reminder['phone'], reminder['message'])
                remindersSent[reminderID].append(curTime)

            # Repeat for the next occurrence
            curTime = getNextDate(reminder, curTime)

        # The loop terminates as soon as curTime is in the future. Schedule the future reminder
        schedule[curTime] = reminderID
