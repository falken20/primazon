# by Richi Rod AKA @richionline / falken20

smtp_server = "smtp.gmail.com"
sender_email = "ricardorg20@gmail.com"
receiver_email = "ricardorg20@gmail.com"
filename = "mail.py"  # In same directory as script

"""The message string starts with "Subject: Hi there" followed by two newlines (\n).
This ensures Hi there shows up as the subject of the email, and the text following the
newlines will be treated as the message body"""
message = """\
Subject: Hi

This message is sent from Python..."""

# Create the plain-text and HTML version of your message
message_plaintext = """\
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
