import google_drive_auth
import google_drive_upload
from esp32_handler import esp32CamInterface
from time import sleep

#TODO - Create the main framework of the program, going to have to wait for better internet to use the ESPs
#TODO - Structure the code to make it efficient and readable
#TODO - Create a test set of photos to test google drive uploads
#TODO - Play around with pydrive and get photo uploads working
#TODO - Play around with pydrive and get video upload working (use opencv and test with webcam)
#TODO - Plan how the system will be managed.  What will trigger cameras, what extra physical components will be needed, and how will the camera be maintained
#TODO - Plan how the file system will be organised
#TODO - Get email notifications working for specific triggers (TBD)
#TODO - Create a script to empty the google drive file regulary to prevent it from becoming full


def main(testing):
    drive = google_drive_auth.authenticate()
    esp32cam = esp32CamInterface(1, "${IP_ADDRESS}", "Living Room")
    if testing:
        for i in range(0, 10):
            esp32cam.takeImage(False)
            sleep(5)


if __name__ == "__main__":
    main(True)
