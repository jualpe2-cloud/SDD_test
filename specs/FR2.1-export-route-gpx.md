# Specification: FR2.1 - Export Route as GPX

## Requirement ID
FR2.1

## Title
Export Route as GPX (GPS Exchange Format)

## Description
Authenticated users can export any of their Strava routes as a GPX file, which is compatible with popular GPS devices like Garmin and Wahoo, enabling them to upload routes directly to their devices for navigation.

## User Story
As a cyclist/runner I want to export my Strava route as a GPX file So that I can upload it to my GPS device (Garmin, Wahoo, etc.)

## Acceptance Criteria
- User can request route export via GET /routes/{id}/gpx
- Response includes valid GPX 1.1 formatted XML
- GPX file includes route coordinates (latitude, longitude, elevation)
- GPX file includes metadata: name, description, waypoints
- Response headers set Content-Type: application/gpx+xml
- Response headers set Content-Disposition for file download
- File downloads with meaningful filename (e.g., route_name.gpx)
- Unauthorized users (no valid token) receive 401 error
- Non-existent routes receive 404 error
- Routes with 1000+ waypoints process correctly
- Response completes within 5 seconds
- Strava API rate limits are not exceeded
- Output compatible with Garmin devices
- Output compatible with Wahoo devices

## Technical Details

### Data Source
Strava API: GET /v3/routes/{id}
Strava returns polyline-encoded coordinates

### GPX Schema Mapping
Strava Route Object → GPX Element
- id → metadata/name + trk/name
- name → metadata/name
- distance → trk/extensions/distance
- elevation_gain → extensions/elevationGain
- map.polyline → trk/trkseg/trkpt (coordinates)
- created_at → metadata/time
- type → metadata/type + extensions/activity

## Response Example

Request: GET /api/v1/routes/12345/gpx Authorization: Bearer {token}

Response (200 OK): Valid GPX 1.1 XML with route coordinates and metadata

## Device Compatibility

### Garmin Compatibility
- Tested devices: Fenix 7, Edge 1040, Instinct 2
- Format: GPX 1.1
- Notes: Elevation data is critical for proper display

### Wahoo Compatibility
- Tested devices: Elemnt Bolt, Elemnt Roam
- Format: GPX 1.1
- Notes: Include trackpoint times for accurate playback

## Error Scenarios
- 400 Bad Request: Invalid route ID format
- 401 Unauthorized: Missing or invalid token
- 404 Not Found: Route ID doesn't exist or user doesn't have access
- 429 Too Many Requests: Strava rate limit hit
- 500 Server Error: Strava API unavailable

## Implementation Notes
- Use polyline library to decode Strava's polyline format
- Use gpxpy (Python) library to generate GPX
- Cache route data for 5 minutes to reduce Strava API calls
- Stream response for large routes (1000+ waypoints)
- Validate GPX output against GPX 1.1 schema before returning