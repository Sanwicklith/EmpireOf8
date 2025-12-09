from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import datetime

# Import settings so that in development ENVIRONMENT!=production triggers
# load_dotenv() and picks up values from a local .env file. In production
# (ENVIRONMENT=production) this import is effectively a no-op for secrets.
from .settings import ENVIRONMENT  # noqa: F401

app = FastAPI()

# OpenAI client; expects OPENAI_API_KEY in the environment.
client = OpenAI()

# Allow browser-based frontends (including the static /ui page) to call this API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the UI in the /ui path from the repo's ui/ directory.
app.mount("/ui", StaticFiles(directory="ui", html=True), name="ui")


@app.get("/")
def home():
    return {
        "message": "Empire of 8 — COA online",
        "timestamp": datetime.datetime.now().isoformat(),
        "ui_url": "/ui"  # hint for humans/clients
    }


class RouteRequest(BaseModel):
    task: str


@app.post("/route")
def route_task(payload: RouteRequest):
    """Route a free-form task string to the OpenAI-powered COA (Chairman's brain).

    Generic entry point. The COA chooses how to respond and may conceptually
    delegate to domain agents, but this endpoint is not domain-specific.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the Empire of 8 Chairman's AI brain (COA). "
                        "Answer clearly and practically, focusing on next actions, "
                        "and think across all 8 domains of the empire."
                    ),
                },
                {"role": "user", "content": payload.task},
            ],
            temperature=0.7,
        )

        reply = completion.choices[0].message.content

        return {
            "status": "ok",
            "task": payload.task,
            "agent": "COA (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "COA (error)",
            "error": str(e),
        }


@app.post("/route/agriculture")
def route_agriculture(payload: RouteRequest):
    """Agriculture-specialized route.

    The COA conceptually delegates to the Agriculture Agent. Use this for
    any tasks related to farming, livestock, agro-processing, agribusiness
    finance, or agricultural policy.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 AGRICULTURE AGENT, reporting to the COA. "
                        "You advise on crops, livestock, soil health, agribusiness finance, "
                        "and operational execution in Southern Africa (especially Zambia). "
                        "Be concrete, numbers-driven, and obsessed with yield, profitability, "
                        "and risk management. Always return: (1) a short summary and (2) a "
                        "clear next-actions list for the next 7–30 days."
                    ),
                },
                {"role": "user", "content": payload.task},
            ],
            temperature=0.6,
        )

        reply = completion.choices[0].message.content

        return {
            "status": "ok",
            "task": payload.task,
            "agent": "Agriculture Agent (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "Agriculture Agent (error)",
            "error": str(e),
        }
