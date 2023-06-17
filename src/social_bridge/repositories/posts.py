from sqlalchemy.orm import Session
from sqlalchemy import update, func

from social_bridge.models import Post, NGO, Comment, Like


def get_post_by_id(db: Session, post_id: int):
    return db.query(
        Post.id.label("post_id"),
        Post.content,
        Post.created_at,
        Post.updated_at,
        Post.image.label("post_image"),
        NGO.id.label("ngo_id"),
        NGO.name,
        NGO.image.label("ngo_image"),
        func.count(Comment.id),
        func.count(Like.id),
    ).join(NGO).outerjoin(Comment).outerjoin(Like).group_by(
        Post.id.label("post_id"),
        Post.content,
        Post.created_at,
        Post.updated_at,
        Post.image.label("post_image"),
        NGO.id.label("ngo_id"),
        NGO.name,
        NGO.image.label("ngo_image"),

    ).filter(Post.id == post_id).first()


def fetch_all_posts(db: Session) -> [[Post, NGO]]:
    return db.query(
        Post.id.label("post_id"),
        Post.content,
        Post.created_at,
        Post.updated_at,
        Post.image.label("post_image"),
        NGO.id.label("ngo_id"),
        NGO.name,
        NGO.image.label("ngo_image"),
        func.count(Comment.id),
        func.count(Like.id),
    ).join(NGO).outerjoin(Comment).outerjoin(Like).group_by(
        Post.id.label("post_id"),
        Post.content,
        Post.created_at,
        Post.updated_at,
        Post.image.label("post_image"),
        NGO.id.label("ngo_id"),
        NGO.name,
        NGO.image.label("ngo_image"),

    ).all()


def create_one(db: Session, **post_props) -> Post | None:
    db_post = Post(**post_props)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_one(db: Session, post_id: int, **ngo_props):
    db.execute(
        update(Post)
        .where(Post.id == post_id)
        .values(**ngo_props)
    )
    db.commit()
    return get_post_by_id(db, post_id)

