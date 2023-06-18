from typing import Optional

from pydantic import BaseModel, PositiveInt


class NGOProfileSchema(BaseModel):
    id: PositiveInt
    name: str
    image: str


class NGOSchema(BaseModel):
    id: PositiveInt
    name: str
    description: Optional[str]
    tax_number: str
    regon: str
