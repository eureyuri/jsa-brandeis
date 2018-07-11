import sendgrid
import os
from sendgrid.helpers.mail import *
import sys


def send(subject, message):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("jsabrandeis@gmail.com")
    to_email = Email("jsabrandeis@gmail.com")
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    debug(response)


def debug(response):
    print('======')
    print(response.status_code)
    print(response.body)
    print(response.headers)
    print('======')
    sys.stdout.flush()