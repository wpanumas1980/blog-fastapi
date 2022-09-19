from pydantic import BaseModel
from typing import Optional, List

class BlogBase(BaseModel):
    # title:Union[str, None] = None
    # description:Optional[str]
    title:str
    description:str
class Blogs(BlogBase):
    class Config():
        orm_mode = True

class UpdateBlog(BaseModel):
    title:Optional[str] = None
    description:Optional[str] = None

class Users(BaseModel):
    fname:str
    email:str
    password:str

class ShowUsers(BaseModel):
    fname:str
    email:str
    blogs:List[Blogs]=[]
    class Config():
        orm_mode = True

class ShowBlogs(BaseModel):
    title: str
    description:str
    creator: ShowUsers
    class Config():
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str