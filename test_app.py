import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import Base, async_session
from app import app

SQLALCHEMY_DATABASE_URL = "sqlite:///test/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[async_session] = override_get_db

client = TestClient(app)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
@pytest.mark.xfail        
def test_cleanup():
    with TestClient(app) as client:
        response = client.get("/post")
        print(response.json())
        

def test_post_new_post():
  
    response = client.post(
        "/post", 
        json={"title": "This is a test", "body": "This is a test body"}
        )
    assert response.status_code == 200
    key = int(response.json())
    print (key)
    response2 = client.get(f"/post/{key}")
    assert response2.json()['Post'] == {
        "title": "This is a test", "body": "This is a test body", "id": key
        }

def test_post_new_post2():
    
    response = client.post(
        "/post", 
        json={"title": "This is a test", "body": "This is a test body"}
        )
    assert response.status_code == 200
    key = int(response.json())
    response2 = client.get(f"/post/{key}")
    assert response2.json()['Post'] == {
        "title": "This is a test", "body": "This is a test body", "id": key
        }

def test_get_first_post():
    response = client.get("/post/1")
    assert response.status_code == 200
    id = response.json()['Post']['id']
    assert response.json()['Post'] == {
        "title": "This is a test", "body": "This is a test body", "id": id
        }
    print (response.json())



def test_update_post():
    response = client.put(
        "/post/2", 
        json={"title": "UPDATED TEST", "body": "UPDATED BODY TEST", "id": 2}
        )
    print (response.json())
    assert response.status_code == 200
    id = response.json()['Post']['id']
    assert response.json()['Post'] == {"title": "UPDATED TEST", "body": "UPDATED BODY TEST", "id": id}

def test_delete_post():
    response = client.delete("/post/1")
    assert response.status_code == 200

def test_get_all_posts():
    response = client.get("/post/")
    assert response.status_code == 200
    print(response.json())
    

def test_get_nonexistent_post():
    response = client.get("/post/1000")
    print(f"something {response.json()}")
    assert response.status_code == 404
    
def test_remove_nonexistent_post():
    response = client.delete("/post/1000")
    assert response.status_code == 404

def test_update_nonexistent_post():
    response = client.put(
        "/post/1000", 
        json={"title": "UPDATED TEST", "body": "UPDATED BODY TEST", "id": 1000}
        )
    assert response.status_code == 404, response.text

def test_post_new_post_without_body():
    response = client.put(
        "/post", 
        json={"title": "This is a test"}
        )
    assert response.status_code == 405, response.text