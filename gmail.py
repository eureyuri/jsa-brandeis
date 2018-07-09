import os
import httplib2
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.text import MIMEText
from email.utils import formatdate
import traceback
import apiclient
import argparse
import json
from dotenv import load_dotenv
from pathlib import Path


SCOPES = 'https://www.googleapis.com/auth/gmail.send'
# CLIENT_SECRET_FILE = 'client_secret.json'
CLIENT_SECRET_FILE = 'client_secret_empty.json'
# CLIENT_SECRET_FILE = os.environ.get("CLIENT_SECRET_FILE")
APPLICATION_NAME = 'JSA Brandeis'
MAIL_FROM = "eureynoguchi@gmail.com"
MAIL_TO = "eurey@brandeis.edu"


def build_client_secret():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    with open(CLIENT_SECRET_FILE, 'r+') as f:
        data = json.load(f)
        # data['web']['client_id'] = os.environ.get("CLIENT_ID")
        # data['web']['client_secret'] = os.environ.get("CLIENT_SECRET")
        data['web']['client_id'] = os.getenv("CLIENT_ID")
        data['web']['client_secret'] = os.getenv("CLIENT_SECRET")
        # Reset file position to 0
        f.seek(0)
        json.dump(data, f)


def delete_client_secret():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    with open(CLIENT_SECRET_FILE, 'r+') as f:
        data = json.load(f)
        # data['web']['client_id'] = os.environ.get("CLIENT_ID")
        # data['web']['client_secret'] = os.environ.get("CLIENT_SECRET")
        data['web']['client_id'] = ''
        data['web']['client_secret'] = ''
        # Reset file position to 0
        f.seek(0)
        json.dump(data, f)
        # Remove remaining part because unwanted stuff gets concatenated for some reason
        # Debug later when we have time
        f.truncate()


def get_credentials():
    build_client_secret()

    # Get absolute path of current directory
    script_dir = os.path.abspath(os.path.dirname(__file__))
    credential_dir = os.path.join(script_dir, ".credentials")

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[oauth2client.tools.argparser]).parse_args()
        credentials = oauth2client.tools.run_flow(flow, store, flags)
        print("Storing credentials to " + credential_path)

    return credentials


def create_message(subject, message):
    message = MIMEText(message)
    message["from"] = MAIL_FROM
    message["to"] = MAIL_TO
    message["subject"] = subject
    message["Date"] = formatdate(localtime=True)

    byte_msg = message.as_string().encode(encoding="UTF-8")
    byte_msg_b64encoded = base64.urlsafe_b64encode(byte_msg)
    str_msg_b64encoded = byte_msg_b64encoded.decode(encoding="UTF-8")

    return {"raw": str_msg_b64encoded}


def send_message(subject, message):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build("gmail", "v1", http=http)

    delete_client_secret()

    try:
        result = service.users().messages().send(
            userId=MAIL_FROM,
            body=create_message(subject, message)
        ).execute()

        print("Message Id: {}".format(result["id"]))

    except apiclient.errors.HttpError:
        print("------start trace------")
        traceback.print_exc()
        print("------end trace------")