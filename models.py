from sqlalchemy import Column, Integer, String
from database import Base
class Blogs(Base):

    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String)
    email = Column(String)
    password = Column(String)