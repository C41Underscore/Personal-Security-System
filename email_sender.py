import yagmail
from decouple import config, Csv


def send_email(yag, receiver, subject, body, *attachments):
    contents = list(attachments)
    contents.insert(0, body)
    yag.send(
        to=receiver,
        subject=subject,
        contents=contents
    )
    print("Email sent to %s" % ", ".join(receiver))


def initialise_yagmail():
    return yagmail.SMTP(config("SENDING_EMAIL")), config("RECEIVING_EMAILS", cast=Csv())
    # send_email(yag, receiving_emails, "The president stole my cheese :0", "but he didn't take the crackers ;)", "test-image.jpg")
