import json
from twilio.rest import Client as TwilioClient
import sys

with open('twiliod/credentials.json') as file:
    credentials = json.JSONDecoder().decode(file.read())

twilioClient = TwilioClient(credentials['sid'], credentials['token'])

message = twilioClient.messages.create(
    body="Hello world!",
    from_=credentials['from'],
    to=sys.argv[1]
)

print(message.sid)
