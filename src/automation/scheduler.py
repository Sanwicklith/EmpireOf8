# src/automation/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from automation.events import check_milestones
from automation.calendar_connector import add_calendar_event

scheduler = BackgroundScheduler()

def remind_chief_aim():
    msg = f"[{datetime.now()}] Reminder: Review Your Chief Aim ( K1 Million target)."
    print(msg)
    add_calendar_event(
	"Chief Aim Reminder",
	"Time to Review my K1m progress and assets.",
	datetime.now() + timedelta(minutes=1),
    )

def start_scheduler():
    scheduler.add_job(remind_chief_aim, "cron", hour=9, minute=16)
    scheduler.add_job(remind_chief_aim, "cron", hour=12, minute=30)
    scheduler.add_job(remind_chief_aim, "cron", hour=21, minute=0)
    scheduler.add_job(check_milestones, "interval", hours=24)
    scheduler.start()

