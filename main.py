from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
from typing import List
from typing import Optional
import crud
import models
import schemas
from database import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


IMAGE_DIR = Path("static/images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/posts/", response_model=schemas.PostResponse)
async def create_post_endpoint(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_path = None
    if image:
        image_path = IMAGE_DIR / image.filename
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = str(image_path)

    post_data = schemas.PostCreate(title=title, content=content, image_path=image_path)
    return crud.create_post(db=db, post=post_data)

# Route to update an existing post
@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post_endpoint(
    id: int,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_post = crud.get_post(db, id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    image_path = db_post.image_path
    if image:
        image_path = IMAGE_DIR / image.filename
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_path = str(image_path)

    post_data = schemas.PostUpdate(title=title, content=content, image_path=image_path)
    return crud.update_post(db=db, post_id=id, post_data=post_data)

# Route to delete a post
@app.delete("/posts/{id}", response_model=dict)
async def delete_post_endpoint(id: int, db: Session = Depends(get_db)):
    if not crud.delete_post(db, id):
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}

# Route to read a single post
@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def read_post(id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Route to read multiple posts
@app.get("/posts/", response_model=List[schemas.PostResponse])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_posts(db, skip=skip, limit=limit)

# Route to upload an image
@app.post("/upload/", response_model=dict)
async def upload_image(image: UploadFile = File(...)):
    image_path = IMAGE_DIR / image.filename
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"image_path": str(image_path)}

# Route to delete an image by filename
@app.delete("/upload/{image_name}", response_model=dict)
async def delete_image(image_name: str):
    image_path = IMAGE_DIR / image_name
    if image_path.exists():
        image_path.unlink()  # Remove the file
        return {"message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")

# Route to serve an image
@app.get("/images/{image_name}")
def get_image(image_name: str):
    image_path = IMAGE_DIR / image_name
    if image_path.exists():
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=404, detail="Image not found")
