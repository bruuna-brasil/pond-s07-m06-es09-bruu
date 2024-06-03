from sqlalchemy.orm import Session
from models import Story, User
from schemas import StoryCreate, UserCreate

# CRUD para Histórias
def get_story(db: Session, story_id: int):
    return db.query(Story).filter(Story.id == story_id).first()

def get_stories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Story).offset(skip).limit(limit).all()

def create_story(db: Session, story: StoryCreate):
    db_story = Story(**story.dict())
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

def update_story(db: Session, story_id: int, story: StoryCreate):
    db_story = db.query(Story).filter(Story.id == story_id).first()
    if db_story:
        db_story.title = story.title
        db_story.description = story.description
        db_story.category = story.category
        db.commit()
        db.refresh(db_story)
        return db_story
    return None

def delete_story(db: Session, story_id: int):
    db_story = db.query(Story).filter(Story.id == story_id).first()
    if db_story:
        db.delete(db_story)
        db.commit()
        return db_story
    return None

# CRUD para Usuários
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None
