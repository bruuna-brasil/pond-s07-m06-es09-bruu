from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import google.generativeai as genai
from typing import List
from database import SessionLocal, engine, Base
from crud import create_story, get_stories, create_user, get_users
from models import Story, User
import schemas
from fastapi.responses import HTMLResponse
from database import Base, engine

def create_database():
    Base.metadata.create_all(bind=engine)

# Chame esta função para criar o banco de dados e as tabelas
create_database()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

os.environ['GOOGLE_API_KEY'] = "AIzaSyAXoSoklDhkVOBIFNFHwAXK7-rZB1h35Ic"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def handle_input(request: Request, user_input: str = Form(...)):
    response_data = model.generate_content(user_input)
    return templates.TemplateResponse("index.html", {"request": request, "response_data": response_data.text})

@app.get("/create_story")
async def create_story_page(request: Request):
    return templates.TemplateResponse("create_story.html", {"request": request})

@app.post("/create_story", response_class=HTMLResponse)
async def create_story_endpoint(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    story_data = {
        "title": form_data["title"],
        "description": form_data["description"],
        "category": form_data["category"]
    }

    try:
        story = schemas.StoryCreate(**story_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_story = create_story(db=db, story=story)
    return templates.TemplateResponse("story_created.html", {"request": request, "story": db_story}, status_code=200)

@app.get("/list_stories", response_class=HTMLResponse)
async def list_stories_page(request: Request, db: Session = Depends(get_db)):
    stories = get_stories(db)
    return templates.TemplateResponse("list_stories.html", {"request": request, "stories": stories})

@app.get("/update_story/{story_id}", response_class=HTMLResponse)
async def update_story_page(story_id: int, request: Request, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    return templates.TemplateResponse("update_story.html", {"request": request, "story": story})

@app.get("/update_story_select", response_class=HTMLResponse)
async def update_story_select_page(request: Request, db: Session = Depends(get_db)):
    stories = get_stories(db)
    return templates.TemplateResponse("update_story_select.html", {"request": request, "stories": stories})

@app.get("/create_user")
async def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.get("/list_users")
async def list_users_page(request: Request):
    return templates.TemplateResponse("list_users.html", {"request": request})

@app.get("/docs")
async def show_docs(request: Request):
    return templates.TemplateResponse("docs.html", {"request": request})

@app.get("/generate_content?story_id={story_id}", response_class=HTMLResponse)
async def generate_content(story_id: int, request: Request, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    return templates.TemplateResponse("generate_content.html", {"request": request, "story": story})


@app.post("/generate_content/{story_id}", response_class=HTMLResponse)
async def generate_content(story_id: int, request: Request, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Gerar conteúdo com a API do Gemini
    response = model.generate_content(story.description)
    if response and response.text:
        new_content = response.text
        story.description += " " + new_content
        db.commit()
        db.refresh(story)
    else:
        new_content = "No content generated."

    return templates.TemplateResponse("story_updated.html", {"request": request, "story": story, "new_content": new_content})
