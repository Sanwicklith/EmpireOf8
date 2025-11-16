import json
from pathlib import Path

def check_policy(task_type: str, amount: float):
    policy = json.loads(Path("config/policies.json").read_text())
    if task_type in policy["approval_required"] or amount > policy["spending_limit_zmw"]:
        return "ESCALATE"
    return "APPROVE"
