from pydantic import BaseModel
from typing import Optional
from datetime import datetime






class PostBased(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int]= None
    # created_at: int

    class Config:
        orm_mode = True


class PostCreate(PostBased):
    pass



class Post(PostBased):
    id: int
    created_at: datetime


    class Config:
        orm_mode = True

