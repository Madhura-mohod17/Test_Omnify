from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.database import engine
from model.base import Base
from route import event  



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  


app = FastAPI(
    title="Event Management System",
    description="API for creating events, registering attendees, and viewing attendee lists.\n\n"
    "### Key Features:\n"
    "- Timezone support: Events are created in IST and converted to UTC internally. "
    "You can view event times in any timezone using the `tz` query parameter.\n"
    "- Duplicate check: An attendee cannot register for the same event more than once (based on email).\n"
    "- Capacity limit: Events will not accept more attendees than the defined `max_capacity`.\n"
    "- Pagination support for attendee lists.",
    version="1.0",
    lifespan=lifespan
)


app.include_router(event.router)
