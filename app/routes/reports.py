from fastapi import APIRouter
import json
from app.redis_client import r

router = APIRouter()

# Simulated DB fetch function
def fetch_shifts_from_db(manager_id: int, week_id: str):
    print("Fetching from DB...")
    return [
        {"employee": "Alice", "day": "Mon", "shift": "9-5"},
        {"employee": "Bob", "day": "Tue", "shift": "10-6"},
    ]

@router.get("/shifts/{manager_id}/{week_id}")
def get_shifts(manager_id: int, week_id: str):
    redis_key = f"shifts:manager:{manager_id}:week:{week_id}"
    cached = r.get(redis_key)

    if cached:
        print("Returning from Redis cache")
        return json.loads(cached)

    # Fallback to "DB"
    shift_data = fetch_shifts_from_db(manager_id, week_id)

    # Cache the data
    r.set(redis_key, json.dumps(shift_data))
    r.expire(redis_key, 1800)  # 30 minutes TTL

    return shift_data
