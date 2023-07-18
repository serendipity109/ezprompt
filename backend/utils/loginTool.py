import hashlib
import jwt
import time
import logging
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()[:10]


def encode(payload: dict):
    token = jwt.encode(payload, key="123", algorithm="HS256")
    return token


def decode(token: str):
    try:
        payload = jwt.decode(token, key="123", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")  # 捕获token过期异常
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")  # 捕获无效token异常


def create_jwt(user_id: str, password: str):
    payload = {
        "user_id": user_id,
        "password": hash_password(password),
        "exp": time.time() + 365.25 * 24 * 60 * 60,  # 一年後 token 過期
    }
    token = jwt.encode(payload, key="123", algorithm="HS256")
    return token


def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, key="123", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")  # 捕获token过期异常
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")  # 捕获无效token异常


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = verify_jwt(token)
        return payload["user_id"]
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
