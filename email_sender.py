import yagmail
from decouple import config, Csv


class EmailHandler:

    def __init__(self):
        self.yag = yagmail.SMTP(config("SENDING_EMAIL"))
        self.receiving_emails = config("RECEIVING_EMAILS", cast=Csv())

    def send_email(self, subject, body, *attachments):
        contents = list(attachments)
        contents.insert(0, body)
        self.yag.send(
            to=self.receiving_emails,
            subject=subject,
            contents=contents
        )
