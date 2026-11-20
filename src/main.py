from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Not in use, docstring for satisfying linter."""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Not in use, docstring for satisfying linter."""
    return {"item_id": item_id, "q": q}
