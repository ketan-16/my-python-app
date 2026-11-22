from fastapi import FastAPI, HTTPException, status

from app.models import Item, ItemCreate

app = FastAPI(title="My Python App", version="0.1.0")

# In-memory store; swap for a real database later.
_items: dict[int, Item] = {}
_next_id = 1


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items", response_model=list[Item])
def list_items(page: int = 1, page_size: int = 10) -> list[Item]:
    """Return one page of items. Pages are numbered from 1."""
    items = list(_items.values())
    start = page * page_size
    return items[start : start + page_size]


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
