from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import os

app = FastAPI(
    title="Service 1",
    description="Service 1 API",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "items",
            "description": "Operations with items",
        },
    ],
    root_path="/service1"
)

class Item(BaseModel):
    name: str
    description: str = None

items = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to Service 1", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/items", tags=["items"])
def get_items():
    return items

@app.get("/items/{item_id}", tags=["items"])
def get_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items", tags=["items"])
def create_item(item: Item):
    item_id = str(len(items) + 1)
    items[item_id] = item
    return {"item_id": item_id, "item": item}

# Add this to make OpenAPI docs work behind a proxy
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return app.openapi()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 