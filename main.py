from fastapi import FastAPI, HTTPException
from pydantic import BaseModel #Pydantic's base class that defines a schema(the exact shape of expected JSON data)
from typing import Optional # Optional → parameter can be provided or left empty (None).
import uvicorn

app = FastAPI()
items = []
class Item(BaseModel):
    name: str
    price: float


@app.get("/")
def root():
    return {"message": "WaytoHome"}


class ItemResponse(BaseModel):
     # Defines what the OUTPUT/response should look like.
    # Only fields listed here get sent back to client — others get stripped, regardless of data type.
    name: str


@app.post("/items", response_model=ItemResponse)
# response_model=ItemResponse -> filters whatever create_item() returns,
# keeping ONLY the fields declared in ItemResponse class created above(here: just "name").
# "item" (Item class) has both name+price, but "price" gets removed before sending response bcoz the ItemResponse clss returns only str i.e;name.

def create_item(item: Item):
    items.append(item)
    return item


@app.get("/items")
# Optional query parameter: name=None by default means "no filter"
# Example: GET /items          -> returns all items
# Example: GET /items?name=lap -> returns items whose name contains "lap"
def get_all_items(name: Optional[str] = None):
    if name is None:
        return items
    return [item for item in items if name.lower() in item.name.lower()]

@app.get("/items/total")
# Calculates summary info across all items — a small business-logic feature
# beyond basic CRUD, useful for a "cart total" style use case.
def get_cart_total():
    total_price = sum(item.price for item in items)
    return {"total_items": len(items), "total_price": total_price}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.put("/items/{item_id}", response_model=ItemResponse)
# PUT replaces the ENTIRE item at that index with new data.
# Reuses the same Item model as POST — same validation rules apply.
def update_item(item_id: int, updated_item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = updated_item
    return updated_item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)