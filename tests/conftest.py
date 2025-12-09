import os

# Ensure required environment variables exist before application modules import.
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("POSTGRES_URL", "postgresql://user:pass@localhost:5432/testdb")
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/testdb")
os.environ.setdefault("OPENAI_API_KEY", "test-openai-key")
