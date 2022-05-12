import pytest

from httpx import AsyncClient
from app import app
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://localhost:7000') as client:
        yield client

@pytest.mark.anyio   
async def test_post_new_post(client):
    response = await client.post(
            "/post", 
            json={"title": "This is a test", "body": "This is a test body"}
        )
    assert response.status_code == 200, response.text
    id = response["id"]
    assert response.json() == {
        "title": "This is a test", "body": "This is a test body", "id": f"{id}"
        }
    
@pytest.mark.anyio
async def test_post(client):
    response = await client.post(
        "/post", 
        json={"title": "This is a test", "body": "This is a test body"}
        )
    assert response.status_code == 200, response.text
    id = response["id"]
    assert response.json() == {
        "title": "This is a test", "body": "This is a test body", "id": f"{id}"
        }
    
@pytest.mark.anyio
async def test_get_first_post(client):
    response = await client.get("/post/0")
    assert response.status_code == 200, response.text
    id = response["id"]
    assert response.json() == {
        "title": "This is a test",
        "body": "This is a test body"
    }

@pytest.mark.anyio
async def test_update_post(client):
    response = await client.put(
        "/post/0", 
        json={"title": "UPDATED TEST", "body": "UPDATED BODY TEST"}
        )
    assert response.status_code == 200, response.text
    id = response["id"]
    assert response.json() == {"title": "UPDATED TEST", "body": "UPDATED BODY TEST", "id": f"{id}"}

@pytest.mark.anyio
async def test_delete_post(client):
    response = await client.delete("/post/0")
    assert response.status_code == 200, response.text

@pytest.mark.anyio
async def test_get_all_posts(client):
    response = await client.get("/post/")
    assert response.status_code == 200, response.text
    """ assert response.json() == {'arrays': [{'body': 'This is a test body', 'title': 'This is a test'}]} """

@pytest.mark.anyio
async def test_get_nonexistent_post(client):
    response = await client.get("/post/10")
    assert response.status_code == HTTP_404_NOT_FOUND, response.text

@pytest.mark.anyio    
async def test_remove_nonexistent_post(client):
    response = await client.delete("/post/10")
    assert response.status_code == HTTP_404_NOT_FOUND, response.text

@pytest.mark.anyio
async def test_update_nonexistent_post(client):
    id = 10
    response = await client.put(
        f"/post/{id}", 
        json={"title": "UPDATED TEST", "body": "UPDATED BODY TEST", "id": f"{id}"}
        )
    assert response.status_code == HTTP_404_NOT_FOUND, response.text

@pytest.mark.anyio
async def test_post_new_post_without_body(client):
    response = await client.post(
        "/post", 
        json={"title": "This is a test"}
        )
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY, response.text
