from pydantic import BaseModel
from typing import Optional

class Blogs(BaseModel):
    # title:Union[str, None] = None
    # description:Optional[str]
    title:str
    description:str

class UpdateBlog(BaseModel):
    title:Optional[str] = None
    description:Optional[str] = None
class ShowBlog(BaseModel):
    title: str
    description:str
    class Config():
        orm_mode = True

class Users(BaseModel):
    fname:str
    email:str
    password:str
