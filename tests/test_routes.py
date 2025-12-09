from fastapi.testclient import TestClient


def _get_app_and_module():
    """Import the FastAPI app module under test.

    Imports inside the function so that environment variables provided in
    tests/conftest.py are applied before the first import.
    """
    from src.core import coa_main

    return coa_main.app, coa_main


class _DummyMessage:
    def __init__(self, content: str):
        self.content = content


class _DummyChoice:
    def __init__(self, content: str):
        self.message = _DummyMessage(content)


class _DummyCompletion:
    def __init__(self, content: str):
        self.choices = [_DummyChoice(content)]


def test_route_processes_valid_task_returns_success(monkeypatch):
    app, coa_main = _get_app_and_module()

    def fake_create(**kwargs):  # matches OpenAI client's .create signature
        # Basic sanity checks on how the endpoint calls OpenAI
        assert kwargs["model"] == "gpt-4o-mini"
        assert kwargs["messages"][0]["role"] == "system"
        assert kwargs["messages"][1]["role"] == "user"
        assert kwargs["messages"][1]["content"] == "Schedule a board meeting next week."
        return _DummyCompletion("Here is a test reply from OpenAI.")

    # Patch the OpenAI client used by the endpoint so no real API calls occur.
    monkeypatch.setattr(coa_main.client.chat.completions, "create", fake_create)

    client = TestClient(app)
    response = client.post("/route", json={"task": "Schedule a board meeting next week."})

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["task"] == "Schedule a board meeting next week."
    assert data["agent"] == "COA (OpenAI gpt-4o-mini)"
    assert data["reply"] == "Here is a test reply from OpenAI."


def test_route_handles_openai_errors_gracefully(monkeypatch):
    app, coa_main = _get_app_and_module()

    def fake_create(**kwargs):
        raise RuntimeError("Simulated OpenAI failure")

    monkeypatch.setattr(coa_main.client.chat.completions, "create", fake_create)

    client = TestClient(app)
    response = client.post("/route", json={"task": "Trigger an error."})

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "error"
    assert data["task"] == "Trigger an error."
    assert data["agent"] == "COA (error)"
    assert "Simulated OpenAI failure" in data["error"]


def test_agriculture_route_processes_valid_task_returns_success(monkeypatch):
    app, coa_main = _get_app_and_module()

    def fake_create(**kwargs):
        # Ensure the agriculture route still uses the expected model and passes the task.
        assert kwargs["model"] == "gpt-4o-mini"
        assert kwargs["messages"][0]["role"] == "system"
        assert "AGRICULTURE AGENT" in kwargs["messages"][0]["content"]
        assert kwargs["messages"][1]["role"] == "user"
        assert kwargs["messages"][1]["content"] == "Plan a maize crop rotation." \
            or kwargs["messages"][1]["content"] == "Plan a maize crop rotation."
        return _DummyCompletion("Agriculture advice response.")

    monkeypatch.setattr(coa_main.client.chat.completions, "create", fake_create)

    client = TestClient(app)
    response = client.post("/route/agriculture", json={"task": "Plan a maize crop rotation."})

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["task"] == "Plan a maize crop rotation."
    assert data["agent"] == "Agriculture Agent (OpenAI gpt-4o-mini)"
    assert data["reply"] == "Agriculture advice response."


def test_agriculture_route_handles_openai_errors_gracefully(monkeypatch):
    app, coa_main = _get_app_and_module()

    def fake_create(**kwargs):
        raise RuntimeError("Simulated agriculture OpenAI failure")

    monkeypatch.setattr(coa_main.client.chat.completions, "create", fake_create)

    client = TestClient(app)
    response = client.post("/route/agriculture", json={"task": "Trigger agriculture error."})

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "error"
    assert data["task"] == "Trigger agriculture error."
    assert data["agent"] == "Agriculture Agent (error)"
    assert "Simulated agriculture OpenAI failure" in data["error"]
