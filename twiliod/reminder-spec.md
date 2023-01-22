# Overall format

The list of reminders is a JSON file of an object. This file is to be saved in the working directory at `reminders.json`. The key is a unique, randomly generated string. The value is one particular reminder, with the following properties:

## message
The message to send to the user

## phone
The phone number to send the message to

## hour
The hour, from 0 to 23, to send the message at.

## minute
The minute, from 0 to 59, to send the message at.

## month
The month, from 1 to 12, of the date to send the message on. If it is a recurring message, this refers to when the message is first sent.

## date
The day of the month, from 1 to 31, of the date to send the message on. If it is a recurring message, this refers to when the message is first sent.

## year
The year, from 1 to 31, of the date to send the message on. If it is a recurring message, this refers to when the message is first sent.

## recurrence
One of the following values:
    * `once`: The message only gets sent once
    * `daily`: The message gets sent every few days
    * `weekly`: The message gets sent every few weeks, on certain days of the week

## recurFreq
Only needs to be defined if `recurrence` is set to `daily` or `weekly`. Is an integer >= 1 referring to how often the reminder gets sent. For example, if this is set to 2, the reminder will be sent every 2 days or every 2 weeks.

## recurDays
Only needs to be defined if `recurrence` is set to `weekly`. It is an object consisting of an array of 7 booleans, where each boolean represents whether to send a reminder on a day of the week starting from Sunday. For example, to send a reminder on Monday, Wednesday, and Friday, this should be `[false, true, false, true, false, true, false]`.

# Example reminders.json

This is an example reminders.json file, for sending reminders to a made-up phone number to wake up at 8 AM every day (starting on january 1, 2023), take out the trash on Wednesday at 7:30 PM every other week (starting on january 4), and attend MATH 302 at 11 AM on Monday, Wednesday, and Friday starting on January 11, and to start hacking on January 21 at 12 PM.

    {
        "A5KDeAE3kW49G9GwBbZhtj23gBtZ3Eym":{
            "message": "Wake up!",
            "phone": "15555555555",
            "hour": 8,
            "minute": 0,
            "month": 1,
            "date": 1,
            "year": 2023,
            "recurrence": "daily",
            "recurFreq": 1
        },
        "8HvBFf1T7YCCbOyuaKRfVAhruZm2yY5L":{
            "message": "Take out trash",
            "phone": "15555555555",
            "hour": 19,
            "minute": 30,
            "month": 1,
            "date": 4,
            "year": 2023,
            "recurrence": "weekly",
            "recurFreq": 2,
            "recurDays": [false, false, false, true, false, false, false]
        },
        "tb42O8m0ZK3Yl1M245P1ZR0ILgNQFkC8":{
            "message": "Attend MATH 302",
            "phone": "15555555555",
            "hour": 11,
            "minute": 0,
            "month": 1,
            "date": 11,
            "year": 2023,
            "recurrence": "weekly",
            "recurFreq": 1,
            "recurDays": [false, true, false, true, false, true, false]
        },
        "e33BFHs4NWRqPiZFFVYPSYLrKZeuuSCf": {
            "message": "Start hacking",
            "phone": "15555555555",
            "hour": 12,
            "minute": 0,
            "month": 1,
            "date": 21,
            "year": 2023,
            "recurrence": "once"
        }
    }