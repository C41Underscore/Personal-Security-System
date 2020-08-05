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
from os import remove
import logging


# TODO - Create the main framework of the program, going to have to wait for better internet to use the ESPs
# TODO - Structure the code to make it efficient and readable
# TODO - Create a test set of photos to test google drive uploads
# TODO - Play around with pydrive and get photo uploads working
# TODO - Play around with pydrive and get video upload working (use opencv and test with webcam)
# TODO - Plan how the system will be managed.  What will trigger cameras, what extra physical components will be needed, and how will the camera be maintained
# TODO - Plan how the file system will be organised
# TODO - Get email notifications working for specific triggers (TBD)
# TODO - Create a script to empty the google drive file regulary to prevent it from becoming full


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    # Initialse the main system objects
    drive = DriveHandler()
    timer = TimeHandler(timedelta(hours=0, minutes=0, seconds=0), timedelta(hours=7, minutes=30, seconds=0))
    emailer = EmailHandler()
    network_checker = MACHandler()
    logging.info("Creating the CameraCollection.")
    cameras = CameraCollection(1)
    schedule.every().monday.do(drive.refresh_drive, get_current_date())
    schedule.every().monday.do(drive.refresh_logs, get_current_date())
    schedule.every().day.do(drive.upload_log)
    while True:
        schedule.run_pending()
        logging.info("Checking the timer...")
        timer_check = timer.check_time()
        logging.debug("timer_check = %s" % timer_check)
        if timer_check:
            logging.info("check_time returned True, system will activate.")
        if not timer_check:
            logging.info("Checking network connections...")
            network_check = network_checker.check_network()
            logging.info("network_check = %s" % network_check)
            if network_check:
                logging.info("check_network returned True, system will activate")
        sleep(1)


if __name__ == "__main__":
    main()
