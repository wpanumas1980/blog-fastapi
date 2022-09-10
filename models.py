from sqlalchemy import Column, Integer, String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship
class Blogs(Base):

    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("Users", back_populates="blogs")


class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blogs", back_populates="creator")