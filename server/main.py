from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse
from core.ws_manager import manager
from features.simulation_runner import run_simulation
import asyncio
import os

app = FastAPI(title="CAMEL-AI Cyber Simulation Server")

@app.get("/", response_class=HTMLResponse)
async def root():
    # Serve the dashboard directly from the root
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r") as f:
        return f.read()

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Just keep the connection open, we broadcast from the simulation side
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/simulation/start")
async def start_simulation(background_tasks: BackgroundTasks):
    """
    Triggers the full Red Team vs Blue Team simulation loop as a background task.
    """
    background_tasks.add_task(run_simulation, provider="azure", use_ws=True)
    return {"status": "Simulation started", "channel": "/ws/logs"}

@app.post("/analysis/scan")
async def start_scan(background_tasks: BackgroundTasks):
    """
    Triggers just the Researcher and Auditor scan.
    """
    # For now, we'll just run a partial simulation or a dedicated scan function
    # background_tasks.add_task(run_scan, provider="azure", use_ws=True)
    return {"status": "Scan started (Partial simulation)", "channel": "/ws/logs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
