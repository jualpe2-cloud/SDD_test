from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(prefix="/api/v1", tags=["routes"])

# Dummy data for example purposes
routes_data = [
    {"id": 1, "name": "Route 1", "details": "Details of Route 1"},
    {"id": 2, "name": "Route 2", "details": "Details of Route 2"}
]

@router.get("/routes", response_model=List[dict])
def list_routes():
    return routes_data

@router.get("/routes/{route_id}")
def get_route(route_id: int):
    route = next((route for route in routes_data if route["id"] == route_id), None)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.get("/routes/{route_id}/gpx")
def export_gpx(route_id: int):
    route = next((route for route in routes_data if route["id"] == route_id), None)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    # Placeholder for GPX file generation
    gpx_content = f"<gpx><trk><name>{route['name']}</name><trkseg></trkseg></trk></gpx>"
    return {
        "filename": f"route_{route_id}.gpx",
        "content": gpx_content
    }
