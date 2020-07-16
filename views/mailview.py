import sys
import os
import time
import smtplib
import ssl

from email.mime.text import MIMEText
from subprocess import Popen, PIPE

from views.clientdatasocketadapter import *

class MailView:
    def __init__(self, config):
        self.config = config
        self.adapter = clientDataSocketAdapter()
        self.view_data = self.adapter.get_view_data()
        self.soil_dry_mail_not_send = True
        self.cistern_empty_mail_not_send = True
        self.cistern_full_mail_not_send = True
        self.battery_mail_not_send = True
        print("Welcome to Gardencontroller Mailer")

    def __del__(self):
        del self.adapter

    def update(self):
        self.view_data = self.adapter.get_view_data()
        self.soil_dry_mail_not_send \
            = self.__check(self.__moist_inacceptable(), self.soil_dry_mail_not_send,
                         "[Gardencontroller] Earth is Dry", "Earth is dry, go watering (manually)!")
        self.cistern_empty_mail_not_send \
            = self.__check(self.__cistern_empty(), self.cistern_empty_mail_not_send,
                         "[Gardencontroller] Cistern Empty", "Cistern is empty!")
        self.cistern_full_mail_not_send \
            = self.__check(self.__cistern_full(), self.cistern_full_mail_not_send,
                         "[Gardencontroller] Cistern Full", "Cistern is full!")
        self.battery_mail_not_send \
            = self.__check(self.__battery_empty(), self.battery_mail_not_send,
                         "[Gardencontroller] Battery Low", "Battery is going to be depleated!")

    def __check(self, check_value, mail_not_send, subject, mail_text):
        if check_value and mail_not_send:
            print("Sending mail : " + mail_text)
            self.__send_email(subject, mail_text)
            return(False)
        if not check_value:
            return(True)

    def __moist_inacceptable(self):
        return(self.view_data["soil_moisture"] <= 35)

    def __cistern_empty(self):
        return(self.view_data["cistern_distance"] >= (self.view_data["cistern_height"] - 1))

    def __cistern_full(self):
        return(self.view_data["cistern_distance"] <= 5.0)

    def __battery_empty(self):
        return(self.view_data["battery_charge_status"] <= 10)

    def __send_email(self, subject, text):
        if os.name == 'nt':
            with smtplib.SMTP(self.config["email_smtp_server"], self.config["email_smtp_port"]) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
                server.login(self.config["email_from"], self.config["email_smtp_pw"])
                server.sendmail(self.config["email_from"], self.config["email_to"], text)
        else:
            msg = MIMEText(text)
            msg["From"] = self.config["email_from"]
            msg["To"] = self.config["email_to"]
            msg["Subject"] = subject
            p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
            p.communicate(msg.as_string())
