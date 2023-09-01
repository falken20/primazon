# by Richi Rod AKA @richionline / falken20

import smtplib
import ssl
from email.mime.text import MIMEText  # Object will contain the HTML and plain-text versions of message
from email.mime.multipart import MIMEMultipart  # Combine HTML and plain.text versions in a single message
from email import encoders  # To send attachments (binaty files) is necesary to be encoded before
from email.mime.base import MIMEBase

# You can test email functionality by running a local SMTP debugging server, using the smtpd module
# that comes pre-installed with Python. Rather than sending emails to the specified address, it discards
# them and prints their content to the console. You can start a local SMTP debugging server by typing
# the following in Command Prompt:
# $ python -m smtpd -c DebuggingServer -n localhost:1025

smtp_server = "smtp.gmail.com"
sender_email = "my@gmail.com"
receiver_email = "ricardorg20@gmail.com"
password = input("Type your password and press enter (SMTP_SSL() demo): ")

"""The message string starts with "Subject: Hi there" followed by two newlines (\n).
This ensures Hi there shows up as the subject of the email, and the text following the
newlines will be treated as the message body"""
message = """\
Subject: Hi

This message is sent from Python..."""


# Option 1. Initiate a secure SMTP using SMTP_SSL() ####################
port = 465  # For SSL

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(host=smtp_server, port=port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)


# Option 2. Initiate a secure SMTP using .starttls() ####################
port = 587  # For .starttls

# Create a secure SSL context
context = ssl.create_default_context()

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


# Email in HTML and plain-text versions ####################
message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
message_text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
message_html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a>
       has many great tutorials.
    </p>
  </body>
</html>
"""

# Turn versions plain-text and HTML into MIMEText objects
part_plain = MIMEText(message_text, "plain")
part_html = MIMEText(message_html, "html")

# Add parts to MIMEMultipart message
# IMPORTANT: The email client will try to render the last part first
message.attach(part_plain)
message.attach(part_html)  # IMPORTANT: The email client will try to render the last part first

# Create secure connection with server and send email
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )


# Email with attachment file ####################
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "An email with attachment from Python"

# Add body to email
body = "This is an email with attachment sent from Python"
message.attach(MIMEText(body, "plain"))

filename = "document.pdf"  # In same directory as script
# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
