from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from garden import tasks

scheduler = BackgroundScheduler()

def start():
    scheduler.add_job(tasks.whats_up, 'interval', seconds=59, id="butt_head")
    scheduler.start()

def change(dur):
    scheduler.remove_job('butt_head')
    scheduler.add_job(tasks.whats_up, 'interval', seconds=dur, id="butt_head")