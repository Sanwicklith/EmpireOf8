import os, datetime
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/calendar"]
cred_path = os.getenv("CREDENTIALS_PATH")
token_path = os.getenv("TOKEN_PATH")

def get_calendar_service():
    creds = None
    if token_path and os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

def add_calendar_event(summary, description, event_time):
    service = get_calendar_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": event_time.isoformat(), "timeZone": os.getenv("TIMEZONE","Africa/Lusaka")},
        "end":   {"dateTime": (event_time + datetime.timedelta(hours=1)).isoformat(),
                  "timeZone": os.getenv("TIMEZONE","Africa/Lusaka")},
    }
    service.events().insert(calendarId="primary", body=event).execute()

