from google_drive_handler import DriveHandler
import email_sender
import yagmail
from esp32_handler import ESP32CamInterface
from time import sleep
from datetime import timedelta
import PIL
from time_handler import get_formatted_time
from decouple import config
import schedule


#TODO - Create the main framework of the program, going to have to wait for better internet to use the ESPs
#TODO - Structure the code to make it efficient and readable
#TODO - Create a test set of photos to test google drive uploads
#TODO - Play around with pydrive and get photo uploads working
#TODO - Play around with pydrive and get video upload working (use opencv and test with webcam)
#TODO - Plan how the system will be managed.  What will trigger cameras, what extra physical components will be needed, and how will the camera be maintained
#TODO - Plan how the file system will be organised
#TODO - Get email notifications working for specific triggers (TBD)
#TODO - Create a script to empty the google drive file regulary to prevent it from becoming full


start_time = timedelta(hours=0, minutes=0, seconds=0)
end_time = timedelta(hours=7, minutes=30, seconds=0)


def main():
    drive_interface = DriveHandler()
    email, receiving_emails = email_sender.initialise_yagmail()
    cam_addresses = config("ESPCAM_IP_ADDRESSES")
    esp32cam = ESP32CamInterface(1, cam_addresses[0], "Living Room")
    image, current_time = esp32cam.take_image(False)
    image.save("%s.jpg" % current_time)
    drive_interface.upload(get_formatted_time(True), current_time)


def print_time():
    print(get_formatted_time(False))


if __name__ == "__main__":
    schedule.every(1).seconds.do(print_time)
    while True:
        schedule.run_pending()
