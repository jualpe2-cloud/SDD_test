# FR1.2 - Get Route Details

## Description
This feature allows users to retrieve detailed information about a specific route based on the route ID.

## Preconditions
- The user must be authenticated.
- The route ID must be valid and exist in the database.

## Postconditions
- The details of the requested route are returned in the response.

## Process
1. The user sends a request to the `GET /routes/{routeId}` endpoint, providing the valid route ID.
2. The system verifies the user's authentication and validates the route ID.
3. If authenticated and valid, the system retrieves the route details from the database.
4. The system returns the route details in JSON format:
   - `routeId`: (string) ID of the route.
   - `routeName`: (string) Name of the route.
   - `startLocation`: (string) Starting point of the route.
   - `endLocation`: (string) Ending point of the route.
   - `distance`: (float) Total distance of the route.
   - `duration`: (float) Estimated time to traverse the route.

## Error Handling
- If the user is not authenticated, return a `401 Unauthorized` status.
- If the route ID is invalid, return a `404 Not Found` status.
- If there is a server error, return a `500 Internal Server Error` status.

## Example Request
```
GET /routes/12345
Authorization: Bearer {token}
```

## Example Response
```json
{
  "routeId": "12345",
  "routeName": "Route 66",
  "startLocation": "Chicago",
  "endLocation": "Los Angeles",
  "distance": 2445.0,
  "duration": 43.5
}
```