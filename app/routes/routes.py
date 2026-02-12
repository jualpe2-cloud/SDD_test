from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from app.services.strava_service import StravaService
from app.services.gpx_service import GPXService
from app.utils.auth import verify_jwt_token

router = APIRouter(prefix="/api/v1", tags=["routes"])
strava_service = StravaService()
gpx_service = GPXService()
security = HTTPBearer()

def get_access_token_from_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract and validate access token from JWT"""
    jwt_token = credentials.credentials
    payload = verify_jwt_token(jwt_token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload.get("access_token")

@router.get("/routes")
def list_routes(access_token: str = Depends(get_access_token_from_jwt)):
    """Get all routes from Strava"""
    try:
        routes = strava_service.get_routes(access_token)
        if not routes:
            return []
        return routes
    except Exception as e:
        print(f"Error fetching routes: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch routes from Strava")

@router.get("/routes/{route_id}")
def get_route(route_id: int, access_token: str = Depends(get_access_token_from_jwt)):
    """Get detailed information about a specific route"""
    try:
        route = strava_service.get_route_detail(access_token, str(route_id))
        if route is None:
            raise HTTPException(status_code=404, detail="Route not found")
        return route
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching route detail: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch route details")

@router.get("/routes/{route_id}/gpx")
def export_gpx(route_id: int, access_token: str = Depends(get_access_token_from_jwt)):
    """Export a route as GPX file"""
    try:
        # Get route details from Strava
        route = strava_service.get_route_detail(access_token, str(route_id))
        if route is None:
            raise HTTPException(status_code=404, detail="Route not found")
        
        # Check if route has map data with polyline
        if 'map' not in route or 'polyline' not in route['map']:
            raise HTTPException(status_code=400, detail="Route has no map data")
        
        # Decode polyline to coordinates
        polyline = route['map']['polyline']
        coordinates = gpx_service.decode_polyline(polyline)
        
        # Convert coordinates to proper format for GPX
        points = [{"lat": lat, "lon": lon} for lat, lon in coordinates]
        
        # Generate GPX content
        gpx_content = gpx_service.create_gpx(points)
        
        # Create filename from route name
        route_name = route.get('name', f'route_{route_id}').replace(' ', '_')
        
        return {
            "filename": f"{route_name}.gpx",
            "content": gpx_content
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error exporting GPX: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to export GPX: {str(e)}")
