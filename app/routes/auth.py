from fastapi import APIRouter, HTTPException, status
from app.models.schemas import AuthRequest, AuthResponse
from app.services.strava_service import StravaService
from app.utils.auth import create_jwt_token
import os

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

strava_service = StravaService()

@router.post("/login", response_model=AuthResponse)
async def oauth_login(request: AuthRequest):
    """
    FR3.1: OAuth2 Authentication with Strava
    Exchange authorization code for JWT token
    """
    try:
        # Exchange code for Strava access token
        token_response = strava_service.exchange_code_for_token(request.code)
        
        if token_response is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid authorization code"
            )
        
        # Extract athlete info and create JWT
        athlete_id = token_response.get('athlete', {}).get('id')
        
        # Create JWT token with athlete info
        jwt_token = create_jwt_token({
            "athlete_id": athlete_id,
            "access_token": token_response.get('access_token')
        })
        
        return AuthResponse(
            access_token=jwt_token,
            token_type="Bearer",
            expires_in=86400  # 24 hours
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )

@router.post("/refresh")
async def refresh_token(authorization: str):
    """
    Refresh JWT token
    """
    # TODO: Implement token refresh logic
    pass

@router.post("/logout")
async def logout():
    """
    Logout user
    """
    # TODO: Implement logout logic (clear tokens, etc.)
    pass
