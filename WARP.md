# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Environment and dependencies

- This is a Python project with a small FastAPI HTTP service, a background automation/scheduler layer, and a simple HTML UI.
- Dependencies are pinned in `requirements.txt`. Install them into a virtual environment before running anything.
  - Bash:
    - `python -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install -r requirements.txt`
  - PowerShell:
    - `python -m venv .venv`
    - `Set-ExecutionPolicy -Scope Process Bypass -Force` (if needed once to allow scripts)
    - `.\.venv\Scripts\Activate.ps1`
    - `pip install -r requirements.txt`
- Many modules call `load_dotenv()` and read environment variables. Expect at least these to be required:
  - `POSTGRES_URL` (SQLAlchemy connection string)
  - `MONGO_URI` (MongoDB connection string)
  - `CREDENTIALS_PATH`, `TOKEN_PATH`, optionally `TIMEZONE` for Google Calendar integration.

## Common commands

All commands assume the working directory is the repo root.

### Initialize the Postgres schema

- Create tables defined in `src/core/models.py`:
  - `python -m src.core.init_db`

### Run the FastAPI "COA" service

The main HTTP API used by the UI lives in `src/core/coa_main.py` (`FastAPI` app named `app`).

- Start the dev server with Uvicorn:
  - `python -m uvicorn src.core.coa_main:app --reload --port 8080`
- The legacy helper script `scripts/run_coa.sh` does something similar for Unix shells, but it assumes a virtualenv named `myvenv` and a module path `core.coa_main:app`. Prefer the explicit `src.core.coa_main:app` target above when running from the repo root.

### Run the automation/scheduler layer

The automation layer schedules recurring jobs (chief aim reminders, milestone checks) and writes both Mongo and Postgres records.

- Entry point: `src/run_automation.py` (defines `start_scheduler()` and jobs).
- Run the scheduler:
  - `python -m src.run_automation`
  - or `python src/run_automation.py`

This process is long-lived; stop it with Ctrl+C.

### Smoke-test DB integrations

There is no formal test suite in this repo, but there is a simple connectivity check in `src/automation/persistence_test.py` that touches the Postgres engine and Mongo client.

- Run the smoke test:
  - `python -m src.automation.persistence_test`
  - or `python src/automation/persistence_test.py`

### Serve the HTML UI

The `ui/index.html` file is a static "Chairman Console" that POSTs to `http://localhost:8080/route`.

- Start the FastAPI server (see above), then open the UI directly in a browser:
  - `ui/index.html`
- No build step is required; it is plain HTML/JS.

### Linting and tests

- There are no linting tools or test runners configured (no `pytest` config, no lint scripts). If you introduce them, document the commands here.

## High-level architecture

### Core infrastructure (`src/core`)

- `db.py`
  - Central SQLAlchemy setup: `engine`, `SessionLocal`, and declarative `Base`.
  - Reads `POSTGRES_URL` from the environment (via `dotenv`).
- `models.py`
  - Defines three tables:
    - `AuditLog`: audit trail entries (category, action, status, detail JSON/text, timestamp).
    - `KPIRecord`: generic KPI time series (category, metric, value, timestamp).
    - `ChiefAim`: stores a single "Definite Chief Aim" statement plus `last_reviewed_at`.
- `mongo_client.py`
  - Connects to MongoDB using `MONGO_URI`.
  - Exposes a shared `db` handle (`empireof8_ops`) and several collections that other modules import: `ops_events`, `chief_aim`, `tasks`, `alerts`, `agent_state`.
- `policy_engine.py`
  - Small helper that reads `config/policies.json` and decides whether a task should be approved or escalated based on type and amount.
- `logging_setup.py`
  - Sets up process-wide logging to `logs/automation.log` and stdout using a rotating file handler.
  - Called early in `src/run_automation.py` so that automation jobs share consistent logging.
- `coa_main.py`
  - FastAPI application exposing:
    - `GET /`: simple health/info endpoint.
    - `POST /route`: placeholder route that echoes the task and assigns a mock agent.
  - Intended to be served by Uvicorn as `src.core.coa_main:app`.
- `init_db.py`
  - Utility script that imports `Base`/models and runs `Base.metadata.create_all` on the configured `engine`.

### Automation layer (`src/automation` and `src/run_automation.py`)

- `persistence.py`
  - Encapsulates persistence concerns for automation jobs:
    - MongoDB operations: `log_ops_event` (writes operational events), `update_chief_aim_reviewed` (upserts a singleton chief aim doc with `last_reviewed_at`).
    - Postgres operations: `write_audit_log` and `bump_kpi`, both using SQLAlchemy sessions.
  - Relies on `src.core.mongo_client` and `src.core.models`.
- `calendar_connector.py`
  - Manages OAuth and token refresh for the Google Calendar API.
  - Uses `CREDENTIALS_PATH` and `TOKEN_PATH` from the environment; persists refreshed tokens to the token file.
  - Provides `get_calendar_service()` and `add_calendar_event(...)` for higher-level code.
- `events.py`
  - Contains a small `check_milestones()` helper that compares hard-coded target dates with `today` and prints alerts for key intervals.
- `src/run_automation.py`
  - Primary automation entry point combining logging, persistence, and external integrations.
  - Key responsibilities:
    - Initialize logging via `setup_logging()`.
    - Provide a `db_session()` context manager around `SessionLocal`.
    - Define automation jobs:
      - `remind_chief_aim()`: logs a reminder, records an audit log and KPI entry in Postgres, updates the `ChiefAim` review timestamp in Mongo, and writes a Google Calendar event.
      - `check_milestones()`: logs milestone status, records an audit log and KPI entry.
    - Configure and start an `APScheduler` `BackgroundScheduler` with cron triggers in the `Africa/Lusaka` timezone.
    - Keep the process alive in a `while True` loop until interrupted.

### Controllers and entrypoints (`src/controllers`)

- `src/controllers/main.py` imports `start_scheduler` from a non-existent `src.automation.scheduler` module and then keeps the process alive.
- In practice, `src/run_automation.py` appears to be the canonical automation entrypoint; prefer it when wiring automation into other tooling.

### Configuration and policy (`config`)

- `config/policies.json`
  - Simple JSON file with:
    - `spending_limit_zmw`: numeric limit for auto-approval.
    - `auto_execute`: flag for whether tasks can be executed automatically.
    - `approval_required`: list of task types that always require approval.
  - Consumed by `src/core/policy_engine.py`.

### UI console (`ui`)

- `ui/index.html`
  - Minimal HTML/JS page used as a "Chairman Console" for sending free-form tasks to the FastAPI `/route` endpoint.
  - Performs a `fetch` POST to `http://localhost:8080/route` with JSON `{ "task": <textarea contents> }` and renders the JSON response in a `<pre>` block.

## Warp-specific notes

- Many modules depend on external services (Postgres, MongoDB, Google Calendar). When making changes that touch these areas, be conservative about running code that could mutate production data; prefer to work against test instances or mock these dependencies.
- Logs for the automation layer are written to `logs/automation.log` relative to the repo. If you add more automation tasks, reuse the existing logging setup rather than creating new top-level loggers.
- If you add structured tests or linting tools, update the "Common commands" section so future Warp instances know how to run them.