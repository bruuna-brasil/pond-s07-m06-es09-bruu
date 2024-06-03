from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from main import app, get_db
from database import Base
from models import Story, User
import schemas

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas
Base.metadata.create_all(bind=engine)

# Dependência sobreposta para usar o banco de dados de teste
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    # Configura o banco de dados de teste
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_story(test_db):
    response = client.post(
        "/stories/",
        json={"title": "Test Story", "description": "Test Description", "category": "Test"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Story"

def test_read_stories(test_db):
    response = client.get("/stories/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_story(test_db):
    # Primeiro, crie uma história
    response = client.post(
        "/stories/",
        json={"title": "Test Story", "description": "Test Description", "category": "Test"}
    )
    story_id = response.json()["id"]
    
    # Atualize a história criada
    response = client.put(
        f"/stories/{story_id}",
        json={"title": "Updated Title", "description": "Updated Description", "category": "Updated Category"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_story(test_db):
    # Primeiro, crie uma história
    response = client.post(
        "/stories/",
        json={"title": "Test Story", "description": "Test Description", "category": "Test"}
    )
    story_id = response.json()["id"]
    
    # Exclua a história criada
    response = client.delete(f"/stories/{story_id}")
    assert response.status_code == 200
    assert response.json()["id"] == story_id

def test_create_user(test_db):
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_read_users(test_db):
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_user(test_db):
    # Primeiro, crie um usuário
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    user_id = response.json()["id"]
    
    # Atualize o usuário criado
    response = client.put(
        f"/users/{user_id}",
        json={"username": "updateduser", "email": "updated@example.com", "password": "updatedpassword"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

def test_delete_user(test_db):
    # Primeiro, crie um usuário
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    user_id = response.json()["id"]
    
    # Exclua o usuário criado
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
