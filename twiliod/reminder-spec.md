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