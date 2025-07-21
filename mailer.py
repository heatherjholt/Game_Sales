import smtplib
from email.message import EmailMessage
from request_deals import top_deals


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

send_outlook_email("New Deals!", "testing", receiver_email)