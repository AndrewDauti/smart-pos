import hmac
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class Login(BaseModel):
    username: str
    password: str


def _matches(given: str, expected: str) -> bool:
    given_bytes = given.encode()
    expected_bytes = expected.encode()
    if len(given_bytes) != len(expected_bytes):
        return False
    return hmac.compare_digest(given_bytes, expected_bytes)


@router.post("/login")
def login(body: Login):
    username = os.getenv("POS_USERNAME", "cashier")
    password = os.getenv("POS_PASSWORD", "mpepo")
    if not (_matches(body.username.strip(), username) and _matches(body.password, password)):
        raise HTTPException(status_code=401, detail="Invalid staff credentials")
    return {"access_token": "demo-token", "token_type": "bearer", "username": username}
