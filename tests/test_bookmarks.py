from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_bookmarks():
    """Test the /bookmarks endpoint returns expected response"""
    response = client.get("/bookmarks")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

def test_bookmarks_structure():
    """Test that each bookmark has the expected fields and types"""
    response = client.get("/bookmarks")
    data = response.json()
    bookmarks = data["data"]
    
    # Skip test if no bookmarks exist
    if not bookmarks:
        return
        
    # Check first bookmark has required fields and correct types
    bookmark = bookmarks[0]
    assert "id" in bookmark
    assert "country" in bookmark
    assert "status" in bookmark
    assert "timestamp" in bookmark
    
    assert isinstance(bookmark["id"], int)
    assert isinstance(bookmark["country"], str)
    assert isinstance(bookmark["status"], str)
    assert isinstance(bookmark["timestamp"], str)

def test_bookmark_status_values():
    """Test that bookmark status values are valid"""
    response = client.get("/bookmarks")
    data = response.json()
    bookmarks = data["data"]
    
    valid_statuses = {"active", "archived", "pending"}
    for bookmark in bookmarks:
        assert bookmark["status"] in valid_statuses

def test_create_bookmark():
    """Test successful bookmark creation"""
    test_bookmark = {
        "country": "New Zealand",
        "status": "active"
    }
    response = client.post("/bookmark", json=test_bookmark)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    created = data["data"]
    assert created["country"] == test_bookmark["country"]
    assert created["status"] == test_bookmark["status"]
    assert isinstance(created["id"], int)
    assert isinstance(created["timestamp"], str)

def test_create_bookmark_validation():
    """Test validation of required fields"""
    # Missing country
    response = client.post("/bookmark", json={"status": "active"})
    assert response.status_code == 422

    # Missing status
    response = client.post("/bookmark", json={"country": "Spain"})
    assert response.status_code == 422

    # Empty country
    response = client.post("/bookmark", json={"country": "", "status": "active"})
    assert response.status_code == 422

    # Invalid status
    response = client.post("/bookmark", json={"country": "France", "status": "invalid"})
    assert response.status_code == 422

def test_create_bookmark_country_validation():
    """Test country name validation"""
    # Country name too long (>100 chars)
    long_country = "x" * 101
    response = client.post("/bookmark", json={"country": long_country, "status": "active"})
    assert response.status_code == 422

    # Special characters in country name
    response = client.post("/bookmark", json={"country": "Test@Country", "status": "active"})
    assert response.status_code == 422
