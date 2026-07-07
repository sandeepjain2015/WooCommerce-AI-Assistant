from pydantic import BaseModel
from pydantic import HttpUrl


class StoreCreate(BaseModel):

    store_url: str

    consumer_key: str

    consumer_secret: str


class StoreUpdate(BaseModel):

    store_url: HttpUrl

    consumer_key: str

    consumer_secret: str


class StoreResponse(BaseModel):

    id: int

    store_url: str

    class Config:
        from_attributes = True
