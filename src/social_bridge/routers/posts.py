from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from social_bridge.repositories.posts import create_one, fetch_all_posts, update_one
from social_bridge.repositories.ngo import get_one_by_id
from social_bridge.config import Settings
from social_bridge.dependencies import get_settings, get_db, get_image_size
from social_bridge.schemas.posts import PostSchema
from social_bridge.schemas.ngo import NGOProfileSchema
from social_bridge.media import get_resource_absolute_path, flush_old_media_resources, create_media_resource, \
    get_media_image_url
from social_bridge.tasks import resize_image

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=PostSchema)
async def create_post(
        content: str = Form(...),
        ngo: int = Form(...),
        event: int = Form(default=None),
        project: int = Form(default=None),
        image: UploadFile = File(...),
        db: Session = Depends(get_db),
        settings: Settings = Depends(get_settings),
        image_size: Settings = Depends(get_image_size)
):
    ngo = get_one_by_id(db, ngo_id=ngo)
    db_post = create_one(db, content=content, event=event, project=project)
    ngo.posts.append(db_post)
    db.commit()
    db.refresh(db_post)

    image_format = image.filename.split(".")[-1]
    relative_image_path = Path(f"{ngo.id}/posts/{db_post.id}.{image_format}")
    absolute_image_path = get_resource_absolute_path(relative_image_path, media_folder=settings.MEDIA_FOLDER)

    flush_old_media_resources(absolute_image_path)
    create_media_resource(absolute_image_path, await image.read())
    resize_image.delay(str(absolute_image_path), list(settings.IMAGE_SIZES.values()))

    data = update_one(db, db_post.id, image=str(relative_image_path.name))
    post_id, content, created_at, updated_at, post_image, \
        ngo_id, ngo_name, ngo_image, comments_count, like_count = data
    return PostSchema(
        id=post_id,
        content=content,
        created_at=created_at,
        updated_at=updated_at,
        image=get_media_image_url(
            Path(f"{ngo_id}/posts/{post_image}"),
            image_size,
            media_base_url=settings.MEDIA_BASE_URL
        ),
        comments_count=comments_count,
        likes_count=like_count,
        ngo=NGOProfileSchema(
            id=ngo_id,
            name=ngo_name,
            image=get_media_image_url(
                Path(f"ngo/{ngo_id}/{ngo_image}"),
                image_size,
                media_base_url=settings.MEDIA_BASE_URL),
            )
        )


@router.get("")
async def fetch_posts(db: Session = Depends(get_db), settings: Settings = Depends(get_settings),
                      image_size: int = Depends(get_image_size)):
    posts = fetch_all_posts(db)
    response_data = []
    for data in posts:
        post_id, content, created_at, updated_at, post_image, \
            ngo_id, ngo_name, ngo_image, comments_count, like_count = data
        response_data.append(
            PostSchema(
                id=post_id,
                content=content,
                created_at=created_at,
                updated_at=updated_at,
                image=get_media_image_url(
                    Path(f"{ngo_id}/posts/{post_image}"),
                    image_size,
                    media_base_url=settings.MEDIA_BASE_URL
                ),
                comments_count=comments_count,
                likes_count=like_count,
                ngo=NGOProfileSchema(
                    id=ngo_id,
                    name=ngo_name,
                    image=get_media_image_url(
                        Path(f"ngo/{ngo_id}/{ngo_image}"),
                        image_size,
                        media_base_url=settings.MEDIA_BASE_URL),
                )
            )
        )
    return response_data
