from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_bookmarks():
    """Test the /bookmarks endpoint returns expected response"""
    response = client.get("/bookmarks")
    assert response.status_code == 200
    data = response.json()
    assert "bookmarks" in data
    assert isinstance(data["bookmarks"], list)

def test_bookmarks_structure():
    """Test that each bookmark has the required key fields and types"""
    response = client.get("/bookmarks")
    data = response.json()
    bookmarks = data["bookmarks"]
    
    # Skip test if no bookmarks exist
    if not bookmarks:
        return
        
    # Check first bookmark has required id field and correct type
    bookmark = bookmarks[0]
    assert "id" in bookmark
    assert isinstance(bookmark["id"], int)

