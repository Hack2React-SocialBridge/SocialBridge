from sqlalchemy.orm import Session
from sqlalchemy import update

from social_bridge.models import NGO


def get_one_by_id(db: Session, ngo_id: int) -> NGO | None:
    return db.query(NGO).filter(NGO.id == ngo_id).first()


def create_one(db: Session, **ngo_props):
    db_ngo = NGO(**ngo_props)
    db.add(db_ngo)
    db.commit()
    db.refresh(db_ngo)
    return db_ngo


def update_one(db: Session, ngo_id: int, **ngo_props) -> None:
    db.execute(
        update(NGO)
        .where(NGO.id == ngo_id)
        .values(**ngo_props)
    )
    db.commit()


