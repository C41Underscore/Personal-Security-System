import time
from datetime import timedelta


class TimeHandler:

    def __init__(self, time_start, time_end):
        self.start = time_start
        self.end = time_end

    def check_time(self):
        current_time = time.localtime()
        current_time = timedelta(hours=current_time.tm_hour, minutes=current_time.tm_min, seconds=current_time.tm_sec)
        if self.start < current_time < self.end:
            return True
        else:
            return False
