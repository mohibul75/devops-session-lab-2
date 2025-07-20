from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Service 2", "status": "running"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == {}

def test_create_and_get_task():
    # Create a task
    task_data = {"title": "Test Task"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    result = response.json()
    assert "task_id" in result
    assert result["task"]["title"] == "Test Task"
    
    # Get the created task
    task_id = result["task_id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

@patch("requests.get")
def test_service1_status_available(mock_get):
    mock_get.return_value.json.return_value = {"status": "healthy"}
    mock_get.return_value.status_code = 200
    
    response = client.get("/service1-status")
    assert response.status_code == 200
    assert response.json() == {"service1_status": {"status": "healthy"}}

@patch("requests.get")
def test_service1_status_unavailable(mock_get):
    mock_get.side_effect = Exception("Connection error")
    
    response = client.get("/service1-status")
    assert response.status_code == 200
    assert "service1_status" in response.json()
    assert response.json()["service1_status"] == "unavailable" 