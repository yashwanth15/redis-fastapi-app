from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.redis_client import r

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserOut(UserCreate):
    id: int

@router.post("/", response_model=UserOut, status_code=201)
def create_user(user: UserCreate):
    # Generate a new user ID
    new_id = r.incr("user:id:counter")
    redis_key = f"user:{new_id}"

    # Save user details
    r.hset(redis_key, mapping=user.model_dump())

    # Save the ID to a set for tracking (for list endpoint later)
    r.sadd("users", new_id)
    print(f"Added user_id {new_id} to Redis set 'users'")

    return {**user.model_dump(), "id": new_id}


@router.get("/users/{id}", response_model=UserOut)
def get_user(id: int):
    user = r.hgetall(f"user:{id}")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Convert byte keys/values to strings
    user_data = {k.decode(): v.decode() for k, v in user.items()}
    
    # Add the `id` explicitly into the returned dict
    return {"id": id, **user_data}

@router.get("/users")
def list_users():
    user_ids = r.smembers("users")
    return [int(uid.decode()) for uid in user_ids]

@router.delete("/users/{id}")
def delete_user(id: int):
    deleted = r.delete(f"user:{id}")
    r.srem("users", id)  # Remove ID from user set
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {id} deleted"}