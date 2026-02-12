import requests
import os
from dotenv import load_dotenv
import urllib3

# Disable SSL warnings (temporarily for testing)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

class StravaService:
    def __init__(self):
        self.client_id = os.getenv('STRAVA_CLIENT_ID')
        self.client_secret = os.getenv('STRAVA_CLIENT_SECRET')
        self.token_url = "https://www.strava.com/oauth/token"
        
    def exchange_code_for_token(self, code: str) -> dict:
        """Exchange authorization code for access token."""
        try:
            response = requests.post(
                self.token_url,
                data={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'code': code,
                    'grant_type': 'authorization_code'
                },
                verify=False,  # Disable SSL verification
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Strava API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error exchanging code: {e}")
            return None

    def get_routes(self, access_token: str) -> list:
        """Get a list of routes from Strava API."""
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                'https://www.strava.com/api/v3/athletes/routes',
                headers=headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
                
        except Exception as e:
            print(f"Error getting routes: {e}")
            return []

    def get_route_detail(self, access_token: str, route_id: str) -> dict:
        """Get detailed information about a specific route."""
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                f'https://www.strava.com/api/v3/routes/{route_id}',
                headers=headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"Error getting route detail: {e}")
            return None

    def check_rate_limit(self, access_token: str) -> dict:
        """Check the current rate limit status from Strava API."""
        try:
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(
                'https://www.strava.com/api/v3/athlete',
                headers=headers,
                verify=False,
                timeout=10
            )
            
            return {
                'limit': response.headers.get('X-RateLimit-Limit'),
                'usage': response.headers.get('X-RateLimit-Usage')
            }
                
        except Exception as e:
            print(f"Error checking rate limit: {e}")
            return {}
