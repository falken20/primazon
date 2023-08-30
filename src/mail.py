# by Richi Rod AKA @richionline / falken20

import smtplib
import ssl


smtp_server = "smtp.gmail.com"
sender_email = "my@gmail.com"
receiver_email = "ricardorg20@gmail.com"

"""The message string starts with "Subject: Hi there" followed by two newlines (\n). 
This ensures Hi there shows up as the subject of the email, and the text following the 
newlines will be treated as the message body"""
message = """\
Subject: Hi

This message is sent from Python..."""


# Create a secure SSL context
context = ssl.create_default_context()

# Initiate a secure SMTP using SMTP_SSL() ####################
port = 465  # For SSL
passsword = input("Type your password and press enter (SMTP_SSL() demo): ")

with smtplib.SMTP_SSL(host=smtp_server, port=port, context=context) as server:
    server.login(sender_email, passsword)
    server.sendmail(sender_email, receiver_email, message)


# Initiate a secure SMTP using .starttls() ####################
port = 587  # For .starttls
password = input("Type your password and press enter (.starttls() demo): ")

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Can be omitted
    server.starttls(context=context)  # Secure the connection
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()
