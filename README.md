# Mini Inventory & Cart API — FastAPI

A small REST API built with **FastAPI** to practice core backend concepts: routing, request validation, response filtering, and auto-generated API documentation. Simulates a basic "cart" system — add items, search them, update them, and calculate a live total.

---

## Features

- Create items (`POST`)
- View all items, with optional search by name (`GET`)
- View a single item by ID (`GET`)
- Update an existing item (`PUT`)
- Calculate live cart total — item count + total price (`GET`)
- Input validation and clean error handling (404, 422) — no raw server crashes
- Auto-generated interactive API docs via Swagger UI (`/docs`)

---

## Tech Stack

- **Python 3**
- **FastAPI** — web framework
- **Pydantic** — data validation and schema definition
- **Uvicorn** — ASGI server to run the app

---

## Project Structure

```
├── main.py       # All API routes and logic
└── README.md     # This file
```

---

## API Endpoints

| Method | Endpoint            | Description                              |
|--------|----------------------|-------------------------------------------|
| GET    | `/`                  | Health check / welcome message            |
| POST   | `/items`             | Add a new item (name, price)              |
| GET    | `/items`             | Get all items, or search via `?name=`     |
| GET    | `/items/total`       | Get total item count and total price      |
| GET    | `/items/{item_id}`   | Get a single item by its ID               |
| PUT    | `/items/{item_id}`   | Update an existing item by its ID         |

---

## How to Run Locally

```bash
pip install fastapi uvicorn
python main.py
```

Server runs at: `http://127.0.0.1:8000`
Interactive docs available at: `http://127.0.0.1:8000/docs`

---

## How I Built and Tested This (walkthrough for revision)

This section is written the way I'd explain the project out loud — in the order I actually built and tested it.

### 1. Basic setup and root route
Started with a simple FastAPI app and one `GET /` route to confirm the server runs and responds. This is the "hello world" checkpoint before adding real logic.

### 2. POST route — creating items
Built `POST /items` to accept a JSON body (`name`, `price`) using a **Pydantic model** (`Item`). This is where I learned Pydantic auto-validates incoming data — if `price` isn't a valid number, the request is rejected automatically with a `422` error, before my function code even runs.

I also added a **response model** (`ItemResponse`) here, so the API only returns the `name` field back to the client, even though `price` is stored internally. This taught me that response filtering works by field *name*, not by data type.

### 3. GET route with path parameter — fetch by ID
Built `GET /items/{item_id}` to fetch one specific item using its position in the list. Added manual bounds checking with `HTTPException(status_code=404)` so an invalid ID returns a clean error instead of crashing the server with a `500`.

### 4. GET all items + search
Extended this into `GET /items`, which returns everything by default, or filters results using an optional query parameter (`?name=`). This is where I learned the difference between **path parameters** (part of the URL, like `/items/3`) and **query parameters** (`?key=value` after the URL).

### 5. PUT route — updating items
Built `PUT /items/{item_id}` to replace an existing item's data, reusing the same `Item` model and validation rules as the POST route. This completed a basic CRUD flow: Create, Read (single + all + search), Update.

### 6. Cart total — a custom feature beyond the tutorial
Added `GET /items/total`, which calculates the total number of items and their combined price using Python's `sum()`. This was the moment the project stopped being "just CRUD routes" and started doing actual computation on stored data — the part I'd highlight most in an interview.

One real bug I hit and fixed here: I initially placed this route *after* `/items/{item_id}` in the code, which broke it — FastAPI tried to convert the word `"total"` into an integer `item_id` and failed. Moving it *above* that route fixed it. Good lesson on route ordering in FastAPI.

### 7. Testing everything through Swagger UI (`/docs`)
Rather than only using `curl`, I tested the full flow through FastAPI's auto-generated `/docs` page:
- Added 3–4 items through `POST /items`
- Viewed them all through `GET /items`
- Searched using the `name` query field
- Updated one item's price through `PUT /items/{item_id}`
- Verified the change reflected correctly in `GET /items/total`

Along the way, I hit and fixed two realistic bugs:
- Sent `"Price"` (capital P) instead of `"price"` — learned that **JSON keys are case-sensitive** and must match the Pydantic model exactly.
- Forgot to overwrite Swagger's default placeholder values (`"string"`, `0`) before executing — learned to always check the actual request body being sent, not just assume the form is ready.

---

## Key Concepts Practiced

- REST principles: resource-based routes, correct use of GET/POST/PUT
- Request validation using Pydantic models
- Response shaping using `response_model`
- Path parameters vs query parameters
- Proper HTTP error handling (404, 422) instead of raw server errors
- Debugging real issues: stale server state, field name casing, route ordering, default placeholder values

---

## Next Steps (planned improvements)

- Add a `DELETE /items/{item_id}` route to complete full CRUD
- Persist data using a real database (SQLite) instead of an in-memory list
- Add basic authentication for protected routes
- Write automated tests using `pytest` and FastAPI's `TestClient`