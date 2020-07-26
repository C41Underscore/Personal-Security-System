import yagmail


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
    email = input("Enter email> ")
    yag = yagmail.SMTP(email)
    receiving_emails = []
    next_email = ""
    while next_email != "/done":
        print("Current receiving emails:", ", ".join(receiving_emails))
        next_email = input("Enter next receiving email(enter /done to finish)> ")
        if next_email != "" and next_email != "/done":#Insert regex here
            receiving_emails.append(next_email)
    return yag, receiving_emails
    # send_email(yag, receiving_emails, "The president stole my cheese :0", "but he didn't take the crackers ;)", "test-image.jpg")

y, r = initialise_yagmail()
send_email(y, r, "chippty", "choppty", yagmail.inline("test-image.jpg"))

