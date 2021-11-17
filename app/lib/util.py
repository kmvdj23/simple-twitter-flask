from datetime import datetime
from app.config import db, app
from flask import url_for
from lib.email import EmailServer

class ResourceMixin(object):
    create_date = db.Column(db.DateTime, default=datetime.now())
    update_date = db.Column(db.DateTime, default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def format_date_to_str(cls, date, format):
        default_datetime = datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

        if date == default_datetime:
            return ''

        return datetime.strftime(date, format)

    @classmethod
    def short_date(cls, date):
        return cls.format_date_to_str(date, '%d/%m/%Y')

    @classmethod
    def long_date(cls, date):
        return cls.format_date_to_str(date, '%B %d, %Y %I:%M %p')

    @classmethod
    def format_time_to_str(cls, date):
        default_datetime = datetime.strptime('01/01/0001 12:00 AM', '%d/%m/%Y %I:%M %p')

        if date == default_datetime:
            return ''

        return datetime.strftime(date, '%I:%M %p')


class Email:
    email = app.config['NOREPLY_EMAIL']
    password = app.config['NOREPLY_PASSWORD']
    server = EmailServer(
        email=email,
        password=password,
        domain=app.config['NOREPLY_DOMAIN'],
        port=app.config['NOREPLY_PORT']
    )

    @classmethod
    def send_password_recovery_email(cls, account, reset_token):
        subject = 'Popzapp - Request for Password Reset'
        to_list = [account.email]

        body = '\
        Hi {0},\n\
        It seems that you have requested for a password reset. Click the link below to confirm and reset your password:\n\
        {1}\n\n\
        If you did not request a password reset, please ignore this message.\n\n\
        Sincerely,\n\
        Popzapp Team\
        '.format(account.username, url_for('main.reset_password_page', reset_token=reset_token, _external=True))

        try:
            PopzappEmail.server.send_email(to_list, subject, body)
        except Exception as err:
            raise Exception('PopzappEmail.send_password_recovery_email() ERROR: ', err.args)

    @classmethod
    def send_welcome_email(cls, account):
        subject = 'Welcome to Popzapp'
        to_list = [account.email]

        body = '\
        Congratulations {0}!\n\n\
        \tYour Account has been created.\
        \nRegards,\
        \nPopzapp Team'.format(account.username)

        try:
            PopzappEmail.server.send_email(to_list, subject, body)
        except Exception as err:
            raise Exception('PopzappEmail.send_welcome_email() ERROR: ', err.args)

    @classmethod
    def send_order_email(cls, order):
        subject = 'Popzapp - Order Successful'
        to_list = [order.email]

        to = order.from_ or order.to_

        body = '\
        Thank You {0}!\n\n\
        \tYour Order has been sent to {1}. Please note that your order may take up to 7 days or earlier and an email will be sent after.\n\n\
        Regards,\n\
        Popzapp Team'.format(to, order.celebrity.account.first_name + ' ' + order.celebrity.account.last_name)

        try:
            PopzappEmail.server.send_email(to_list, subject, body)
        except Exception as err:
            raise Exception('PopzappEmail.send_order_email() ERROR: ', err.args)

    @classmethod
    def send_decline_email(cls, order):
        subject = 'Popzapp - Order Declined'
        to_list = [order.email]

        to = order.from_ or order.to_

        body = 'Dear {0},\n\n\
        \tYour Order has been declined by {1} and has stated the following reason: "{2}". Your payment will be returned within 7 days and an email will be sent after.\n\n\
        Regards,\n\
        Popzapp Team'.format(to, order.celebrity.account.first_name + ' ' + order.celebrity.account.last_name, order.remarks)

        try:
            PopzappEmail.server.send_email(to_list, subject, body)
        except Exception as err:
            raise Exception('PopzappEmail.send_decline_email() ERROR: ', err.args)

    @classmethod
    def send_video_email(cls, video):
        subject = 'Popzapp - Order Arrived'
        to_list = [video.order.email]

        to = video.order.from_ or video.order.to_
        body = 'Dear {0}!\n\n\
        \tYour video from {1} is already available. Here is the link to your video:\n\
        localhost:12000/view_video/{3} .Thank you for using Popzapp.\n\
        Regards,\n\
        Popzapp Team'.format(to, video.celebrity.account.first_name + ' ' + video.celebrity.account.last_name, video.id)

        try:
            PopzappEmail.server.send_email(to_list, subject, body)
        except Exception as err:
            raise Exception('PopzappEmail.send_video_email() ERROR: ', err.args)

