from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from utils.loginTool import (
    hash_password,
    create_jwt,
    get_current_user,
)
from utils.integrated_crud import IntegratedCRUD


router = APIRouter()
crud = IntegratedCRUD()


@router.post("/user/create")
async def create_user(username: str, password: str):
    try:
        token = create_jwt(username, password)
        await crud.create_user(username, hash_password(password), token)
        return {"code": 200, "message": f"Successfully create user {username}"}
    except Exception as e:
        return {"code": 400, "message": str(e)}


@router.put("/user/top-up")
async def topup_credits(username: str, credits: int):
    try:
        credits = await crud.topup_credits(username, credits)
        return {
            "code": 200,
            "message": f"Successfully top up credits {username}",
            "result": {"remaining_credits": credits},
        }
    except Exception as e:
        return {"code": 400, "message": str(e)}


@router.post("/user/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_id = form_data.username
    hashed_password = hash_password(form_data.password)
    token = await crud.get_token(user_id, hashed_password)
    if token:
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@router.get("/user/credits")
async def read_user_credits(user_id: str = Depends(get_current_user)):
    credits = await crud.get_credits(user_id)
    return {
        "code": 200,
        "message": "Successfully get credits",
        "data": {"user_id": user_id, "credits": credits},
    }


@router.delete("/user/delete")
async def delete_user(user_id):
    try:
        await crud.delete_user_by_id(user_id)
        return {"code": 200, "message": f"Successfully delete user {user_id}"}
    except Exception as e:
        return {"code": 400, "message": str(e)}
