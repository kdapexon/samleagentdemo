
# FastAPI Service

A simple web service built with FastAPI providing basic endpoints including health checks.

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

Start the service locally:
```bash
uvicorn main:app --reload
```

The service will be available at http://localhost:8000

## Available Endpoints

- `/`: Root endpoint, returns "Hello World" message
- `/health`: Health check endpoint, returns service status
- `GET /bookmarks`: Returns a list of all bookmarks
- `POST /bookmark`: Creates a new bookmark
- `GET /bookmark/{bookmark_id}`: Retrieves a specific bookmark by ID
- `DELETE /bookmark/{bookmark_id}`: Deletes a specific bookmark by ID

### GET /bookmarks

Returns a list of all bookmarks with their details.

**Response:**
```json
{
  "success": true,
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
```

### POST /bookmark

Creates a new bookmark entry.

**Request Body:**
```json
{
  "country": "Spain",
  "status": "active"
}
```

**Validation Rules:**
- `country`: Must be 1-100 characters, contain only letters, spaces, and hyphens, and start with an uppercase letter
- `status`: Must be one of: "active", "archived", or "pending"

**Response:**
```json
{
  "success": true,
  "message": "Bookmark created successfully",
  "data": [
    {
      "id": 6,
      "country": "Spain",
      "status": "active",
      "timestamp": "2026-03-05T10:30:00"
    }
  ],
  "metadata": {
    "total": 6,
    "page": 1,
    "per_page": 1
  }
}
```

### GET /bookmark/{bookmark_id}

Retrieves a specific bookmark by its ID.

**Parameters:**
- `bookmark_id` (path): Integer ID of the bookmark (must be positive)

**Response:**
```json
{
  "success": true,
  "message": "Bookmark retrieved successfully",
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
    "per_page": 1
  }
}
```

**Error Responses:**
- `400`: Invalid bookmark ID (must be positive integer)
- `404`: Bookmark not found

### DELETE /bookmark/{bookmark_id}

Deletes a specific bookmark by its ID.

**Parameters:**
- `bookmark_id` (path): Integer ID of the bookmark to delete (must be positive)

**Response:**
```json
{
  "status": "success",
  "message": "Bookmark with ID 1 deleted successfully",
  "deleted_bookmark": {
    "id": 1,
    "country": "Japan",
    "status": "active",
    "timestamp": "2026-02-15T14:30:00"
  }
}
```

**Error Responses:**
- `400`: Invalid bookmark ID (must be positive integer)
- `404`: Bookmark not found

## API Documentation

FastAPI automatically generates API documentation. Once the service is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
