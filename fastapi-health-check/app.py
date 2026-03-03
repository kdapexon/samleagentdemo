from fastapi import FastAPI

app = FastAPI(
    title="Health Check API",
    description="A simple API with health check endpoint",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
