from google_drive_handler import DriveHandler
from time_handler import TimeHandler
from email_sender import EmailHandler
from network_handler import MACHandler
from time_handler import get_current_date
from sys import exit
from time import sleep
import yagmail
from esp32_handler import CameraCollection
from time import sleep
from datetime import timedelta
import PIL
from time_handler import get_formatted_time
from decouple import config, Csv
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


def main():
    #Initialse the main system objects
    drive = DriveHandler()
    timer = TimeHandler(timedelta(hours=0, minutes=0, seconds=0), timedelta(hours=7, minutes=30, seconds=0))
    emailer = EmailHandler()
    network_checker = MACHandler()
    camera_ips = list(zip(config("ESPCAM_IP_ADDRESSES", cast=Csv()), config("ESPCAM_LOCATIONS", cast=Csv())))
    cameras = CameraCollection(*camera_ips)
    #Schedule the object tasks
    schedule.every().monday.do(drive.refresh_drive, get_current_date())
    while True:
        schedule.run_pending()
        print("Checking time...")
        timer_check = timer.check_time()
        print("Checking network...")
        network_check = network_checker.check_network()
        if network_check:
            print("There is no cheese in the house :0")
        sleep(1)

    #add esp32 handlers later


if __name__ == "__main__":
    main()
