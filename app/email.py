from threading import Thread
from flask_mail import Message
from app import mail
from flask import render_template
from app import app

# wrapper function to send email
# Wraps the Message class from Flask-Mail to send an email
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Blog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
    

# Asynchronous email sending #

# The send_async_email function is used to send emails asynchronously.
# This function is used to send emails in a separate thread, so the main thread can continue
# executing while the email is being sent.
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# The send_email function is a wrapper function that wraps the send_async_email function.
# This function is used to send emails asynchronously.
# The function creates a Message object using the Message class from Flask-Mail.
# The function then creates a new thread using the Thread class from the threading module.
# The thread calls the send_async_email function with the app and msg arguments.
# The thread is then started using the start method.
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()