import pytest

@pytest.mark.asyncio
async def test_create_event(async_client):
    response = await async_client.post("/events/", json={
        "name": "Test Event",
        "location": "Bangalore",
        "start_time": "2025-06-21T10:00:00",
        "end_time": "2025-06-21T12:00:00",
        "max_capacity": 5
    })
    assert response.status_code == 200

