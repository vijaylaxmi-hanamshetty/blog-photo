from pydantic import BaseModel
from typing import Optional

class PostCreate(BaseModel):
    title: str
    content: str
    image_path: Optional[str] = None  

class PostUpdate(BaseModel):
    title: Optional[str] = None  
    image_path: Optional[str] = None  
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    image_path: Optional[str] = None  
    class Config:
        from_attribute = True
