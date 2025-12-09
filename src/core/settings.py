import os
from dotenv import load_dotenv

# ENVIRONMENT controls whether we load .env or rely purely on real env vars.
# In production, set ENVIRONMENT=production and inject secrets via the process
# manager / cloud platform rather than a .env file.
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

if ENVIRONMENT != "production":
    # Local/dev: load variables from a .env file in the project root if present.
    # This is a no-op in production where ENVIRONMENT=production.
    load_dotenv()

# Required settings. These will raise KeyError at startup if missing,
# which is preferable to a half-configured production app.
POSTGRES_URL = os.environ["POSTGRES_URL"]
MONGO_URI = os.environ["MONGO_URI"]

# Optional: OpenAI client reads OPENAI_API_KEY directly from the environment.
# We don't access it here, but we document it so the contract is clear.
#   OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
