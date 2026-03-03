# FastAPI Health Check Service

A simple FastAPI application that provides a health check endpoint for monitoring service status.

## Features

- RESTful health check endpoint
- FastAPI-powered async API
- OpenAPI/Swagger documentation
- Production-ready ASGI server configuration

## Requirements

Python 3.7+ and the following packages:
- fastapi (v0.109.0)
- uvicorn (v0.27.0)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-health-check
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Start the server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The service will be available at:
- Health Check endpoint: http://localhost:8000/health
- API Documentation: http://localhost:8000/docs

## API Documentation

### Health Check Endpoint

```
GET /health
```

Returns the health status of the service.

Response example:
```json
{
    "status": "healthy"
}
```

## Development

The API is configured with:
- Title: "Health Check API"
- Description: "A simple API with health check endpoint"
- Version: "1.0.0"

For development with auto-reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
