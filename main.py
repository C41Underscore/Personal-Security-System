from google_drive_handler import DriveHandler
from email_sender import EmailHandler
from network_handler import MACHandler
from time_handler import get_current_date
from esp32_handler import CameraCollection
from time import sleep
from datetime import timedelta
import schedule
import logging
import multiprocessing
import time_handler
from sys import stdout
from math import ceil

MAX_CAMS = 6
NUMBER_OF_CAMS = 2
NUMBER_OF_PROCESSES = ceil(NUMBER_OF_CAMS / 2)
NUMBER_OF_CAMS_PER_CORE = ceil(NUMBER_OF_CAMS / NUMBER_OF_PROCESSES)
print(NUMBER_OF_CAMS, NUMBER_OF_PROCESSES, NUMBER_OF_CAMS_PER_CORE)


# TODO - Structure the code to make it efficient and readable
# TODO - Plan how the system will be managed.  What will trigger cameras, what extra physical components will be needed, and how will the camera be maintained
# TODO - Get email notifications working for specific triggers (TBD)


def state_check(timer, network_check, q):
    is_active = False
    # logging.debug("Checking the timer...")
    # timer_check = timer()
    # logging.debug("timer_check = %s" % timer_check)
    # if timer_check:
    #     q.put(True)
    # else:
    logging.debug("Checking network connections...")
    network_check = network_check()
    logging.debug("network_check = %s" % network_check)
    q.put(network_check)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    logging.getLogger().addHandler(logging.StreamHandler(stdout))
    drive = DriveHandler()
    emailer = EmailHandler()
    network_checker = MACHandler()
    logging.debug("Creating the CameraCollection(s)...")
    camera_collections = []
    for i in range(NUMBER_OF_PROCESSES):
        if NUMBER_OF_CAMS == 1:
            camera_collections.append(CameraCollection(1))
        elif i + 1 == NUMBER_OF_PROCESSES and NUMBER_OF_CAMS % 2 == 1:
            camera_collections.append(CameraCollection(NUMBER_OF_CAMS_PER_CORE - 1))
        else:
            camera_collections.append(CameraCollection(NUMBER_OF_CAMS_PER_CORE))
    logging.debug("Creating camera checking process...")
    camera_queue = multiprocessing.Queue()
    camera_collection_processes = [multiprocessing.Process(
        target=camera_collections[i].camera_loop,
        kwargs={
            "drive": drive,
            "activation_q": camera_queue
        }
    ) for i in range(NUMBER_OF_PROCESSES)]
    schedule.every().monday.do(drive.refresh_drive, get_current_date())
    # schedule.every().monday.do(drive.refresh_logs, get_current_date(s))
    schedule.every().day.do(drive.upload_log)
    # schedule.every().day.at("23:59").do(emailer.email_logs)
    schedule.every(10).seconds.do(state_check, time_handler.check_time, network_checker.check_network, camera_queue)
    logging.debug("Starting camera checking process...")
    for process in camera_collection_processes:
        process.start()
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()

