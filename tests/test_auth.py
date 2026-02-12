import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAuth:
    """Test authentication endpoints (FR3.1)"""
    
    def test_oauth_login_endpoint_exists(self):
        """Test that the OAuth login endpoint exists"""
        response = client.post("/api/v1/auth/login", json={"code": "test_code"})
        # Should not return 404
        assert response.status_code != 404
    
    def test_oauth_login_invalid_code(self):
        """Test OAuth login with invalid code"""
        response = client.post("/api/v1/auth/login", json={"code": "invalid_code"})
        # Should return an error (400, 422, or 500)
        assert response.status_code in [400, 422, 500]
