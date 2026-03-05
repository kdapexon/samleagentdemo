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

def test_get_bookmark_by_id():
    """Test retrieving a single bookmark by ID"""
    response = client.get("/bookmark/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == 1

def test_get_bookmark_not_found():
    """Test retrieving a non-existent bookmark returns 404"""
    response = client.get("/bookmark/99999")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

def test_get_bookmark_invalid_id():
    """Test retrieving a bookmark with invalid ID returns 400"""
    # Zero ID
    response = client.get("/bookmark/0")
    assert response.status_code == 400
    data = response.json()
    assert "positive integer" in data["detail"].lower()

    # Negative ID
    response = client.get("/bookmark/-1")
    assert response.status_code == 400
    data = response.json()
    assert "positive integer" in data["detail"].lower()

def test_get_bookmark_non_integer_id():
    """Test retrieving a bookmark with non-integer ID returns 422"""
    response = client.get("/bookmark/abc")
    assert response.status_code == 422

    response = client.get("/bookmark/1.5")
    assert response.status_code == 422

def test_delete_bookmark_not_found():
    """Test deleting a non-existent bookmark returns 404"""
    response = client.delete("/bookmark/99999")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

def test_delete_bookmark_invalid_id():
    """Test deleting a bookmark with invalid ID returns 400"""
    # Zero ID
    response = client.delete("/bookmark/0")
    assert response.status_code == 400
    data = response.json()
    assert "positive integer" in data["detail"].lower()

    # Negative ID
    response = client.delete("/bookmark/-1")
    assert response.status_code == 400
    data = response.json()
    assert "positive integer" in data["detail"].lower()

def test_delete_bookmark_non_integer_id():
    """Test deleting a bookmark with non-integer ID returns 422"""
    response = client.delete("/bookmark/abc")
    assert response.status_code == 422

    response = client.delete("/bookmark/1.5")
    assert response.status_code == 422

def test_delete_bookmark_success():
    """Test successful deletion of a bookmark"""
    # First, create a bookmark to delete
    test_bookmark = {
        "country": "Germany",
        "status": "active"
    }
    create_response = client.post("/bookmark", json=test_bookmark)
    assert create_response.status_code == 200
    created_data = create_response.json()
    bookmark_id = created_data["data"]["id"]

    # Delete the bookmark
    delete_response = client.delete(f"/bookmark/{bookmark_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "success"
    assert "deleted successfully" in delete_data["message"].lower()
    assert "deleted_bookmark" in delete_data
    assert delete_data["deleted_bookmark"]["id"] == bookmark_id
    assert delete_data["deleted_bookmark"]["country"] == test_bookmark["country"]

    # Verify the bookmark is actually deleted
    get_response = client.get(f"/bookmark/{bookmark_id}")
    assert get_response.status_code == 404

def test_delete_bookmark_and_verify_list():
    """Test that deleted bookmark is removed from the bookmarks list"""
    # Get initial count
    initial_response = client.get("/bookmarks")
    initial_count = len(initial_response.json()["data"])

    # Create a bookmark
    test_bookmark = {
        "country": "Italy",
        "status": "pending"
    }
    create_response = client.post("/bookmark", json=test_bookmark)
    created_id = create_response.json()["data"]["id"]

    # Verify count increased
    after_create_response = client.get("/bookmarks")
    assert len(after_create_response.json()["data"]) == initial_count + 1

    # Delete the bookmark
    delete_response = client.delete(f"/bookmark/{created_id}")
    assert delete_response.status_code == 200

    # Verify count is back to original
    after_delete_response = client.get("/bookmarks")
    after_delete_bookmarks = after_delete_response.json()["data"]
    assert len(after_delete_bookmarks) == initial_count

    # Verify the specific bookmark is not in the list
    assert not any(b["id"] == created_id for b in after_delete_bookmarks)

def test_delete_bookmark_twice():
    """Test that deleting the same bookmark twice returns 404 on second attempt"""
    # Create a bookmark
    test_bookmark = {
        "country": "Sweden",
        "status": "active"
    }
    create_response = client.post("/bookmark", json=test_bookmark)
    bookmark_id = create_response.json()["data"]["id"]

    # First deletion should succeed
    first_delete = client.delete(f"/bookmark/{bookmark_id}")
    assert first_delete.status_code == 200

    # Second deletion should return 404
    second_delete = client.delete(f"/bookmark/{bookmark_id}")
    assert second_delete.status_code == 404
    assert "not found" in second_delete.json()["detail"].lower()
