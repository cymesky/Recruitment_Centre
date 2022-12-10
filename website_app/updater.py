import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from .scrapy_update import update_scrapy


def start():
    scheduler = BackgroundScheduler(timezone="Europe/Warsaw")
    first_start_time = datetime.datetime.now() + datetime.timedelta(seconds=15)
    scheduler.add_job(update_scrapy, 'interval', minutes=60,
                      jitter=120, next_run_time=first_start_time)

    if os.environ.get('RUN_MAIN'):
        scheduler.start()

