from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ

from fastapi import Depends, HTTPException, status, APIRouter, Body
from sqlalchemy.orm import Session

from social_bridge.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from social_bridge.database import get_db
from social_bridge.schemas.users import (
    LoginSchema,
    TokenSchema,
    UserSchema,
    UserCreateSchema,
)
from social_bridge.repositories.users import create_one
from social_bridge.mail import send_mail
from social_bridge.jinja_config import env
from social_bridge.auth import generate_confirmation_token


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserSchema, status_code=201)
async def register(user: UserCreateSchema = Body(...), db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = create_one(
        db,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        disabled=True,
    )

    template = env.get_template("confirmation_email.html")
    msg_content = template.render(confirm_url=generate_confirmation_token(user.email))
    message = MIMEMultipart("alternative")
    message["Subject"] = "social_bridge account - email confirmation"
    message["From"] = environ.get("SMTP_EMAIL")
    message["To"] = user.email
    message.attach(MIMEText(msg_content, "html"))
    send_mail(user.email, message)

    return db_user
