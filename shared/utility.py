import re, threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework.exceptions import ValidationError

email_regex = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
phone_regex = re.compile(r"^\+998\d{9}$")
username_regex = re.compile(r"^[a-zA-Z0-9_]{3,30}$")

def check_user_input(user_input):
    if re.fullmatch(email_regex, user_input):
        user_input = "via_email"
    elif re.fullmatch(phone_regex, user_input):
        user_input = "phone_regex"
    else:
        data = {
            'success': False,
            'message': 'Email or phone number invalid'
        }
        raise ValidationError(data)
    return user_input

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def check_user_type(user_input):
    if re.fullmatch(email_regex, user_input):
        user_input = "email"
    elif re.fullmatch(phone_regex, user_input):
        user_input = "phone"
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"
    else:
        data = {
            'success': False,
            'message': "email or phone incorrect"
        }
        raise ValidationError(data)
    return user_input

class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject = data['subject'],
            body = data['body'],
            to = [data['to_email']]
        )
        if data.get('content_type') == 'html':
            email.content_subtype = 'html'
        EmailThread(email).start()

def send_email(email, code):
    html_content = render_to_string(
        'email/activate/activation_code.html',
        {"code": code}
    )
    Email.send_email(
        {
            "subject": "Ro'yxatdan o'tish",
            "to_email": email,
            "body": html_content
        }
    )
