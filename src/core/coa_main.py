from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

# Import the orchestrator factory
from core.orchestrator.router import build_default_orchestrator

# Build the mastermind engine instance
orchestrator = build_default_orchestrator()

app = FastAPI(
    title="Empire of 8 - Mastermind Engine",
    version="0.3.0",
)


# -------------------------------
# Request / Response Models
# -------------------------------

class ChatRequest(BaseModel):
    message: str
    preferred_pillar: str | None = None


class ChatResponse(BaseModel):
    reply: str
    pillar_used: str | None = None


# -------------------------------
# API Endpoints
# -------------------------------

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """
    Main interface for sending natural language queries
    to the Empire of 8 mastermind orchestrator.
    """

    reply = await orchestrator.handle(
        query=payload.message,
        preferred_pillar=payload.preferred_pillar,
        context={"source": "api"},
    )

    return ChatResponse(
        reply=reply,
        pillar_used=payload.preferred_pillar,
    )


@app.get("/")
async def root():
    return {
        "status": "running",
        "engine": "Empire of 8 Mastermind v0.3.0",
        "message": "Mastermind Engine is active.",
    }

