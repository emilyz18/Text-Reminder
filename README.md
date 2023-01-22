# Text-Reminder

Project created for [NWHacks](https://www.nwhacks.io/) 2023. A program to send SMS reminders at a scheduled time.

Created by: Bruce Blore, Swapnil Dubey, Alice Low, Emily Zhang

## Setup
For now, this program only works without modification on systems where the Python binary is at `/usr/bin/python`, and this binary is Python 3. I know that Arch Linux works, but others are less certain. Install the Python Twilio API module. Run `pip install twilio`. On Arch-based systems, you can also install the `python-twilio` package from the AUR.

You also need to get a Twilio phone number. When you do this, Twilio will provide you with authentication details for your account that can be used in programs. To use these details, create the file `twiliod/credentials.json`, and fill it in as follows:

    {
        "sid": "The SID provided on the webpage",
        "token": "The token provided on the webpage",
        "from": "Your Twilio phone number"
    }

## Running

Make sure that you are in the root directory of the project, and run `python server/server.py` to start the server. This code only supports a server running locally on your machine without modification. If you host the server on another machine, you will need to modify the XMLHttpRequest code in `script.js`, and you may want to modify `server/server.py` to change the port. Also, surveillance blockers such as Brave Shields may block the communication, so should be disabled.

## Usage
The client side is at [https://emilyz18.github.io/Text-Reminder/](https://emilyz18.github.io/Text-Reminder/), or you can open it in your browser from you local drive with a `file://` URL.

You will be provided a simple GUI with a few options:
 * A text box to enter the phone number that you want to send the reminder to
 * A text box to enter the message that you want to send
 * A date and time picker to select when the message gets sent
 * A dropdown menu to select whether you want your reminder to occur only once, every few days, or every few weeks. (WARNING: As of now, there is no way to cancel a reminder within the interface. You must delete it from `reminders.json` manually.)

If you select a recurring reminder, you will also have a "recurrence frequency" option. When the recurrence is set to be based on the number of days, this controls how many days are between each reminder. 1 is every day, 2 is every other day, 3 is every third day, etc. When the recurrence is set to be based on weeks, this controls how many weeks are between each reminder instead.

Additionally, if the recurrence is set to be based on weeks, you can check or uncheck individual days. In the weeks where the reminder occurs, it occurs on every day that is checked in the interface.

## Demo
### Website: 
<img width="400" height = "300" alt="Screenshot 2023-01-22 at 11 08 40 AM" src="https://user-images.githubusercontent.com/68439730/213935077-d9c5d16c-cea8-4c17-8738-58d8d5d4fa8f.png">

### Text Reminder:
<img width="300" height = "600" src="https://user-images.githubusercontent.com/68439730/213935376-3f7dad7b-ab5f-424b-a6a3-8c537712aa9e.jpg">


