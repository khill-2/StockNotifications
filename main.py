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
    
def fetch_open_and_close_prices(symbols):
    tickers = yf.download(" ".join(symbols), period='1d', interval='1m', group_by='ticker', progress=False)
    result = {}
    for sym in symbols:
        data = tickers[sym] if len(symbols) > 1 else tickers
        open+_price = data['Open'].iloc[0]
        close_price = data['Close'].iloc[-1]
        result[sym] = (open_price, close_price)
    return result

def calculate_daily_pl(portfolio, price_data):
    total_pl = 0.0
    breakdown = []

    for stock in portfolio:
        symbol = stock["symbol"]
        shares = stock["shares"]
        open_price, close_price = price_data[symbol]
        pl = (close_price - open_price) * shares
        total_pl += pl
        breakdown.append(f"{symbol}: ${pl:.2f} ({shares} shares, Open ${open_price:.2f} → Close ${close_price:.2f})")

    return total_pl, breakdown

