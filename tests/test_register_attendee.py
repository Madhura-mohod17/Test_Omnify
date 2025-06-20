import pytest

@pytest.mark.asyncio
async def test_register_attendee(async_client):
   
    event_resp = await async_client.post("/events/", json={  
        "name": "Workshop",
        "location": "Bangalore",
        "start_time": "2025-06-22T10:00:00",
        "end_time": "2025-06-22T12:00:00",
        "max_capacity": 1
    })
    assert event_resp.status_code == 200, event_resp.text
    event_id = event_resp.json()["id"]

    
    register_resp = await async_client.post(f"/events/{event_id}/register", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert register_resp.status_code == 200

    
    duplicate_resp = await async_client.post(f"/events/{event_id}/register", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert duplicate_resp.status_code == 400

    
    overbook_resp = await async_client.post(f"/events/{event_id}/register", json={
        "name": "Jane",
        "email": "jane@example.com"
    })
    assert overbook_resp.status_code == 400
