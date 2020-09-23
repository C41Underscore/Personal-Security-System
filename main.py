from google_drive_handler import DriveHandler
from time_handler import TimeHandler
from email_sender import EmailHandler
from network_handler import MACHandler
from time_handler import get_current_date
from esp32_handler import CameraCollection
from time import sleep
from datetime import timedelta
import schedule
import logging
import multiprocessing
from sys import stdout
from math import ceil


NUMBER_OF_CAMS = 2
NUMBER_OF_PROCESSES = ceil(NUMBER_OF_CAMS / 2)
NUMBER_OF_CAMS_PER_CORE = ceil(NUMBER_OF_CAMS / NUMBER_OF_PROCESSES)
print(NUMBER_OF_CAMS, NUMBER_OF_PROCESSES, NUMBER_OF_CAMS_PER_CORE)


# TODO - Structure the code to make it efficient and readable
# TODO - Plan how the system will be managed.  What will trigger cameras, what extra physical components will be needed, and how will the camera be maintained
# TODO - Get email notifications working for specific triggers (TBD)


def loop(timer, network_checker, q):
    is_active = False
    while True:
        schedule.run_pending()
        logging.debug("Checking the timer...")
        timer_check = timer.check_time()
        logging.debug("timer_check = %s" % timer_check)
        if timer_check:
            q.put(True)
        else:
            logging.debug("Checking network connections...")
            network_check = network_checker.check_network()
            logging.debug("network_check = %s" % network_check)
            q.put(network_check)
        sleep(1)


def setup():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="app.log",
        filemode="w",
        format="%(asctime)s - %(levelname)s: %(message)s",
        datefmt="%H:%M:%S"
    )
    logging.getLogger().addHandler(logging.StreamHandler(stdout))
    drive = DriveHandler()
    timer = TimeHandler(timedelta(hours=0, minutes=0, seconds=0), timedelta(hours=7, minutes=30, seconds=0))
    emailer = EmailHandler()
    network_checker = MACHandler()
    logging.debug("Creating the CameraCollection(s)...")
    camera_collections = []
    for i in range(NUMBER_OF_PROCESSES):
        if i + 1 == NUMBER_OF_PROCESSES and NUMBER_OF_CAMS % 2 == 1:
            camera_collections.append(CameraCollection(NUMBER_OF_CAMS_PER_CORE - 1))
        else:
            camera_collections.append(CameraCollection(NUMBER_OF_CAMS_PER_CORE))
    schedule.every().monday.do(drive.refresh_drive, get_current_date())
    # schedule.every().monday.do(drive.refresh_logs, get_current_date(s))
    schedule.every().day.do(drive.upload_log)
    schedule.every().day.at("23:59").do(emailer.email_logs)
    logging.debug("Creating camera checking process...")
    camera_queue = multiprocessing.Queue()
    camera_collection_processes = [multiprocessing.Process(
        target=camera_collections[i].camera_loop,
        kwargs={
            "drive": drive,
            "activation_q": camera_queue
        }
    ) for i in range(NUMBER_OF_PROCESSES)]
    logging.debug("Starting camera checking process...")
    for process in camera_collection_processes:
        process.start()
    loop(timer, network_checker, camera_queue)


if __name__ == "__main__":
    setup()
