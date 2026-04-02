from fastapi import FastAPI
from target_app.api.endpoints import router
import uvicorn
import logging

logging.basicConfig(
    filename='target_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Vulnerable Target App")

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Human Resources Portal", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
