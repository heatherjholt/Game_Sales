import smtplib
from email.message import EmailMessage
import requests

API_URL = "https://www.cheapshark.com/api/1.0"
DEALS_URL = f"{API_URL}/deals"

def top_deals(n):
    params = {
        "pageSize": n,
        "sortBy":   "dealRating",
        "desc":     1
    }
    resp = requests.get(DEALS_URL, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

deals = top_deals(10)

def format_email(deals):
    lines = ["Here are today’s top CheapSnake deals:\n"]
    for d in deals:
        title   = d["title"]
        sale    = d["salePrice"]
        normal  = d["normalPrice"]
        savings = float(d["savings"])
        store   = d["storeID"]
        lines.append(f"- {title} @ Store {store}: ${sale} → was ${normal} ({savings:.0f}% off)")
    return "\n".join(lines)

port = 587
smtp_server = "smtp.gmail.com"


EMAIL_ADDRESS = "CheapSnake2025@gmail.com"
EMAIL_PASSWORD = "nisd dmht nkqm rmuw"

receiver_email = input("Enter Email: ")

def send_outlook_email(subject, body, to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg.set_content(body)

    # Connect to Outlook SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()  # Upgrade the connection to secure
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("Email sent via Gmail!") 

send_outlook_email("New Deals!", format_email(deals), receiver_email)