from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# ------------------------------------------------------
# MongoDB Connection
# ------------------------------------------------------

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, uuidRepresentation="standard")

# Main operational DB used by EmpireOf8
db = client["empireof8_ops"]

# ------------------------------------------------------
# Collection handles (must exist for imports)
# ------------------------------------------------------

ops_events = db["ops_events"]
chief_aim = db["chief_aim"]
tasks = db["tasks"]
alerts = db["alerts"]
agent_state = db["agent_state"]

# ------------------------------------------------------
# Utility getter
# ------------------------------------------------------

def get_db():
    return db

