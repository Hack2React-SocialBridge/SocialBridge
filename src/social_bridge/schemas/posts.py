from datetime import datetime

from pydantic import BaseModel, PositiveInt

from social_bridge.schemas.ngo import NGOProfileSchema


class PostSchema(BaseModel):
    id: PositiveInt
    content: str
    ngo: NGOProfileSchema
    image: str
    created_at: datetime
    updated_at: datetime
