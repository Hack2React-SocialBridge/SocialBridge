from enum import Enum

from sqlalchemy import Boolean, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship


from social_bridge.database import Base, engine


Base.metadata.create_all(bind=engine)


class TimestampedModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class UserTypes(Enum):
    PUBLIC = 1
    NGO = 2
    BUSINESS = 4
    ADMIN = 8


class User(TimestampedModel):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    disabled = Column(Boolean)
    profile_image = Column(String)
    account_type = Column(Integer)


# class NGO(TimestampedModel):
#     __tablename__ = "ngo"




