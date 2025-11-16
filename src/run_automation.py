import logging
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from contextlib import contextmanager

# -----------------------------
# Persistence Layer
# -----------------------------
from src.core.db import SessionLocal
from src.automation.persistence import (
    log_ops_event,
    write_audit_log,
    bump_kpi,
    update_chief_aim_reviewed
)

# -----------------------------
# Logging Setup
# -----------------------------
from src.core.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger("automation")

# -----------------------------
# Google Calendar Setup
# -----------------------------

def load_google_creds():
    creds = Credentials.from_authorized_user_file("config/token.json")
    return creds

def add_calendar_event(summary: str):
    creds = load_google_creds()
    service = build("calendar", "v3", credentials=creds)

    now = datetime.utcnow().isoformat() + "Z"

    event = {
        "summary": summary,
        "start": {"dateTime": now},
        "end": {"dateTime": now}
    }

    service.events().insert(calendarId="primary", body=event).execute()
    logger.info("Calendar event added")


# -----------------------------
# DB Session Helper
# -----------------------------

@contextmanager
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# AUTOMATION JOBS WITH PERSISTENCE
# -----------------------------

def remind_chief_aim():
    now = datetime.now()
    msg = f"[{now}] Reminder: Review Your Chief Aim (K1 Million target)."
    logger.info(msg)

    # 1. MongoDB log
    log_ops_event("remind_chief_aim", {"message": msg})

    # 2. Audit + KPI in Postgres
    with db_session() as db:
        write_audit_log(
            db,
            category="automation",
            action="remind_chief_aim",
            status="success",
            detail={"message": msg}
        )
        bump_kpi(db, "automation", "reminder_runs", 1)

    # 3. Update Chief Aim timestamp
    update_chief_aim_reviewed()

    # 4. Google Calendar event
    add_calendar_event("Review your Chief Aim")


def check_milestones():
    result = {
        "next_milestone": "MVP Launch",
        "date": "11 Nov 2025",
        "days_remaining": 2
    }

    logger.info("Milestones checked")

    # 1. Mongo log
    log_ops_event("check_milestones", result)

    # 2. Audit + KPI in Postgres
    with db_session() as db:
        write_audit_log(
            db,
            category="automation",
            action="check_milestones",
            status="success",
            detail=result
        )
        bump_kpi(db, "automation", "milestone_checks", 1)


# -----------------------------
# SCHEDULER SETUP
# -----------------------------

def start_scheduler():
    tz = pytz.timezone("Africa/Lusaka")
    scheduler = BackgroundScheduler(timezone=tz)

    # Chief Aim reminders
    scheduler.add_job(remind_chief_aim, "cron", hour=11, minute=13)
    scheduler.add_job(remind_chief_aim, "cron", hour=12, minute=30)
    scheduler.add_job(remind_chief_aim, "cron", hour=21, minute=0)

    # Milestone checker
    scheduler.add_job(check_milestones, "cron", hour=6, minute=0)

    scheduler.start()
    logger.info("Scheduler started")
    print("✅ Automation Layer started... waiting for triggers.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.info("Shutting down…")
        scheduler.shutdown()


if __name__ == "__main__":
    start_scheduler()

