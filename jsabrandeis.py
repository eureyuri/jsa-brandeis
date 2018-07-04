import os
from flask import Flask, render_template, request
import httplib2
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
from json import *


app = Flask(__name__)


SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = os.environ.get("CLIENT_SECRET_FILE")
APPLICATION_NAME = 'JSA Brandeis'


@app.errorhandler(404)
def page_not_found(e):
    # TODO
    print(e)
    return "404"


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def contact():
    to = "eurey@brandeis.edu"
    sender = "eurey@brandeis.edu"
    subject = "JSA - Contact"
    msg_html = "Name: " + str(request.form["name"]) + "\nEmail: " + str(request.form["email"]) \
                   + "\nComment: " + (request.form["comment"])
    msg_plain = "Name: " + str(request.form["name"]) + "\nEmail: " + str(request.form["email"]) \
                   + "\nComment: " + (request.form["comment"])
    send_message(sender, to, subject, msg_html, msg_plain)

    return render_template("index.html")


@app.route('/news', methods=["GET"])
def news():
    return render_template("news.html")


@app.route('/pastEvents', methods=["GET"])
def pastEvents():
    return render_template("past_events.html")


@app.route('/involve', methods=["GET"])
def involve():
    return render_template("involve.html")


@app.route('/involve', methods=['POST'])
def volunteer():
    to = "eurey@brandeis.edu"
    sender = "eurey@brandeis.edu"
    subject = "JSA - Volunteer"
    msg_html = "Name: " + str(request.form["name"]) + "\nEmail: " + str(request.form["email"]) \
              + "\nComment: " + (request.form["comment"])
    msg_plain = "Name: " + str(request.form["name"]) + "\nEmail: " + str(request.form["email"]) \
               + "\nComment: " + (request.form["comment"])
    send_message(sender, to, subject, msg_html, msg_plain)

    return render_template("involve.html")


@app.route('/outsideBrandeis', methods=["GET"])
def outside_brandeis():
    return render_template("outsidebrandeis.html")


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        # flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow = client.OAuth2WebServerFlow(client_id=os.environ.get("CLIENT_ID"), client_secret=os.environ.get("CLIENT_SECRET"), scope=SCOPES, redirect_uri=app.root_path)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def send_message(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    message1 = create_message_html(sender, to, subject, msgHtml, msgPlain)
    result = send_message_internal(service, "me", message1)
    return result


def send_message_internal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"


def create_message_html(sender, to, subject, msgHtml, msgPlain):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msgPlain, 'plain'))
    msg.attach(MIMEText(msgHtml, 'html'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body


if __name__ == '__main__':
    app.run()