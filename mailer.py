import smtplib
from email.message import EmailMessage
from request_deals import top_deals
#from database import get_emails, insert_email, create_email_table
# import time


deals = top_deals(10)

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

receiver_email = input("Enter Email: ")
# For test purposes not including adding to database
#insert_email(receiver_email) 


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

# for demo purposes, not using loop to send emails
#time.sleep(86400)
#mailer_list = get_emails()
#for x in mailer_list:
send_outlook_email("New Deals!", format_email(deals), receiver_email)

