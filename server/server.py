from wsgiref.simple_server import make_server
import json
import subprocess
import calendar


PORT = 8080  # Which port the server runs on
REMINDER_CONFIG_FILE = 'reminders.json'  # Where to save the reminders


def startTwilioProcess():
    global twilioProcess
    twilioProcess = subprocess.Popen(
        [
            '/usr/bin/python',
            'twiliod/twiliod.py',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


startTwilioProcess()


def validate(reminder):
    if (
        'message' not in reminder.keys() or
        'hour'not in reminder.keys() or
        'minute'not in reminder.keys() or
        'month'not in reminder.keys() or
        'date'not in reminder.keys() or
        'year'not in reminder.keys() or
        'recurrence'not in reminder.keys()
    ):
        return False

    message = reminder['message']
    hour = reminder['hour']
    minute = reminder['minute']
    month = reminder['month']
    date = reminder['date']
    year = reminder['year']
    recurrence = reminder['recurrence']
    recurFreq = reminder['recurFreq'] if 'recurFreq' in reminder.keys(
    ) else None
    recurDays = reminder['recurDays'] if 'recurDays' in reminder.keys(
    ) else None

    def onlyBools(items):
        for item in items:
            if type(item) is not bool:
                return False
        return True

    return (
        (type(message) is str and len(message) > 0) and
        (type(hour) is int and 0 <= hour <= 23) and
        (type(minute) is int and 0 <= minute <= 59) and
        (type(month) is int and 1 <= month <= 12) and
        (type(date) is int and 1 <= date <= calendar.monthrange(year, month)[1]) and
        recurrence in ['once', 'daily', 'weekly'] and
        (
            recurrence == 'once' or
            (type(recurFreq) is int and 1 <= recurFreq)
        ) and (
            recurrence in ['once', 'daily'] or
            (type(recurDays) is list and len(recurDays) == 7 and onlyBools(recurDays))
        )
    )


def serverApp(environ, start_response):
    # Getting request body in wsgi is unbelievably obnoxious
    try:
        bodySize = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        bodySize = 0
    reminder = json.JSONDecoder().decode(
        environ['wsgi.input'].read(bodySize).decode())

    reminderId = list(reminder.keys())[0]
    reminderObj = reminder[reminderId]

    if validate(reminderObj):
        twilioProcess.kill()

        # Load the existing reminders from storage to add to them
        try:
            with open(REMINDER_CONFIG_FILE) as file:
                reminders = json.JSONDecoder().decode(file.read())
        except:
            reminders = {}

        reminders[reminderId] = reminderObj

        # Save the reminders
        with open(REMINDER_CONFIG_FILE, 'w') as file:
            file.write(json.JSONEncoder().encode(reminders))

        startTwilioProcess()

        start_response('204 No Content', [
            ('Content-Type', 'text/plain'),
            ('Access-Control-Allow-Origin', '*')])
        return [b'204 No Content']
    else:
        start_response('400 Bad Request', [
            ('Content-Type', 'text/plain'),
            ('Access-Control-Allow-Origin', '*')])
        return [b'400 Bad Request']


server = make_server('', PORT, serverApp)
server.serve_forever()
