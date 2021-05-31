import time
from datetime import timedelta, datetime
import logging


START_TIME = timedelta(hours=0, minutes=0, seconds=0)
END_TIME = timedelta(hours=7, minutes=30, seconds=0)


def get_formatted_time(use_date):
    if use_date:
        return datetime.now().strftime("%Y-%m-%d")
    return datetime.now().strftime("%H%M%S")


def get_current_date():
    return datetime.now().date()


def check_time():
    logging.info("Checking current time...")
    current_time = time.localtime()
    current_time = timedelta(hours=current_time.tm_hour, minutes=current_time.tm_min, seconds=current_time.tm_sec)
    if START_TIME < current_time < END_TIME:
        return True
    else:
        return False
