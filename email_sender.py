import yagmail
from decouple import config, Csv
from time_handler import get_formatted_time
import logging


class EmailHandler:

    def __init__(self):
        self.yag = yagmail.SMTP(config("SENDING_EMAIL"))
        self.receiving_emails = config("RECEIVING_EMAILS", cast=Csv())

    def __send_email(self, subject, body, *attachments):
        logging.info("Sending email to %s, Subject: %s" % (self.receiving_emails, subject))
        contents = list(attachments)
        contents.insert(0, body)
        self.yag.send(
            to=self.receiving_emails,
            subject=subject,
            contents=contents
        )

    def email_logs(self):
        logging.debug("Emailing daily logs to users...")
        main_body = ""
        with open("app.log", "r") as logs:
            for line in logs:
                main_body += line
        self.__send_email("Security Logs from %s" % get_formatted_time(True), main_body)
