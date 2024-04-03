from pydantic import BaseModel


class CommentCreateSchema(BaseModel):
    author_id: int
    comment: str
