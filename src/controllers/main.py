from src.automation.scheduler import start_scheduler
import time

start_scheduler()
print("✅ Automation Layer started... waiting for triggers.")

# Keep process alive
while True:
    time.sleep(60)

