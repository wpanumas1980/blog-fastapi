from pydantic import BaseModel, Field
from typing import Optional,Union

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


