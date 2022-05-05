from models import schemas, model
from sqlalchemy.orm import Session

async def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Post).offset(skip).limit(limit).all()


async def get_post(db: Session, id:int):
    return db.query(model.Post).filter(model.Post.id == id).first()


async def create_post(db: Session, post: schemas.PostCreate):
    db_post = model.Post(title=post.title, body=post.body)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
 

async def update_post(db: Session, post: schemas.Post):
    db_post = db.query(model.Post).filter(model.Post.id == id).first()
    db_post.title = post.title
    db_post.body = post.body
    db.commit()
    db.refresh(db_post)
    return db_post


async def delete_post(db: Session, id:int):
    db_post = db.query(model.Post).filter(model.Post.id == id).first()
    db.delete(db_post)
    db.commit()
