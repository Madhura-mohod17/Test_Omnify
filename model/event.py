from sqlalchemy import Column, Integer, String, DateTime
from model.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)  # timezone-aware
    end_time = Column(DateTime(timezone=True), nullable=False)
    max_capacity = Column(Integer, nullable=False)
