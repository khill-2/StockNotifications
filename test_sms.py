import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv("GMAIL_ADDRESS")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
TO = os.getenv("TO_SMS")

def send_test_message():
    msg = EmailMessage()
    msg.set_content("🚨 Test SMS: This is a test from Python via email-to-text.")
    msg["From"] = SENDER
    msg["To"] = TO
    msg["Subject"] = "Stock Alert"  # Often ignored by SMS gateways

    print("Connecting to Gmail...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(msg)
    print("Message sent!")

if __name__ == "__main__":
    send_test_message()
