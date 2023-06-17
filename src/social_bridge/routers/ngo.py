from pathlib import Path
from fastapi import APIRouter, Depends, Body, UploadFile, File, Form
from sqlalchemy.orm import Session

from social_bridge.dependencies import get_settings, get_db, get_image_size
from social_bridge.schemas.ngo import NGOSchema, NGOCreationSchema
from social_bridge.config import Settings
from social_bridge.media import get_media_image_url, get_resource_absolute_path, flush_old_media_resources, \
    create_media_resource
from social_bridge.tasks import resize_image
from social_bridge.repositories.ngo import create_one, update_one

router = APIRouter(prefix="/ngo", tags=["ngo"])


@router.post("", response_model=NGOSchema)
async def create_ngo(
        description: str | None = Form(...),
        name: str = Form(...),
        tax_number: str = Form(...),
        regon: str = Form(...),
        image: UploadFile = File(...),
        db: Session = Depends(get_db),
        settings: Settings = Depends(get_settings),
        image_size: int = Depends(get_image_size)
):
    db_ngo = create_one(
        db,
        name=name,
        description=description,
        tax_number=tax_number,
        regon=regon,
    )

    image_format = image.filename.split(".")[-1]
    relative_image_path = Path(f"ngo/{db_ngo.id}/ngo_image.{image_format}")
    absolute_image_path = get_resource_absolute_path(relative_image_path, media_folder=settings.MEDIA_FOLDER)

    flush_old_media_resources(absolute_image_path)
    create_media_resource(absolute_image_path, await image.read())
    resize_image.delay(str(absolute_image_path), list(settings.IMAGE_SIZES.values()))

    update_one(db, ngo_id=db_ngo.id, image=str(relative_image_path.name))
    db.refresh(db_ngo)
    ngo_data = db_ngo.__dict__
    del ngo_data["image"]
    return NGOSchema(**ngo_data,
                     image=get_media_image_url(relative_image_path, image_size, media_base_url=settings.MEDIA_BASE_URL))
