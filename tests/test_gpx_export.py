import pytest
from app.services.gpx_service import GPXService

class TestGPXExport:
    """Test GPX export functionality (FR2.1)"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.sample_route = {
            "id": 12345,
            "name": "Test Route",
            "description": "A test route",
            "distance": 25000,
            "elevation_gain": 450,
            "type": "Ride",
            "map": {
                "polyline": "encoded_polyline_string"
            }
        }
    
    def test_decode_polyline(self):
        """Test polyline decoding"""
        # Mock encoded polyline
        encoded = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
        coords = GPXService.decode_polyline(encoded)
        
        # Verify coordinates are decoded
        assert coords is not None
        assert len(coords) > 0
    
    def test_create_gpx_from_route(self):
        """Test GPX creation from route data"""
        # Sample points with lat/lon structure expected by create_gpx_from_route
        sample_points = [
            {"lat": 40.7128, "lon": -74.0060},  # New York
            {"lat": 40.7580, "lon": -73.9855},  # Central Park
        ]
        gpx_content = GPXService.create_gpx(sample_points)
        
        # Verify GPX structure
        assert gpx_content is not None
        assert "<?xml" in gpx_content
        assert "<gpx" in gpx_content
