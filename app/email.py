from flask_mail import Message
from app import mail

# wrapper function to send email
# Wraps the Message class from Flask-Mail to send an email
def send_password_reset_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)