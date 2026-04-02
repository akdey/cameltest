from fastapi import WebSocket
from typing import List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """
        Broadcasts a JSON message to all connected clients.
        Example message: {"agent": "Researcher", "content": "Found CVE...", "type": "thought"}
        """
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                # Handle disconnected clients gracefully
                pass

# Global instance
manager = ConnectionManager()
