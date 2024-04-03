from typing import List

from pydantic import BaseModel


class UserBaseModel(BaseModel):
    email: str
    username: str
    password: str
    followers: List[str] = []
