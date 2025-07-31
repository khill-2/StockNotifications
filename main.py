import yfinance as yf
from datetime import datetime
import os
import json
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()

def load_portfolio(filename='portfolio.json'):
    with open(filename, 'r') as file:
        return json.load(file)
    
def fetch_open_and_close_prices(symbols):
    today = datetime.now().date()
    result = {}

    for sym in symbols:
        # Get the last 2 days (so today is included)
        data = yf.download(sym, period='2d', interval='1d', auto_adjust=False, progress=False)

        # Fix timezone issues by ensuring index is just the date
        data.index = pd.to_datetime(data.index).date

        if today in data.index:
            row = data.loc[today]
        else:
            raise Exception(f"No data available for {sym} on {today}. Try running the script later (after 4:30 PM ET).")

        open_price = row["Open"]
        close_price = row["Close"]
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
        breakdown.append(f"{symbol}: ${pl:.2f} (Open: ${open_price:.2f} → Close: ${close_price:.2f})")

    return total_pl, breakdown

def send_sms(message):
    sender = os.getenv('GMAIL_ADDRESS')
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    recepient = os.getenv('TO_SMS')

    msg = EmailMessage()
    msg.set_content(message)
    msg["From"] = sender
    msg["To"] = recepient
    msg["Subject"] = ""

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.send_message(msg)

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
