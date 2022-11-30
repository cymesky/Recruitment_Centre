import os

from apscheduler.schedulers.background import BackgroundScheduler
from .scrapy_update import update_scrapy


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_scrapy, 'interval', hours=1, jitter=120)

    if os.environ.get('RUN_MAIN'):
        scheduler.start()
