
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
- `/bookmarks`: Returns a list of bookmarks with their status

### Bookmarks Endpoint

The `/bookmarks` endpoint returns a JSON array of bookmark objects. Each bookmark contains:
- `url`: The bookmarked URL
- `title`: Title of the bookmark
- `status`: Current status (e.g., "active", "archived")
- `created_at`: Timestamp of when the bookmark was created

Example response:
```json
[
  {
    "url": "https://example.com",
    "title": "Example Site",
    "status": "active",
    "created_at": "2026-03-01T10:00:00Z"
  }
]
```

## API Documentation

FastAPI automatically generates API documentation. Once the service is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
