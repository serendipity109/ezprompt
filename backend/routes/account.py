from typing import Annotated
import os

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from utils.loginTool import hash_password, create_jwt, get_current_user, encode, decode
from utils.integrated_crud import IntegratedCRUD
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from dotenv import load_dotenv


router = APIRouter()

load_dotenv()
OWN_EMAIL = os.getenv("OWN_EMAIL")
OWN_EMAIL_PASSWORD = os.getenv("OWN_EMAIL_PASSWORD")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/user/create")
async def create_user(username: str, password: str):
    crud = IntegratedCRUD()
    try:
        if username == "" or password == "":
            return {"code": 400, "message": "Invalid username or password"}
        token = create_jwt(username, password)
        await crud.create_user(username, hash_password(password), token)
        return {
            "code": 200,
            "message": f"Successfully create user {username}",
            "data": username,
        }
    except Exception as e:
        logger.error(str(e))
        if "Duplicate entry" in str(e):
            return {"code": 400, "message": f"User {username} already exists!"}
        return {"code": 400, "message": str(e)}


@router.put("/user/top-up")
async def topup_credits(credits: int, user_id: str = Depends(get_current_user)):
    crud = IntegratedCRUD()
    try:
        credits = await crud.topup_credits(user_id, credits)
        return {
            "code": 200,
            "message": f"Successfully top up credits {user_id}",
            "result": {"remaining_credits": credits},
        }
    except Exception as e:
        logger.error(str(e))
        return {"code": 400, "message": str(e)}


@router.post("/user/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    crud = IntegratedCRUD()
    user_id = form_data.username
    hashed_password = hash_password(form_data.password)
    token = await crud.get_token(user_id, hashed_password)
    if token:
        return {"code": 200, "access_token": token, "token_type": "bearer"}
    else:
        return {"code": 400, "message": "Incorrect username or password"}


@router.get("/user/credits")
async def read_user_credits(user_id: str = Depends(get_current_user)):
    crud = IntegratedCRUD()
    credits = await crud.get_credits(user_id)
    return {
        "code": 200,
        "message": "Successfully get credits",
        "data": {"user_id": user_id, "credits": credits},
    }


@router.delete("/user/delete")
async def delete_user(user_id):
    crud = IntegratedCRUD()
    try:
        await crud.delete_user_by_id(user_id)
        return {"code": 200, "message": f"Successfully delete user {user_id}"}
    except Exception as e:
        return {"code": 400, "message": str(e)}


@router.post("/user/send-email")
def send_email(receiver_email, token, verification_link="http://192.168.3.16:8080/"):
    try:
        email_server = SMTP_SSL("smtp.gmail.com", 465)
        email_server.login(OWN_EMAIL, OWN_EMAIL_PASSWORD)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Log in to EZPrompt"
        html = """
        <html>
        <body>
            <p>Click the button below to log in to <b>EZPrompt</b></p>

            <a href="{}" style="display: inline-block; padding: 10px 20px; color: #FFF; background-color: #007BFF; text-decoration: none; border-radius: 5px;">Log in to EZPrompt</a>
        </body>
        </html>
        """.format(
            verification_link + f"?token={token}"
        )
        part = MIMEText(html, "html")
        msg.attach(part)
        email_server.sendmail(OWN_EMAIL, receiver_email, msg.as_string())
        email_server.quit()
        return {"code": 200, "message": "Email sent successfully"}
    except Exception as e:
        logger.error(str(e))
        return {"code": 400, "message": str(e)}


@router.post("/user/encode")
def encode_account(user_id: str, password: str):
    payload = {"user_id": user_id, "password": password}
    return encode(payload)


@router.post("/user/decode")
def decode_account(token: str):
    try:
        return decode(token)
    except Exception as e:
        return HTTPException(status_code=400, detail=e)
