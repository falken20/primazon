# by Richi Rod AKA @richionline / falken20

import smtplib
import ssl
# Object will contain the HTML and plain-text versions of message
from email.mime.text import MIMEText
# Combine HTML and plain.text versions in a single message
from email.mime.multipart import MIMEMultipart
# To send attachments (binaty files) is necesary to be encoded before
from email import encoders
from email.mime.base import MIMEBase
import sys

import mail_config
from logger import Log

# You can test email functionality by running a local SMTP debugging server, using the smtpd module
# that comes pre-installed with Python. Rather than sending emails to the specified address, it discards
# them and prints their content to the console. You can start a local SMTP debugging server by typing
# the following in Command Prompt:
# $ python -m smtpd -c DebuggingServer -n localhost:1025

# Option 1. Initiate a secure SMTP using SMTP_SSL() ########################################


def send_email_SMTP_SSL(smtp_server: str, sender_email: str, password: str, receiver_email: str, message: str) -> None:
    port = 465  # For SSL
    context = ssl.create_default_context()  # Create a secure SSL context

    with smtplib.SMTP_SSL(host=smtp_server, port=port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


# Option 2. Initiate a secure SMTP using .starttls() ########################################

def send_email_starttls(smtp_server: str, sender_email: str, password: str, receiver_email: str, message: str) -> None:
    port = 587  # For .starttls
    context = ssl.create_default_context()  # Create a secure SSL context

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


# Email in HTML and plain-text versions ########################################
def send_email_HTML_plaintext(smtp_server: str, sender_email: str, password: str,
                              receiver_email: str, message_plaintext: str, message_html: str):
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn versions plain-text and HTML into MIMEText objects
    part_plain = MIMEText(message_plaintext, "plain")
    part_html = MIMEText(message_html, "html")

    # Add parts to MIMEMultipart message
    # IMPORTANT: The email client will try to render the last part first
    message.attach(part_plain)
    # IMPORTANT: The email client will try to render the last part first
    message.attach(part_html)

    send_email_SMTP_SSL(smtp_server, sender_email, password,
                        receiver_email, message.as_string())


# Email with attachment file ########################################
def send_email_attachment(smtp_server: str, sender_email: str, password: str,
                          receiver_email: str, filename: str, message: str):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "An email with attachment from Python"
    message.attach(MIMEText(message, "plain"))

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

    send_email_SMTP_SSL(smtp_server, sender_email,
                        password, receiver_email, text)


if __name__ == "__main__":
    Log.info("MODULE FOR TESTING SEND EMAILS")

    password = input("Type your password and press enter: ")
    try:
        Log.info("1. Testing send email with starttls method")
        send_email_starttls(mail_config.smtp_server, mail_config.sender_email,
                            password, mail_config.receiver_email, "Testing starttls")

        Log.info("2. Testing send email with SMTP_SSL: Plain text and html")
        send_email_HTML_plaintext(mail_config.smtp_server, mail_config.sender_email,
                                  password, mail_config.receiver_email,
                                  mail_config.message_plaintext, mail_config.message_html)

        Log.info("3. Testing send email with SMTP_SSL: With attachment")
        send_email_attachment(mail_config.smtp_server, mail_config.sender_email,
                              password, mail_config.receiver_email,
                              mail_config.filename, mail_config.message_plaintext)

    except Exception as err:
        Log.error("Error testing send emails", err, sys)
