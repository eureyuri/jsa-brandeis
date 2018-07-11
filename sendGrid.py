import sendgrid
import os
from sendgrid.helpers.mail import *
import sys

def send():
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("jsabrandeis@gmail.com")
    to_email = Email("jsabrandeis@gmail.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print('======')
    print(os.environ.get('SENDGRID_API_KEY'))
    print(response.status_code)
    print(response.body)
    print(response.headers)
    print('======')
    sys.stdout.flush()


# # -*- coding: utf-8 -*-
# import sendgrid
# from dotenv import Dotenv
#
#
#
#
# config = Dotenv('./.env')
# api_key = config['API_KEY']
# tos = config['TOS'].split(',')
# from_address = config['FROM']
#
# sg = sendgrid.SendGridClient(api_key)
# message = sendgrid.Mail()
# message.smtpapi.add_to(tos)
# message.set_from('送信者名 <' + from_address + '>')
# message.set_subject('[sendgrid-python-example] フクロウのお名前はfullnameさん')
# message.set_text('familyname さんは何をしていますか？\r\n 彼はplaceにいます。')
# message.set_html('<strong> familyname さんは何をしていますか？</strong><br />彼はplaceにいます。')
# fullname_list = ['田中 太郎', '佐藤 次郎', '鈴木 三郎']
# for fullname in fullname_list:
#   message.add_substitution('fullname', fullname)
# familyname_list = ["田中", "佐藤", "鈴木"]
# for familyname in familyname_list:
#   message.add_substitution("familyname", familyname)
# place_list = ["office", "home", "office"]
# for place in place_list:
#   message.add_substitution("place", place)
# message.add_section('office', '中野')
# message.add_section('home', '目黒')
# message.add_category('category1')
# message.add_attachment('gif.gif', './gif.gif')
#
# status, msg = sg.send(message)
# print(status)
# print(msg)
