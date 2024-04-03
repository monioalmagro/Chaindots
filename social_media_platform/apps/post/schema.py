from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from social_media_platform.apps.user.schema import UserBaseModel


class PostSchema(BaseModel):
    author: UserBaseModel
    content: str
    created_at: Optional[datetime]


class PostListSchema(BaseModel):
    author_id: Optional[int] = None
    page_size: Optional[int] = None
    page_number: Optional[int] = None
