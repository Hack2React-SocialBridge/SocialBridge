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


class NGOMembership(TimestampedModel):
    __tablename__ = "ngo_memberships"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="memberships")
    ngo_id = Column(Integer, ForeignKey("ngo.id"))
    ngo = relationship("NGO", back_populates="ngo")


class CompanyMembership(TimestampedModel):
    __tablename__ = "company_memberships"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="memberships")
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="company")


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
    ngo = relationship("NGOMembership", secondary=NGOMembership, back_populates="user")
    company = relationship("CompanyMembership", secondary=CompanyMembership, back_populates="user")


class NGO(TimestampedModel):
    __tablename__ = "ngo"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    image = Column(String)
    description = Column(String)
    members = relationship("NGOMembership", secondary=NGOMembership, back_populates="ngo")
    tax_number = Column(String)
    regon = Column(String)
    events = relationship("Event", back_populates="ngo")
    posts = relationship("Post", back_populates="ngo")


class Company(TimestampedModel):
    __tablename__ = "companies"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    image = Column(String)
    description = Column(String)
    members = relationship("CompanyMembership", secondary=CompanyMembership, back_populates="company")
    tax_number = Column(String)
    regon = Column(String)


class Event(TimestampedModel):
    __tablename__ = "events"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    date = Column(DateTime)
    name = Column(String)
    description = Column(String)
    image = Column(Integer)
    ngo_id = Column(Integer, ForeignKey("ngo.id"))
    ngo = relationship("NGO", back_populates="events", uselist=False)
    post = relationship("Post", back_populates="event", uselist=False)


class Post(TimestampedModel):
    __tablename__ = "posts"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    content = Column(String)
    image = Column(String)
    ngo_id = Column(Integer, ForeignKey("ngo.id"))
    ngo = relationship("NGO", back_populates="posts", uselist=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="post", uselist=False)
