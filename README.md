# CryptoBot

You'll need to edit/create the password.json file in root directory with the following information

{"password": "password",
"sender": "sender email address",
"receiver": "receiver email address"}

You'll also have to create an email address for the bot to use

# Purpose of this bot

Sends an email out if the last 45 minutes (3 candles worth) experiences a percentage drop of 1% or more

FOR SOME REASON THE requests MODULE IS MESSED UP PLZ RUN THE FOLLOWING COMMAND IN CASE IT MESSES UP ON YOU

'python -m pip install requests'