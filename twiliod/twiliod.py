import json
import os
from twilio.rest import Client as TwilioClient
from datetime import datetime
import calendar
import time
import sys

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

schedule = []


def getFirstDate(reminder):
    # Get the unix timestamp of the first date that the reminder occurs
    return datetime(
        reminder['year'],
        reminder['month'],
        reminder['date'],
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


for reminderID in reminders.keys():
    reminder = reminders[reminderID]

    # If the reminder does not recur, schedule it. If it had been sent, it would have been deleted. Anything scheduled in the past will be sent immediately.
    if reminder['recurrence'] == 'once' or (reminder['recurrence'] == 'weekly' and True not in reminder['recurDays']):
        schedule.append({
            'id': reminderID,
            'time': getFirstDate(reminder)
        })

    # If the reminder does recur:
    else:
        # For every time that the reminder should have occurred in the past:
        curTime = getFirstDate(reminder)
        while (curTime < datetime().now().timestamp()):
            # If this occurrence has not been sent, stop here.
            if (reminderID not in remindersSent) or (curTime > remindersSent[reminderID]):
                break

            # Check the next occurrence
            curTime = getNextDate(reminder, curTime)

        # When the loop terminates, it means that either:
        #   We passed the last occurrence that was actually sent, and need to send the rest
        #   We are now in the future, and need to schedule the future reminder
        schedule.append({
            'id': reminderID,
            'time': curTime
        })

save()


def printSchedule(reminderIDs, schedule):
    # Print the schedule to the console
    for entry in schedule:
        reminder = reminders[entry["id"]]
        dt = datetime.fromtimestamp(entry["time"])
        weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                   'Saturday'][fixWeekday(calendar.weekday(dt.year, dt.month, dt.day))]
        print(
            f'To {reminder["phone"]} at {weekday}, {dt}: {reminder["message"]}')


# Go through the scheduled reminders, sorted in order of when they should happen
schedule.sort(lambda entry: entry['time'])
while len(schedule) > 0:
    printSchedule(reminderIDs, schedule)
    if len(sys.argv) >= 2 and sys.argv[1] == 'PAUSE':
        input('Paused')
    else:
        print()

    nextEntry, schedule = schedule[0], schedule[1:]
    time.sleep(max(0, nextEntry['time'] - datetime.now().timestamp()))
    reminder = reminders[nextEntry['id']]

    # If the reminder does not recur, delete it:
    if reminder['recurrence'] == 'once' or (reminder['recurrence'] == 'weekly' and True not in reminder['recurDays']):
        sendSMS(reminder['phone'], reminder['message'])
        del reminder[reminderID]
        save()

    # If the reminder does recur, log it and schedule the next occurrence:
    else:
        sendSMS(reminder['phone'], reminder['message'])
        remindersSent[reminderID] = nextEntry['time']
        save()

        schedule.append({
            'id': reminderID,
            'time': getNextDate(reminder, nextEntry['time'])
        })
        schedule.sort()  # Sort again in case next recurrence comes before another scheduled reminder
