from sqlalchemy.ext.declarative import declarative_base, declared_attr
from airflow import settings

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    PickleType,
    Index,
    Float,
)

Base = declarative_base()


class ResetDagAudit(Base):
    __tablename__ = "aerofoil_reset_dag"
    id = Column(Integer, primary_key=True)
    dag_id = Column(Integer, index=True, nullable=False)
    reset_type = Column(String(20), nullable=False)
    reset_by = Column(String(64), nullable=False)
    reset_date = Column(DateTime, nullable=True, index=True)
    reset_reason = Column(String(500), nullable=False)
