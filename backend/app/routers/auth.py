from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os

router = APIRouter(prefix="/auth", tags=["auth"])

class Login(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(_: Login):
    # Simple demo token; replace with JWT if needed
    return {"access_token": "demo-token", "token_type": "bearer"}
