# by Richi Rod AKA @richionline / falken20

from mailjet_rest import Client
import os
import sys

from src.logger import Log


api_key = os.environ['MAILJET_APIKEY_PUBLIC']
api_secret = os.environ['MAILJET_APIKEY_PRIVATE']
api_version = 'v3.1'
receiver_email = os.environ['RECEIVER_EMAIL']
text_part_default = "Several Amazon products are lowered their price."

data = {
    'Messages': [{
        "From": {
            "Email": "primazon@mailjet.com",
            "Name": "Primazon Alert"
        },
        "To": [{
            "Email": receiver_email,
            "Name": ""
        }],
        "Subject": "Primazon Alert!!!!",
        "TextPart": text_part_default,
        "HTMLPart": ""
    }]
}


def send_email(receiver_email: str = receiver_email, text_part: str = "") -> bool:
    try:
        Log.info("Preparing to send email...")
        mailjet = Client(auth=(api_key, api_secret), version=api_version)

        data["Messages"][0]["To"][0]["Email"] = receiver_email
        data["Messages"][0]["TextPart"] = text_part

        result = mailjet.send.create(data=data)

        Log.info(f"Email sent with status code: {result.status_code}")
        Log.debug(f"JSON result email sent:\n {result.json()}")

        return True

    except Exception as err:
        print(err)
        Log.error("Error sneding email by mailjet API", err, sys)
        return False

