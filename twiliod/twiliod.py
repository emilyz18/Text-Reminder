import json
import os
from twilio.rest import Client as TwilioClient
from datetime import datetime
import calendar
calendar.setfirstweekday(calenar.SUNDAY)

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


def fixWeekday(weekday):
    # The calendar library uses 0 for Monday and 6 for Sunday. We use 0 for Sunday and 6 for Saturday. This fixes that
    return (weekday + 1) % 7


def addDays(timestamp, days):
    # Add the given number of days to a timestamp
    dt = datetime.fromtimestamp(timestamp)
    nextDayOfMonth = dt.day + days
    nextMonth = dt.month
    nextYear = dt.year
    while nextDayOfMonth > calendar.monthrange(nextYear, nextMonth):
        nextDayOfMonth -= calendar.monthrange(nextYear, nextMonth)
        nextMonth += 1
        if nextMonth > 12:
            nextMonth -= 12
            nextYear += 1
    return datetime(nextYear, nextMonth, nextDayOfMonth,
                    dt.hour, dt.minute, dt.second).timestamp()


def getNextDate(reminder, lastDate):
    # Given a reminder and the last time it occured, return the next time it occurs
    if reminder['recurrence'] == 'daily':
        return addDays(lastDate, reminder['recurFreq'])

    elif reminder['recurrence'] == 'weekly':
        dt = datetime.fromtimestamp(lastDate)
        dayOfWeek = fixWeekday(calendar.weekday(dt.year, dt.month, dt.day))

        # If there are more reminders this week, return the time for the next one
        if True in reminder['recurDays'][dayOfWeek + 1:]:
            # Adding 1 because the zeroth element of the array is actually tomorrow!
            return addDays(lastDate, reminder['recurDays'][dayOfWeek + 1:].index(True) + 1)

        # If there are not more reminders this week, the next one is in the following number of days:
        #   The number of days until Sunday (7 if today is Sunday) +
        #   The number of days from Sunday to the first day of the week with the reminder (can be zero) +
        #   7 * (recurFreq - 1) (skip 0 weeks if it should be every week, 1 week if it should be every 2 weeks, etc)
        else:
            daysUntilSunday = 7 - dayOfWeek
            daysFromSunday = reminder['recurDays'].index(True)
            return addDays(lastDate, daysUntilSunday + daysFromSunday + 7 * (reminder['recurFreq'] - 1))


def save():
    # Save the state of reminders and remindersSent
    with open(REMINDER_CONFIG_FILE, 'w') as file:
        file.write(json.JSONEncoder().encode(reminders))
    with open(REMINDERS_SENT_FILE, 'w') as file:
        file.write(json.JSONEncoder().encode(remindersSent))


remindersToDelete = []
for reminderID in reminders.keys():
    reminder = reminders[reminderID]

    # If the reminder does not recur:
    if reminder['recurrence'] == 'once' or (reminder['recurrence'] == 'weekly' and True not in reminder['recurDays']):
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

# Delete all reminders that we flagged for deletion
for reminderID in remindersToDelete:
    del reminders[reminderID]
save()

# Sleep until the first scheduled reminder
