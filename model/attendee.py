from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from model.base import Base

class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    __table_args__ = (UniqueConstraint("email", "event_id", name="uix_email_event"),)
