from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import redis
import json

app = FastAPI()

r=redis.Redis(host='localhost',port=6379,decode_responses=True)

class Item(BaseModel):
    title: str = Field(..., min_length=3, description="Title must be at least 3 characters")
    description: str


@app.post("/items")
def create_item(item: Item):
    item_id = r.incr("item_id")  # auto-increment ID
    r.set(f"item:{item_id}", item.json())  # store item as JSON string
    return {"message": "Item created", "id": item_id, "item": item}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item_data = r.get(f"item:{item_id}")
    if item_data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": json.loads(item_data)}

@app.get("/items")
def get_all_items():
    keys = r.keys("item:*")
    items = []

    for key in keys:
        data = r.get(key)
        if data:
            item = json.loads(data)
            item['id'] = key.split(":")[1]  
            items.append(item)

    return {"items": items}