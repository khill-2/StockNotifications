import yfinance as yf
from twilio.rest import Client
from datetime import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
TO_PHONE_NUMBER = os.getenv('TWILIO_TO')

def load_portfolio(filename='portfolio.json'):
    with open(filename, 'r') as file:
        return json.load(file)
    
def fetch_open_and_close_prices(symbols):
    tickers = yf.download(" ".join(symbols), period='1d', interval='1m', group_by='ticker', progress=False)
    result = {}
    for sym in symbols:
        data = tickers[sym] if len(symbols) > 1 else tickers
        open_price = data['Open'].iloc[0]
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

def send_sms(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )

def main():
    portfolio = load_portfolio()
    symbols = []
    for stock in portfolio:
        symbols.append(stock["symbol"])
    price_data = fetch_open_and_close_prices(symbols)
    total_pl, breakdown = calculate_daily_pl(portfolio, price_data)

    today = datetime.now().strftime("%Y-%m-%d")
    emoji = "📈" if total_pl >= 0 else "📉"
    message = f"Stock Daily Report – {today}\n{emoji} Net P/L: ${total_pl:.2f}\n\n" + "\n".join(breakdown)

    send_sms(message)
    print("SMS sent successfully!", message)

if __name__ == "__main__":
    main()
