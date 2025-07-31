import os
import smtplib
import json
import pandas as pd
import yfinance as yf
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv("GMAIL_ADDRESS")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
TO = os.getenv("TO_SMS")

def load_portfolio(filename="portfolio.json"):
    with open(filename, "r") as file:
        return json.load(file)

def fetch_open_close(symbols):
    today = datetime.now().date()
    result = {}

    for sym in symbols:
        data = yf.download(sym, period="2d", interval="1d", progress=False, auto_adjust=False)
        data.index = pd.to_datetime(data.index).date

        if today in data.index:
            row = data.loc[today]
        else:
            raise Exception(f"No data yet for {sym} on {today}. Try again after 4:30 PM ET.")

        # result[sym] = (row["Open"], row["Close"])
        open_price = float(row["Open"])
        close_price = float(row["Close"])
        result[sym] = (open_price, close_price)


    return result

def calculate_pl(portfolio, prices):
    total = 0.0
    breakdown = []
    for stock in portfolio:
        symbol = stock["symbol"]
        shares = stock["shares"]
        open_price, close_price = prices[symbol]
        pl = (close_price - open_price) * shares
        total += pl
        breakdown.append(f"{symbol}: ${pl:.2f} (Open: ${open_price:.2f} → Close: ${close_price:.2f})")
    return total, breakdown

def send_sms(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg["From"] = SENDER
    msg["To"] = TO
    msg["Subject"] = "Stock Report"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(msg)

def main():
    portfolio = load_portfolio()
    symbols = [stock["symbol"] for stock in portfolio]
    prices = fetch_open_close(symbols)
    total_pl, breakdown = calculate_pl(portfolio, prices)

    emoji = "📈" if total_pl >= 0 else "📉"
    today = datetime.now().strftime("%Y-%m-%d")
    message = f"Stock Report for {today}\n{emoji} Net P/L: ${total_pl:.2f}\n\n" + "\n".join(breakdown)

    print("Sending this message:\n" + message)
    send_sms(message)
    print("✅ SMS sent!")

if __name__ == "__main__":
    main()
