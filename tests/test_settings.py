import importlib


def test_settings_loads_env_vars_in_development(monkeypatch):
    """ENVIRONMENT != 'production' should call load_dotenv and read env vars.

    We don't rely on a real .env file here; instead we patch load_dotenv to
    flip a flag and assert that flag after reloading the module.
    """
    # Ensure the environment simulates a development setup.
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.setenv("POSTGRES_URL", "postgresql://dev_user:dev_pass@localhost:5432/dev_db")
    monkeypatch.setenv("MONGO_URI", "mongodb://localhost:27017/dev_db")

    # Import inside the test so we can safely reload with the patched function.
    import src.core.settings as settings

    called = {"value": False}

    def fake_load_dotenv():
        called["value"] = True

    # Patch the load_dotenv symbol used inside src.core.settings.
    monkeypatch.setattr(settings, "load_dotenv", fake_load_dotenv, raising=True)

    # Re-run the module code under the patched function and test env.
    reloaded = importlib.reload(settings)

    assert reloaded.ENVIRONMENT == "development"
    assert reloaded.POSTGRES_URL == "postgresql://dev_user:dev_pass@localhost:5432/dev_db"
    assert reloaded.MONGO_URI == "mongodb://localhost:27017/dev_db"
    # In non-production we expect load_dotenv to be called.
    assert called["value"] is True


def test_settings_skips_dotenv_in_production(monkeypatch):
    """ENVIRONMENT == 'production' should *not* call load_dotenv.

    We patch load_dotenv to raise if called so the test would fail in that
    case, and then reload the module under a production-like environment.
    """
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("POSTGRES_URL", "postgresql://prod_user:prod_pass@db:5432/prod_db")
    monkeypatch.setenv("MONGO_URI", "mongodb://mongo:27017/prod_db")

    import src.core.settings as settings

    def bad_load_dotenv():  # pragma: no cover - only hit on failure
        raise AssertionError("load_dotenv should not be called in production")

    monkeypatch.setattr(settings, "load_dotenv", bad_load_dotenv, raising=True)

    reloaded = importlib.reload(settings)

    assert reloaded.ENVIRONMENT == "production"
    # Even in production, the module should still expose the env-derived URLs.
    assert reloaded.POSTGRES_URL == "postgresql://prod_user:prod_pass@db:5432/prod_db"
    assert reloaded.MONGO_URI == "mongodb://mongo:27017/prod_db"
