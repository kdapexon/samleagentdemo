from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel, Field, constr, validator
import re
from typing import List

# Pydantic models for response schema
class Bookmark(BaseModel):
    id: int = Field(..., description="Unique identifier for the bookmark")
    country: str = Field(..., description="Country name")
    status: str = Field(..., description="Current status of the bookmark (active, archived, or pending)")
    timestamp: str = Field(..., description="ISO format timestamp of the bookmark creation")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "country": "Japan",
                "status": "active",
                "timestamp": "2026-02-15T14:30:00"
            }
        }

class BookmarkResponse(BaseModel):
    success: bool = Field(default=True, description="Indicates if the request was successful")
    message: str = Field(default="Bookmarks retrieved successfully", description="Response message")
    data: List[Bookmark] = Field(..., description="List of bookmarks")
    metadata: dict = Field(
        default_factory=lambda: {"total": 0, "page": 1, "per_page": 10},
        description="Metadata about the response"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Bookmarks retrieved successfully",
                "data": [
                    {
                        "id": 1,
                        "country": "Japan",
                        "status": "active",
                        "timestamp": "2026-02-15T14:30:00"
                    }
                ],
                "metadata": {
                    "total": 1,
                    "page": 1,
                    "per_page": 10
                }
            }
        }

# Request model for creating bookmarks
class BookmarkCreate(BaseModel):
    country: constr(min_length=1, max_length=100) = Field(..., description="Country name")
    status: constr(regex="^(active|archived|pending)$") = Field(..., description="Status of the bookmark")

    @validator('country')
    def validate_country(cls, v):
        if not re.match(r'^[A-Za-z\s\-]+$', v):
            raise ValueError('Country name must contain only letters, spaces, and hyphens')
        if not v[0].isupper():
            raise ValueError('Country name must start with an uppercase letter')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "country": "Spain",
                "status": "active"
            }
        }

def get_next_id():
    """Generate the next bookmark ID"""
    return max([b["id"] for b in bookmarks], default=0) + 1

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
    return {
        "success": True,
        "message": "Bookmarks retrieved successfully",
        "data": bookmarks,
        "metadata": {
            "total": len(bookmarks),
            "page": 1,
            "per_page": 10
        }
    }

@app.post("/bookmark", response_model=BookmarkResponse)
async def create_bookmark(bookmark: BookmarkCreate):
    # Check if country already exists
    if any(b["country"] == bookmark.country for b in bookmarks):
        raise HTTPException(
            status_code=400,
            detail=f"Bookmark for country '{bookmark.country}' already exists"
        )
    new_bookmark = {
        "id": get_next_id(),
        "country": bookmark.country,
        "status": bookmark.status,
        "timestamp": datetime.now().isoformat()
    }
    bookmarks.append(new_bookmark)

    return {
        "success": True,
        "message": "Bookmark created successfully",
        "data": [new_bookmark],
        "metadata": {
            "total": len(bookmarks),
            "page": 1,
            "per_page": 1
        }
    }

@app.get("/bookmark/{bookmark_id}")
async def get_bookmark(bookmark_id: int):
    # Validate bookmark ID
    if bookmark_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Bookmark ID must be a positive integer"
        )

    # Find the bookmark with the given ID
    bookmark = next((b for b in bookmarks if b["id"] == bookmark_id), None)

    if bookmark is None:
        raise HTTPException(
            status_code=404,
            detail=f"Bookmark with ID {bookmark_id} not found"
        )

    return {
        "success": True,
        "message": "Bookmark retrieved successfully",
        "data": [bookmark],
        "metadata": {
            "total": 1,
            "page": 1,
            "per_page": 1
        }
    }

@app.delete("/bookmark/{bookmark_id}")
async def delete_bookmark(bookmark_id: int):
    # Validate bookmark ID
    if bookmark_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Bookmark ID must be a positive integer"
        )

    # Find the bookmark with the given ID
    bookmark_index = next((i for i, b in enumerate(bookmarks) if b["id"] == bookmark_id), None)

    if bookmark_index is None:
        raise HTTPException(
            status_code=404,
            detail=f"Bookmark with ID {bookmark_id} not found"
        )

    # Remove the bookmark from the list
    deleted_bookmark = bookmarks.pop(bookmark_index)

    return {
        "status": "success",
        "message": f"Bookmark with ID {bookmark_id} deleted successfully",
        "deleted_bookmark": deleted_bookmark
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
