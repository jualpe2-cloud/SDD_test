class StravaService:
    def exchange_code_for_token(self, code: str) -> dict:
        """Exchange authorization code for access token."""
        # Implementation goes here
        pass

    def get_routes(self, access_token: str) -> list:
        """Get a list of routes from Strava API."""
        # Implementation goes here
        pass

    def get_route_detail(self, access_token: str, route_id: str) -> dict:
        """Get detailed information about a specific route."""
        # Implementation goes here
        pass

    def check_rate_limit(self, access_token: str) -> dict:
        """Check the current rate limit status from Strava API."""
        # Implementation goes here
        pass
