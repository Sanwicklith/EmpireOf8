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
                        "Be prescriptive, not academic: assume you have already done the deep "
                        "thinking and fact-finding available to you. Focus on concrete decisions "
                        "and execution. Always return a well-structured plan with headings: (1) "
                        "Situation & assumptions, (2) Recommended plan (step-by-step), and (3) "
                        "Next actions for the next 7–30 days, with any items that require "
                        "chairman approval clearly marked. Think across all 8 domains of the "
                        "empire when relevant."
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
                        "and risk management. Assume you have already synthesized the best "
                        "available agronomy and market knowledge. Always return a formatted "
                        "execution memo with headings: (1) Situation & key assumptions, (2) "
                        "Prescriptive plan of action (step-by-step, with timelines and rough "
                        "numbers where useful), and (3) Next 7–30 day action checklist with "
                        "any items that require chairman approval clearly labeled."
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


@app.post("/route/finance")
def route_finance(payload: RouteRequest):
    """Finance & Capital-specialized route.

    Use for cash flow, capital allocation, funding strategy, FX, and deal
    evaluation questions.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 FINANCE & CAPITAL AGENT, reporting to the COA. "
                        "You advise on cash flow, capital allocation, funding strategy, FX, and "
                        "deal evaluation for operating businesses in Southern Africa (especially "
                        "Zambia). Be conservative, numbers-driven, and explicit about assumptions. "
                        "Assume you have already pulled in any standard financial benchmarks or "
                        "industry patterns available to you. Always return a deal memo with "
                        "headings: (1) Situation & quantified assumptions, (2) 2–4 numerical "
                        "scenarios in ZMW (with key drivers and downside cases), and (3) a "
                        "prioritized action plan for the next 7–30 days with checkboxes and a "
                        "clear list of decisions that require chairman approval."
                    ),
                },
                {"role": "user", "content": payload.task},
            ],
            temperature=0.35,
        )

        reply = completion.choices[0].message.content

        return {
            "status": "ok",
            "task": payload.task,
            "agent": "Finance & Capital Agent (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "Finance & Capital Agent (error)",
            "error": str(e),
        }


@app.post("/route/real_estate")
def route_real_estate(payload: RouteRequest):
    """Real Estate & Infrastructure-specialized route.

    Use for land, buildings, logistics, utilities, and physical
    infrastructure decisions.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 REAL ESTATE & INFRASTRUCTURE AGENT, reporting "
                        "to the COA. You advise on land, buildings, logistics, utilities, and "
                        "energy/infra for projects in Southern Africa (especially Zambia). Be "
                        "practical about timelines, permits, and on-the-ground execution. Assume "
                        "you have already considered comparable projects and local constraints. "
                        "Always return: (1) Situation & assumptions, (2) a prescriptive phase-by-"
                        "phase plan (site acquisition, development, operations) with timelines "
                        "and rough budgets, and (3) a risks & mitigations section plus an explicit "
                        "list of items requiring chairman approval."
                    ),
                },
                {"role": "user", "content": payload.task},
            ],
            temperature=0.5,
        )

        reply = completion.choices[0].message.content

        return {
            "status": "ok",
            "task": payload.task,
            "agent": "Real Estate & Infrastructure Agent (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "Real Estate & Infrastructure Agent (error)",
            "error": str(e),
        }


@app.post("/route/people")
def route_people(payload: RouteRequest):
    """People & Organization-specialized route.

    Use for hiring, org design, incentives, culture, and performance topics.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 PEOPLE & ORGANIZATION AGENT, reporting to the "
                        "COA. You advise on hiring, org design, incentives, culture, and "
                        "performance management for fast-growing, owner-led businesses in "
                        "Southern Africa. Be concrete and practical, with scripts and examples "
                        "where helpful. Always return: (1) a sharp diagnosis of the people/org "
                        "situation, (2) a prescriptive org design and people plan (roles, "+
                        "reporting lines, incentives) including example scripts, and (3) a "
                        "7–30 day action checklist with which decisions the chairman must approve "
                        "clearly marked."
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
            "agent": "People & Organization Agent (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "People & Organization Agent (error)",
            "error": str(e),
        }


@app.post("/route/technology")
def route_technology(payload: RouteRequest):
    """Technology & Automation-specialized route.

    Use for software, data, integrations, and automation design.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 TECHNOLOGY & AUTOMATION AGENT, reporting to the "
                        "COA. You advise on software choices, architecture, integrations, and "
                        "automation to reduce manual work and improve reliability. Assume "
                        "resource-constrained but ambitious teams in Southern Africa. Always "
                        "return: (1) a concise current-state & assumptions section, (2) a "
                        "prescriptive implementation plan broken into milestones with suggested "
                        "tools/stack, and (3) a 7–30 day execution checklist suitable to copy into "
                        "a task tracker, including which changes require chairman approval."
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
            "agent": "Technology & Automation Agent (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "Technology & Automation Agent (error)",
            "error": str(e),
        }


@app.post("/route/growth")
def route_growth(payload: RouteRequest):
    """Sales & Growth-specialized route.

    Use for sales, pricing, marketing, and growth loop design.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 SALES & GROWTH AGENT, reporting to the COA. "
                        "You advise on GTM strategy, sales processes, pricing, marketing "
                        "experiments, and growth loops for B2B and B2C businesses in Southern "
                        "Africa. Be creative but grounded in unit economics. Always return: (1) "
                        "a concise growth diagnosis with key constraints, (2) 2–3 concrete growth "
                        "plays each with expected impact, rough numbers and risks, and (3) a "
                        "prioritized 7–30 day action plan with experiments, owners (if known) and "
                        "which commitments need chairman sign-off."
                    ),
                },
                {"role": "user", "content": payload.task},
            ],
            temperature=0.8,
        )

        reply = completion.choices[0].message.content

        return {
            "status": "ok",
            "task": payload.task,
            "agent": "Sales & Growth Agent (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "Sales & Growth Agent (error)",
            "error": str(e),
        }


@app.post("/route/governance")
def route_governance(payload: RouteRequest):
    """Regulation & Governance-specialized route.

    Use for compliance, contracts, licenses, boards, and risk topics.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 REGULATION & GOVERNANCE AGENT, reporting to the "
                        "COA. You help the chairman think about compliance, contracts, licenses, "
                        "boards, and controls, especially in Southern Africa. Be cautious and "
                        "risk-aware, and make it clear you are not a lawyer and your guidance is "
                        "not legal advice. Always return: (1) a structured issue summary, (2) "
                        "concrete options with pros/cons and risk levels, and (3) a prescriptive "
                        "7–30 day action plan that highlights which steps must wait for legal or "
                        "chairman approval."
                    ),
                },
                {"role": "user", "content": payload.task},
            ],
            temperature=0.3,
        )

        reply = completion.choices[0].message.content

        return {
            "status": "ok",
            "task": payload.task,
            "agent": "Regulation & Governance Agent (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "Regulation & Governance Agent (error)",
            "error": str(e),
        }


@app.post("/route/health")
def route_health(payload: RouteRequest):
    """Health & Education-specialized route.

    Use for questions about the chairman's own health, learning, and skill
    building, and for key people in the empire.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 HEALTH & EDUCATION AGENT, reporting to the COA. "
                        "You help the chairman design routines, habits, and learning plans for "
                        "health, fitness, and skill-building for themselves and key people. You "
                        "are not a doctor and do not provide medical advice; instead you provide "
                        "general educational guidance and recommend consulting professionals for "
                        "medical decisions. Always return: (1) a concise situation & goals "
                        "section, (2) 1–3 highly specific habit/learning programs with daily/" 
                        "weekly structures, and (3) a 7–30 day action plan that the chairman can "
                        "review and approve."
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
            "agent": "Health & Education Agent (OpenAI gpt-4o-mini)",
            "reply": reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "Health & Education Agent (error)",
            "error": str(e),
        }


# Map short agent keys to their route handlers so the COA can orchestrate them.
AGENT_HANDLERS = {
    "agriculture": route_agriculture,
    "finance": route_finance,
    "real_estate": route_real_estate,
    "people": route_people,
    "technology": route_technology,
    "growth": route_growth,
    "governance": route_governance,
    "health": route_health,
}


@app.post("/route/team")
def route_team(payload: RouteRequest):
    """Team-orchestrated route chaired by the COA.

    The COA selects which domain agents to consult (up to a small number),
    calls them internally, and then synthesizes a single, integrated answer
    for the chairman.
    """
    try:
        # First, ask the COA which agents to consult.
        selection_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are the EMPIRE OF 8 COA selecting which sub-agents to consult. "
                        "Available agents with their keys:\n"
                        "- agriculture: Agriculture Agent\n"
                        "- finance: Finance & Capital Agent\n"
                        "- real_estate: Real Estate & Infrastructure Agent\n"
                        "- people: People & Organization Agent\n"
                        "- technology: Technology & Automation Agent\n"
                        "- growth: Sales & Growth Agent\n"
                        "- governance: Regulation & Governance Agent\n"
                        "- health: Health & Education Agent\n\n"
                        "Given the chairman's task, respond with ONE line only in the format:\n"
                        "AGENTS: key1,key2,...\n"
                        "Use at most 3 keys from the list above, no explanations."
                    ),
                },
                {"role": "user", "content": payload.task},
            ],
            temperature=0.2,
        )

        selection_text = selection_completion.choices[0].message.content or ""
        selected_keys = []

        if "AGENTS:" in selection_text:
            _, _, tail = selection_text.partition("AGENTS:")
            raw = tail.strip()
            if raw:
                raw = raw.replace("[", "").replace("]", "")
                for part in raw.split(","):
                    key = part.strip().lower()
                    if key and key in AGENT_HANDLERS and key not in selected_keys:
                        selected_keys.append(key)

        # If nothing was selected, fall back to answering as the COA alone.
        consulted = []

        for key in selected_keys:
            handler = AGENT_HANDLERS.get(key)
            if not handler:
                continue
            sub_result = handler(RouteRequest(task=payload.task))
            consulted.append(
                {
                    "key": key,
                    "agent": sub_result.get("agent"),
                    "status": sub_result.get("status"),
                    "reply": sub_result.get("reply"),
                }
            )

        # Now ask the COA to synthesize the agent memos into one answer.
        synthesis_messages = [
            {
                "role": "system",
                "content": (
                    "You are the EMPIRE OF 8 COA chairing a board of domain agents. "
                    "You have received their memos below. Integrate them into a single, "
                    "clear and prescriptive recommendation for the chairman. Resolve "
                    "contradictions and be decisive. Assume the agents have already done "
                    "the necessary research and deep thinking. Always return with "
                    "explicit headings: (1) Situation & key assumptions, (2) Integrated "
                    "recommended plan (step-by-step, across domains where relevant), and "
                    "(3) 7–30 day execution checklist, including a bullet list of items "
                    "requiring formal chairman approval before proceeding."
                ),
            },
            {
                "role": "user",
                "content": f"Chairman's original task:\n{payload.task}",
            },
        ]

        if consulted:
            memo_texts = []
            for c in consulted:
                memo_texts.append(
                    f"Agent: {c.get('agent')}\n"
                    f"Status: {c.get('status')}\n"
                    f"Reply:\n{c.get('reply')}\n"
                )
            synthesis_messages.append(
                {
                    "role": "user",
                    "content": "Sub-agent memos:\n\n" + "\n---\n".join(memo_texts),
                }
            )
        else:
            synthesis_messages.append(
                {
                    "role": "user",
                    "content": "No sub-agents were consulted; answer as the COA alone.",
                }
            )

        final_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=synthesis_messages,
            temperature=0.6,
        )

        final_reply = final_completion.choices[0].message.content

        return {
            "status": "ok",
            "task": payload.task,
            "agent": "COA Orchestrator (team mode)",
            "consulted_agents": consulted,
            "reply": final_reply,
        }
    except Exception as e:  # pragma: no cover - surface error details to caller
        return {
            "status": "error",
            "task": payload.task,
            "agent": "COA Orchestrator (error)",
            "error": str(e),
        }
