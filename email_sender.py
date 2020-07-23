import yagmail

receiver = "MASSIVE EMAIL"
body = "big up the yagmail test"
filename = "test-image.jpg"
yag = yagmail.SMTP("N0000 GET OOF MY EMAMIAIL")

def main():
    yag.send(
            to=receiver,
            subject="who ate my ch33s3??",
            contents=body,
            attachments=filename
        )


if __name__ == "__main__":
    main()
