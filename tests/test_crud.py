from fastapi import FastAPI, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import google.generativeai as genai
from typing import List
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

os.environ['GOOGLE_API_KEY'] = "AIzaSyAXoSoklDhkVOBIFNFHwAXK7-rZB1h35Ic"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root(request: Request):
    return {"message": "Welcome to the Story Management API"}

@app.post("/generate-content/")
async def generate_content(request: Request, user_input: str = Form(...)):
    response_data = model.generate_content(user_input)
    return {"generated_content": response_data.text}

@app.post("/stories/", response_model=schemas.Story)
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db)):
    return crud.create_story(db=db, story=story)

@app.get("/stories/", response_model=List[schemas.Story])
def read_stories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stories = crud.get_stories(db, skip=skip, limit=limit)
    return stories

@app.put("/stories/{story_id}", response_model=schemas.Story)
def update_story(story_id: int, story: schemas.StoryCreate, db: Session = Depends(get_db)):
    db_story = crud.update_story(db=db, story_id=story_id, story=story)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story

@app.delete("/stories/{story_id}", response_model=schemas.Story)
def delete_story(story_id: int, db: Session = Depends(get_db)):
    db_story = crud.delete_story(db=db, story_id=story_id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return db_story

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
