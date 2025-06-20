from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from model.event import Event
from model.attendee import Attendee
from schema.event import EventCreate
from schema.attendee import AttendeeCreate
from fastapi import HTTPException
from pytz import timezone, UTC
from datetime import datetime
from typing import List
import math

# Create event
async def create_event(db: AsyncSession, event_data: EventCreate) -> Event:
    ist = timezone("Asia/Kolkata")

    if event_data.start_time.tzinfo is None:
        event_data.start_time = ist.localize(event_data.start_time)
    event_data.start_time = event_data.start_time.astimezone(UTC)

    if event_data.end_time.tzinfo is None:
        event_data.end_time = ist.localize(event_data.end_time)
    event_data.end_time = event_data.end_time.astimezone(UTC)

    new_event = Event(**event_data.model_dump())
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event



# Get all upcoming events
async def get_upcoming_events(db: AsyncSession) -> List[Event]:
    now = datetime.utcnow()
    result = await db.execute(select(Event).where(Event.start_time > now).order_by(Event.start_time))
    return result.scalars().all()


# Register attendee 
async def register_attendee(db: AsyncSession, event_id: int, data: AttendeeCreate) -> Attendee:
    query = select(Attendee).where(Attendee.email == data.email, Attendee.event_id == event_id)
    if (await db.execute(query)).first():
        raise HTTPException(status_code=400, detail="Attendee already registered for this event.")

    count_query = select(func.count(Attendee.id)).where(Attendee.event_id == event_id)
    attendee_count = (await db.execute(count_query)).scalar()
    event = await db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    if attendee_count >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event is fully booked.")

    attendee = Attendee(**data.model_dump(), event_id=event_id)
    db.add(attendee)
    await db.commit()
    await db.refresh(attendee)
    return attendee


# Get attendees for event 
async def get_attendees_for_event(db, event_id: int, skip: int = 0, limit: int = 10):
    total_query = await db.execute(
        select(func.count()).where(Attendee.event_id == event_id)
    )
    total = total_query.scalar()

    result = await db.execute(
        select(Attendee).where(Attendee.event_id == event_id).offset(skip).limit(limit)
    )
    attendees = result.scalars().all()

    
    current_page = (skip // limit) + 1
    total_pages = math.ceil(total / limit) if total else 1
    record_start = skip + 1 if total > 0 else 0
    record_end = skip + len(attendees)

    return {
        "attendees": attendees,
        "pagination": {
            "total_records": total,
            "total_pages": total_pages,
            "current_page": current_page,
            "records_per_page": limit,  
            "record_start": record_start,
            "record_end": record_end
        }
    }


