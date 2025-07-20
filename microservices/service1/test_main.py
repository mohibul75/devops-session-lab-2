from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Service 1", "status": "running"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {}

def test_create_and_get_item():
    # Create an item
    item_data = {"name": "Test Item", "description": "This is a test item"}
    response = client.post("/items", json=item_data)
    assert response.status_code == 200
    result = response.json()
    assert "item_id" in result
    assert result["item"]["name"] == "Test Item"
    
    # Get the created item
    item_id = result["item_id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item" 