from os import environ
from typing import Annotated

from fastapi import Header, HTTPException, status, Depends
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status

from social_bridge.auth import oauth2_scheme, verify_token
from social_bridge.database import get_db
from social_bridge.models import User
from social_bridge.repositories.users import get_user_by_email
from social_bridge.schemas.users import TokenDataSchema

AVAILABLE_IMAGE_SIZES = environ.get("AVAILABLE_IMAGE_SIZES").split(",")
IMAGE_SIZES = {size: environ.get(f"{size.upper()}_IMAGE_SIZE").split("x") for size in AVAILABLE_IMAGE_SIZES}


async def get_image_size(image_size: Annotated[str, Header(...)]):
    if image_size in AVAILABLE_IMAGE_SIZES:
        return IMAGE_SIZES[image_size][1]

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Wrong image size! Available sizes are: {AVAILABLE_IMAGE_SIZES}")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = verify_token(token)
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
