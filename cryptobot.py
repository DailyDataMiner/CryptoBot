import requests
import configparser
import json
import logging
import os
import sys
import smtplib, ssl
from socket import gaierror
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

## Gets email information from password.json file
def get_details():

    f = open('password.json',)

    data = json.load(f)

    f.close()

    return data

## Creates and send email
def email(percent):

    data = get_details()

    email = data['sender']
    password = data['password']
    send_to_email = data['receiver']
    subject = 'CryptoBot has detected a drop in Bitcoin' # The subject line
    message = """\
    BITCOIN HAS DROPPED BY """ + str(percent) + """% AND YOU NEED TO START BUYING!!!"""

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()

## Simple function to determine if a three_candle_drop (probably) happened ¯\_(ツ)_/¯
def three_candle_drop(data):

    ## Modify as needed
    percent = 1.0

    opening = float(data[2]['open'])
    closing = float(data[0]['close'])

    logging.info('3rd candle''s opening: ' + str(opening))
    logging.info('1st candle''s closing: ' + str(closing))

    decrease = opening - closing

    percent_diff = (decrease / opening) * 100

    logging.info('Percentage difference: ' + str(percent_diff))

    if (percent_diff > percent):
        return percent_diff
    else:
        return False

## Analyzing the data, supposed to be more modular ¯\_(ツ)_/¯
def analyze_data(data):

    return three_candle_drop(data)
    
## Obtains candle data from hitbtc API
def get_candle_data(config, session):
    logging.info('Obtaining last 3 candles for btcusd')

    ## URL request configuration
    params = {'period': 'm15','sort': 'DESC'}
    URL = 'https://api.hitbtc.com/api/2/public/candles/btcusd'

    ## Get Request for data
    response = session.get(URL, params=params)

    ## Should be a 200
    if response.status_code == 200:
        return response.json()
    else:
        return None

## What is run upon execution
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    session = requests.Session()

    while True:
        ## Will run every 15 minutes. Starting at the beginning or the end of the candle has it's advantages and disadvantages
        data = get_candle_data(config=config, session=session)
        if data != None:

            percent = analyze_data(data)

            if percent != False:
                logging.info('Sending email!')
                email(percent)
            else:
                logging.info('Carry on...')
        else :
            logging.error('Error when obtaining the data from hitbtc API')
        time.sleep(900)
