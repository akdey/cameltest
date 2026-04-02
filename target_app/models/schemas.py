from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    username: str
    role: str

class AuthRequest(BaseModel):
    username: str
    password: str
