from pydantic import BaseModel, Field
from typing import Optional,Union

class Blogs(BaseModel):
    title:Union[str, None] = None
    description:Optional[str]