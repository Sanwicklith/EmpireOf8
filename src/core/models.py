from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from .db import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(64), index=True)     # e.g. "automation", "calendar"
    action = Column(String(128), index=True)      # e.g. "remind_chief_aim"
    status = Column(String(32), index=True)       # "success" | "error"
    detail = Column(Text)                         # freeform JSON/text
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KPIRecord(Base):
    __tablename__ = "kpi_records"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(64), index=True)     # e.g. "automation"
    metric = Column(String(64), index=True)       # e.g. "jobs_executed"
    value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ChiefAim(Base):
    __tablename__ = "chief_aim"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), default="Definite Chief Aim")
    statement = Column(Text)
    last_reviewed_at = Column(DateTime(timezone=True), nullable=True)
