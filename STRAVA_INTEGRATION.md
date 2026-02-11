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
