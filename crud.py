from sqlalchemy.orm import Session
import models
import schemas

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(title=post.title, content=post.content, image_path=post.image_path)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_data: schemas.PostUpdate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return None
    update_data = post_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False

def get_all_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()
