from fastapi import APIRouter, HTTPException
from target_app.models.schemas import UserSchema, AuthRequest
from target_app.db.mock_db import get_user_by_id, DATABASE
import logging

router = APIRouter()

# Configure logging to write to target_app.log
logger = logging.getLogger("TargetAPI")
logger.setLevel(logging.INFO)
if not logger.handlers:
    file_handler = logging.FileHandler("target_app.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(user_id: int):
    logger.info(f"User profile access attempt for ID: {user_id}")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/auth")
async def login(auth: AuthRequest):
    logger.info(f"Login attempt for user: {auth.username}")
    # Insecure logic: checking against hardcoded password in DB config
    if auth.username == "admin" and auth.password == DATABASE["config"]["DB_ADMIN_PASS"]:
        logger.warning(f"SECURITY ALERT: Successful admin login from untrusted source!")
        return {"session": "ADMIN_LOGGED_IN_XYZ"}
    
    logger.error(f"Failed login for {auth.username}")
    raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/debug/config")
async def get_debug_config():
    logger.warning("SENSITIVE DATA EXPOSURE: /debug/config accessed.")
    # EXTREMELY INSECURE: Exposing internal config via endpoint
    return DATABASE["config"]
