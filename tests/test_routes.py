import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRoutes:
    """Test route endpoints"""
    
    def test_list_routes(self):
        """Test FR1.1: List all routes"""
        response = client.get("/api/v1/routes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_route_details(self):
        """Test FR1.2: Get route details"""
        response = client.get("/api/v1/routes/1")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "name" in data
    
    def test_get_route_not_found(self):
        """Test getting non-existent route"""
        response = client.get("/api/v1/routes/999")
        assert response.status_code == 404
    
    def test_export_gpx(self):
        """Test FR2.1: Export route as GPX"""
        response = client.get("/api/v1/routes/1/gpx")
        assert response.status_code == 200
        data = response.json()
        assert "filename" in data
        assert "content" in data
        assert data["filename"].endswith(".gpx")
