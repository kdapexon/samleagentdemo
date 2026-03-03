from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from typing import List

# Pydantic models for response schema
class Bookmark(BaseModel):
    id: int
    country: str
    status: str
    timestamp: str

class BookmarkResponse(BaseModel):
    data: List[Bookmark]

# Mock data for bookmarks
bookmarks = [
    {
        "id": 1,
        "country": "Japan",
        "status": "active",
        "timestamp": datetime(2026, 2, 15, 14, 30, 0).isoformat()
    },
    {
        "id": 2,
        "country": "France",
        "status": "archived",
        "timestamp": datetime(2026, 2, 20, 9, 15, 0).isoformat()
    },
    {
        "id": 3,
        "country": "Brazil",
        "status": "active",
        "timestamp": datetime(2026, 2, 25, 18, 45, 0).isoformat()
    },
    {
        "id": 4,
        "country": "Canada",
        "status": "active",
        "timestamp": datetime(2026, 3, 1, 11, 0, 0).isoformat()
    },
    {
        "id": 5,
        "country": "Australia",
        "status": "pending",
        "timestamp": datetime(2026, 3, 2, 16, 20, 0).isoformat()
    }
]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/bookmarks", response_model=BookmarkResponse)
async def get_bookmarks():
    return {"data": bookmarks}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
