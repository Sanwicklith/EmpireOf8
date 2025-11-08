from automation.scheduler import start_scheduler
import time

print("✅ Automation Layer started... waiting for triggers.")
start_scheduler()

while True:
    time.sleep(60)
