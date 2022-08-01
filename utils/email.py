import requests as requests
from dotenv import load_dotenv
import os

load_dotenv()


def sendEmail(to, subject, emailContent):
    return requests.post(
        os.environ.get("MAILGUN_DEFULT_SEND_API"),
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={"from": os.environ.get("MAILGUN_DEFAULT_SENDER"),
              "to": [to],
              "subject": subject,
              "text": emailContent,
              "html": emailContent
              })
