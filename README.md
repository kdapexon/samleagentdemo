
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

## API Documentation

FastAPI automatically generates API documentation. Once the service is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
