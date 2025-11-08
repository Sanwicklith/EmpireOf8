import datetime

def check_milestones():
    milestones = {
        "MVP Launch": datetime.date(2025, 11, 11),
        "Chief Aim": datetime.date(2026, 5, 17)
    }
    today = datetime.date.today()
    for name, date in milestones.items():
        days = (date - today).days
        if days in [30, 7, 1, 0]:
            print(f"Alert ⚠️ {name} in {days} days!")
