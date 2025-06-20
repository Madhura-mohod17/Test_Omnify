from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from crud.event import (
    create_event, 
    get_upcoming_events, 
    register_attendee, 
    get_attendees_for_event
)
from schema.event import EventCreate, EventOut
from schema.attendee import AttendeeCreate, AttendeeOut, PaginationResponse, PaginatedAttendeeResponse
from typing import List
from pytz import timezone

router = APIRouter(prefix="/events", tags=["Events"])

# 1. Create Event
@router.post("/", response_model=EventOut, summary="Create a new event", description="Creates an event with a name, location, start/end time (in IST, e.g., use '+05:30' for timezone), and max capacity.")
async def create_event_handler(
    event: EventCreate = Body(...),
    db: AsyncSession = Depends(get_session)
):
    if event.start_time >= event.end_time:
        raise HTTPException(status_code=400, detail="Start time must be before end time.")
    return await create_event(db, event)



# 2. Get All Upcoming Events
@router.get("/", response_model=List[EventOut], summary="List all upcoming events")
async def get_events(db: AsyncSession = Depends(get_session), tz: str = Query(default="Asia/Kolkata"), description="Timezone in which to view the event timings"):
    events = await get_upcoming_events(db)
    try:
        tz_obj = timezone(tz)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timezone")
    
    for e in events:
        e.start_time = e.start_time.astimezone(tz_obj)
        e.end_time = e.end_time.astimezone(tz_obj)
    return events



# 3. Register Attendee
@router.post("/{event_id}/register", response_model=AttendeeOut, summary="Register an attendee")
async def register(event_id: int, attendee: AttendeeCreate = Body(..., description="Attendee's name and email"), db: AsyncSession = Depends(get_session)):
    return await register_attendee(db, event_id, attendee)


# 4. Get Attendees
@router.get("/{event_id}/attendees", response_model=PaginatedAttendeeResponse, summary="List all attendees for an event")
async def get_attendees(
    event_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),      
    limit: int = Query(10, ge=1, description="Number of records to return"),    
    db: AsyncSession = Depends(get_session)
):
    return await get_attendees_for_event(db, event_id, skip, limit)