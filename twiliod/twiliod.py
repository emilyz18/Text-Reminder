import json
import os
from twilio.rest import Client as TwilioClient

with open('twiliod/credentials.json') as file:
    twilioCredentials = json.JSONDecoder().decode(file.read())
    twilioClient = TwilioClient(
        twilioCredentials['sid'], twilioCredentials['token'])


def sendReminder(target, message):
    message = twilioClient.messages.create(
        body=message,
        from_=twilioCredentials['from'],
        to=target
    )
    # print(message.sid)
