from sqlalchemy import Column, Integer, String, Text
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)  # Rich text HTML/Markdown content
    image_path = Column(String, nullable=True)  # Optional image path
