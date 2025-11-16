from .db import Base, engine
from .models import AuditLog, KPIRecord, ChiefAim

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Postgres tables created successfully.")

