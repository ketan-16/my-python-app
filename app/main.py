from fastapi import FastAPI, HTTPException, status

from app import db
from app.models import Item, ItemCreate

app = FastAPI(title="My Python App", version="0.1.0")

# In-memory store; swap for a real database later.
_items: dict[int, Item] = {}
_next_id = 1


@app.on_event("startup")
def startup():
    db.init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items", response_model=list[Item])
def list_items() -> list[Item]:
    return list(_items.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> Item:
    global _next_id
    item = Item(id=_next_id, **payload.model_dump())
    _items[item.id] = item
    _next_id += 1
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if _items.pop(item_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.get("/users")
def search_users(name: str = ""):
    rows = db.find_users(name)
    return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]


@app.post("/users")
def create_user(name: str, email: str):
    db.add_user(name, email)
    return {"ok": True}
