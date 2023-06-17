from sqlalchemy.orm import Session

from social_bridge.models import Post, NGO


def get_post_by_id(db: Session, post_id: int) -> Post | None:
    return db.query(Post, NGO).join(NGO).filter(Post.id == post_id).first()


def get_all_posts(db: Session) -> [Post]:
    return db.query(Post, NGO).join(NGO).all()


def create_one(db: Session, **post_props) -> Post | None:
    db_post = Post(**post_props)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


