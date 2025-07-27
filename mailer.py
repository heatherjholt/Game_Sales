import smtplib
from email.message import EmailMessage
from request_deals import top_deals
from database import get_emails, insert_email, create_email_table
import time

# Pull top 10 deals from the request deals
deals = top_deals(10)
#format the email as one long string
def format_email(deals):
    lines = "Here are today’s top CheapSnake deals:\n"
    for d in deals:
        title   = d["title"]
        sale    = d["salePrice"]
        normal  = d["normalPrice"]
        savings = float(d["savings"])
        store   = d["dealID"]
        lines += (f"- {title} @ Store https://www.cheapshark.com/redirect?dealID={store}: ${sale} --> was ${normal} ({savings:.0f}% off)\n")
    return lines

port = 587
smtp_server = "smtp.gmail.com"


EMAIL_ADDRESS = "CheapSnake2025@gmail.com"
EMAIL_PASSWORD = "nisd dmht nkqm rmuw"

def send_outlook_email(subject, body, to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg.set_content(body)
    
    # Connect to Outlook SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo() # Establish ehlo connection
        smtp.starttls()  # Upgrade the connection to tls connection
        smtp.ehlo() # Reinstate ehlo connection
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) # Login to email using app password
        smtp.send_message(msg) # Email out the message
        print("Email sent via Gmail!") # Confirm email was sent

def emailing():
    # receiver_email = input("Enter Email: ") - was used for testing
    # for demo purposes, not using time for emailing
    mailer_list = get_emails()
    for x in mailer_list:
        send_outlook_email("New Deals!", format_email(deals), x)
# Infinite loop to wait 24 hours before sending deals
#while True:
 #   time.sleep(24*60*60) #24 hours x 60 minx 60 seconds
 #   emailing()