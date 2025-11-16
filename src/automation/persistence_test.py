from src.core.db import engine
from src.core.mongo_client import db

print("Postgres Engine:", engine)
print("Mongo Collections:", db.list_collection_names())
