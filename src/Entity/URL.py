from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, String
from src.Database.Database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    target_url = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, index=True)
    is_active = Column(Boolean, default=True)
    clicks = Column(Integer, default=0)


