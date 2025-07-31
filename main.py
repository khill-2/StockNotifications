import yfinance as yf
from twilio.rest import Client
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
TO_PHONE_NUMBER = os.getenv('TO_PHONE_NUMBER')

def load_portfolio(filename='portfolio.json'):
    with open(filename, 'r') as file:
        return json.load(file)
    

