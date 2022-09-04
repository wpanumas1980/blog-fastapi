from pydantic import BaseModel, Field

class Blogs(BaseModel):
    title:str
    description:str