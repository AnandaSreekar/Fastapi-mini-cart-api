# FastAPI Learning Notes — REST API Basics

I built a small REST API using FastAPI — it's a mini cart/inventory system. I implemented routes to add items, fetch all items or a single item, update an item, search by name, and calculate a live cart total. I used Pydantic for data validation, so bad requests get automatically rejected, and response models to control exactly what data gets sent back to the client. I tested everything using FastAPI's built-in Swagger UI
from  the above para:
how do u used  pydantic and wt rspone models u used means wt to sayy:
I used Pydantic to define an Item model with name and price fields — it auto-validates incoming data, so bad requests get rejected before my code even runs. I also used a separate ItemResponse model with just name, attached via response_model, so even though I store the full item internally, only name gets sent back to the client
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



Built while following a FastAPI tutorial, extended with custom routes for practice.

---

## Step 1: Basic App Setup

```python
from fastapi import FastAPI
app = FastAPI()
```
`app` is the object every route attaches to.

```python
items = []
```
Simple in-memory list acting as a fake database — data resets on every server restart.

---

## Step 2: GET and POST Routes

```python
@app.get("/")
def root():
    return {"message": "WaytoHome"}
```
`@app.get("/")` — runs this function when someone visits `/` with a GET request. Returns a dict, auto-converted to JSON.

```python
@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items
```
Early version — `item: str` with no path pattern (`{item}`) and no Pydantic model means FastAPI treats it as a **query parameter** (`?item=apple`), not a JSON body.

**Type hints = automatic validation.** `item: str` isn't just a hint — FastAPI uses it to reject bad data automatically, no extra code needed.

---

## Step 3: Path Parameters + Error Handling

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```
- `{item_id}` in the URL = **path parameter** — captured into the function
- `item_id: int` — auto-converted from URL text to integer, rejected if invalid
- `HTTPException(status_code=404, ...)` — returns a clean 404 error instead of crashing with a raw 500

**Key lesson learned:** if you're running the server with `python main.py` (not `uvicorn --reload`), you MUST manually stop (`Ctrl+C`) and restart after every code change — otherwise you're testing stale code and get confusing errors.

---

## Step 4: JSON Request Body (Pydantic)

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
```
`BaseModel` defines a **schema** — the exact shape of expected JSON. If `price` isn't a valid number, FastAPI auto-rejects the request with a `422 Validation Error` before your function even runs.

```python
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return item
```
Changing `item: str` → `item: Item` switches FastAPI from expecting a query param to expecting a **JSON body**.

---

## Step 5: Response Models

```python
class ItemResponse(BaseModel):
    name: str
```
```python
@app.post("/items", response_model=ItemResponse)
def create_item(item: Item):
    items.append(item)
    return item
```
**Response Model = filters by field NAME, not data type.** Only fields declared in `ItemResponse` survive in the output. Even though `item` has `price` too, it gets silently stripped because `ItemResponse` never mentions it. Useful for hiding internal fields (e.g. cost price, internal flags) from the public response.

---

## Step 6: Interactive Docs (`/docs`)

No code needed — FastAPI auto-builds a testing page (Swagger UI) from your routes + Pydantic models.

**What's on the page:**
- **Request body** — the JSON box to edit and send
- **Schema** — just the field types, no need to fill real values
- **Execute** — sends a real request, same as curl, and shows you the exact curl command it used
- **Server response** — the LIVE result of your last Execute (status code + response body + headers)
- **Responses section** — DOCUMENTATION of all possible outcomes (e.g. `200` success shape, `422` validation error shape) — shown in advance, not live, until you trigger them

**Confirmed working:** sending `price` as a string (`"cheap"`) correctly triggers a live `422 Validation Error`, proving Pydantic's automatic validation.

---

## FastAPI vs Flask (concept only, no code)

| | FastAPI | Flask |
|---|---|---|
| Async support | Built-in | Needs extra setup |
| Data validation | Automatic (Pydantic) | Manual / extra libraries |
| Auto docs (`/docs`) | Built-in, free | Needs extra library |
| Speed | Faster | Slower (sync by default) |
| Best for | Modern APIs, microservices | Simple apps, quick prototypes |

**Interview line:** "FastAPI is async by default, auto-validates data using Pydantic, and auto-generates interactive docs — all things Flask needs extra libraries for. Flask is simpler with a gentler learning curve, but FastAPI is generally preferred for modern, high-performance APIs."

---

## Extensions added beyond the tutorial (for practice)

- **`GET /items`** — returns all items, with an optional `?name=` query param to search/filter by partial name match
- **`PUT /items/{item_id}`** — updates an existing item at a given index, reusing the same `Item` model and validation as POST

These complete a basic CRUD pattern: Create (POST), Read (GET one / GET all / search), Update (PUT) — Delete intentionally left out for now as a next practice step.

---

## Full working code

See `main.py` in this repo.
