import urllib.parse
from wsgiref.simple_server import make_server
import json
import subprocess


PORT = 8080  # Which port the server runs on
REMINDER_CONFIG_FILE = 'reminders.json'  # Where to save the reminders

try:
    with open(REMINDER_CONFIG_FILE) as file:
        reminders = json.JSONDecoder().decode(file.read())
except:
    reminders = {}


def startTwilioProcess():
    with open(REMINDER_CONFIG_FILE, 'w') as file:
        file.write(json.JSONEncoder().encode(reminders))

    global twilioProcess
    twilioProcess = subprocess.Popen(
        [
            '/usr/bin/python3',
            'twiliod/twiliod.py',
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def killTwilioProcess():
    twilioProcess.kill()


startTwilioProcess()


def serverApp(environ, start_response):
    # Getting request body in wsgi is unbelievably obnoxious
    try:
        bodySize = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        bodySize = 0
    body = environ['wsgi.input'].read(bodySize).decode()

    print(body)
    form = urllib.parse.parse_qs(body)
    print(form)
    start_response('204 No Content', [
        ('Content-Type', 'text/plain')])
    return [b'204 No Content']


server = make_server('', PORT, serverApp)
server.serve_forever()
