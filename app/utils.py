
import secrets
import string
import os
import json
from django.conf import settings

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(subject, recipient_list, template_path, context):
    message = render_to_string(template_path, context)
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=f'KeySavvy <{settings.EMAIL_HOST_USER}>',
        to=recipient_list,
    )
    email.content_subtype = 'html'
    email.send()
    print("email send")


def load_json_file(file_path):
    absolute_path = os.path.join(settings.BASE_DIR, file_path)
    with open(absolute_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def generate_secure_password(length=12):
    # Define the character pool for the password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Ensure the password contains at least one of each character type
    password = (
        secrets.choice(string.ascii_lowercase) +
        secrets.choice(string.ascii_uppercase) +
        secrets.choice(string.digits) +
        secrets.choice(string.punctuation)
    )
    # Fill the rest of the password length with random characters
    password += ''.join(secrets.choice(characters) for _ in range(length - 4))
    # Shuffle the password to ensure randomness
    password = ''.join(secrets.choice(password) for _ in range(len(password)))
    return password