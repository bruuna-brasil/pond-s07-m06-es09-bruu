from pydantic import BaseModel
from typing import List, Optional

# Schemas para Histórias
class StoryBase(BaseModel):
    title: str
    description: str
    category: str

class StoryCreate(StoryBase):
    pass

class Story(StoryBase):
    id: int

    class Config:
        orm_mode = True

# Schemas para Usuários
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
