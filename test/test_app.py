from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_get_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "home":"The Homepage"
    }

def test_get_first_post():
    response = client.get("/crudapi/0")
    assert response.status_code == 200
    assert response.json() == {
        "title": "Testing",
        "body": "Testbody"
    }

def test_post_new_post():
    response = client.post(
        "/crudapi", 
        json={"title": "This is a test", "body": "This is a test body"}
        )
    assert response.status_code == 200
    assert response.json() == {
        "title": "This is a test", "body": "This is a test body"
        }

def test_update_post():
    response = client.put(
        "/crudapi/0", 
        json={"title": "UPDATED TEST", "body": "UPDATED BODY TEST"}
        )
    assert response.status_code == 200
    assert response.json() == {"title": "UPDATED TEST", "body": "UPDATED BODY TEST"}

def test_delete_post():
    response = client.delete("/crudapi/0")
    assert response.status_code == 200

def test_get_all_posts():
    response = client.get("/crudapi/")
    assert response.status_code == 200
    assert response.json() == {'arrays': [{'body': 'This is a test body', 'title': 'This is a test'}]}

def test_get_nonexistent_post():
    response = client.get("/crudapi/10")
    assert response.status_code == 404
    
def test_remove_nonexistent_post():
    response = client.delete("/crudapi/10")
    assert response.status_code == 404

def test_update_nonexistent_post():
    response = client.put(
        "/crudapi/10", 
        json={"title": "UPDATED TEST", "body": "UPDATED BODY TEST"}
        )
    assert response.status_code == 404

def test_post_new_post_without_body():
    response = client.post(
        "/crudapi", 
        json={"title": "This is a test"}
        )
    assert response.status_code == 422
