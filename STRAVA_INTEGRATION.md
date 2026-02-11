# Strava API Integration Guide

## Overview
This API integrates with Strava API v3 to extract user routes in GPX format for GPS device upload.

## Strava OAuth2 Flow

### Step-by-Step Flow
1. **User Initiation** - User clicks "Connect with Strava" button in frontend
2. **Authorization Redirect** - Frontend redirects to Strava authorization URL
3. **User Authorization** - User approves app access to Strava data
4. **Callback** - Strava redirects back with authorization code
5. **Token Exchange** - Frontend sends code to `POST /auth/login` endpoint
6. **JWT Generation** - Our server exchanges Strava code for token and returns JWT
7. **API Access** - Client uses JWT for subsequent API calls

### Authorization URL
```
https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=route:read_all
```

**Required Scopes:**
- `route:read_all` - Read all routes
- `profile:read_all` - Read athlete profile

## Strava API Endpoints Used

### 1. GET /v3/routes
- **Purpose:** List all routes for authenticated athlete
- **Rate Limit:** Counts towards 600 requests per 15 minutes
- **Response:** Array of route objects with polyline data
- **Our Endpoint:** `GET /routes`

### 2. GET /v3/routes/{id}
- **Purpose:** Get detailed route information including full polyline
- **Rate Limit:** Counts towards 600 requests per 15 minutes
- **Response:** Single route object with complete polyline coordinates
- **Our Endpoint:** `GET /routes/{id}`

### 3. GET /v3/oauth/token (Exchange)
- **Purpose:** Exchange authorization code for access token
- **Method:** POST
- **Parameters:** client_id, client_secret, code, grant_type
- **Rate Limit:** Not rate limited
- **Used by:** `POST /auth/login` endpoint

## Rate Limiting

Strava enforces rate limits:
- **600 requests per 15 minutes** (per authenticated athlete)
- **30,000 requests per day** (per application)

### Rate Limit Headers
```
X-RateLimit-Limit: 600
X-RateLimit-Usage: 150
X-RateLimit-Expiration: 1634313600 (unix timestamp)
```

### Handling Rate Limits
1. Check response headers before making request
2. If approaching limit, return 429 with Retry-After header
3. Implement exponential backoff for retries
4. Cache route data (5-minute TTL) to reduce API calls

## Data Mapping

### Route Object Mapping
```
Strava Route              →  Our API Response
├── id                    →  id
├── name                  →  name
├── description           →  description
├── distance              →  distance (meters)
├── elevation_gain        →  elevation_gain (meters)
├── elevation_high        →  elevation_high (meters)
├── elevation_low         →  elevation_low (meters)
├── type                  →  type (Ride, Run, Walk)
├── created_at            →  created_at (ISO 8601)
├── updated_at            →  updated_at (ISO 8601)
└── map.polyline          →  polyline_summary (base32-encoded)
```

## Polyline Encoding

Strava returns route coordinates as **encoded polyline** (Google's polyline algorithm v5).

### Decoding Process
```python
import polyline

# Strava returns encoded polyline
encoded = "strava_encoded_polyline_here"

# Decode to get lat/lng coordinates
coordinates = polyline.decode(encoded)
# Result: [(37.7749, -122.4194), (37.7750, -122.4193), ...]
```

### GPX Conversion
Decoded coordinates are converted to GPX trackpoints:
```xml
<trkpt lat="37.7749" lon="-122.4194">
  <ele>10</ele>
  <time>2023-10-15T10:30:00Z</time>
</trkpt>
```

## Token Management

### Access Token Storage
- Tokens should NOT be stored permanently
- Store only in memory during active session
- Use refresh tokens to obtain new access tokens
- Clear tokens on logout

### Token Refresh Flow
```
1. Check if token expired
2. If expired, use refresh_token to get new access_token
3. Strava endpoint: POST /v3/oauth/token
4. Return new JWT to client
```

## Error Handling

### Common Strava Errors
| Status | Error | Handling |
|--------|-------|----------|
| 401 | Unauthorized | Invalid/expired Strava token, re-authenticate |
| 403 | Forbidden | User doesn't own route, return 404 |
| 404 | Not Found | Route doesn't exist, return 404 |
| 429 | Rate Limit | Queue request, return 429 with Retry-After |
| 500 | Server Error | Strava API unavailable, return 503 |

### Our API Error Responses
```json
{
  "error": "strava_rate_limit",
  "message": "Strava API rate limit exceeded",
  "details": "Retry after 45 seconds"
}
```

## Testing with Strava Sandbox

Strava provides sandbox environment for testing:
- Use test credentials without impacting real Strava data
- Test auth flow without affecting production

**Configuration:**
```python
STRAVA_ENV = "development"  # Uses sandbox
STRAVA_CLIENT_ID = "sandbox_client_id"
STRAVA_CLIENT_SECRET = "sandbox_secret"
```

## Caching Strategy

### Cache Layers
1. **Route List** - Cache for 5 minutes
2. **Route Detail** - Cache for 5 minutes
3. **Polyline Data** - Cache with route detail

### Cache Invalidation
- Automatic expiration after 5 minutes
- Manual invalidation on user logout
- Manual refresh via query parameter: `?refresh=true`

## Environment Variables Required

```bash
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_REDIRECT_URI=http://localhost:3000/callback
JWT_SECRET=your_jwt_secret
JWT_EXPIRATION=86400  # 24 hours in seconds
```

## Resources

- [Strava API Documentation](https://developers.strava.com/)
- [OAuth 2.0 Specification](https://tools.ietf.org/html/rfc6749)
- [GPX Format Specification](https://www.topografix.com/GPX/1/1/)
- [Polyline Encoding Algorithm](https://developers.google.com/maps/documentation/utilities/polylinealgorithm)