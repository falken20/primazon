# by Richi Rod AKA @richionline / falken20

import smtplib
import ssl


# Create a secure SSL context
context = ssl.create_default_context()

# Using SMTP_SSL() ####################
port = 465  # FOr SSL
smtp_server = "smtp.gmail.com"
passsword = input("Type your password and press enter (SMTP_SSL() demo): ")

with smtplib.SMTP_SSL(host=smtp_server, port=port, context=context) as server:
    server.login("cuenta@gmail.com", passsword)
    # TODO: Send email


# Using .starttls() ####################
port = 587  # For starttls
sender_email = "my@gmail.com"
smtp_server = "smtp.gmail.com"
password = input("Type your password and press enter (.starttls() demo): ")

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Can be omitted
    server.starttls(context=context)  # Secure the connection
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    # TODO: Send email
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()
