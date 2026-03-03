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
