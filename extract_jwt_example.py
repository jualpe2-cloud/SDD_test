"""
Example: How to extract athlete_id from JWT token
"""

import jwt

# Your JWT token from the response
jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdGhsZXRlX2lkIjo0ODQ1MzU0LCJhY2Nlc3NfdG9rZW4iOiI0YTA1YmVhZDYyZjUxY2YxMDdlOWFkNzg0N2Y1YWM4ZGM3YTEyNzNhIiwiZXhwIjoxNzcwODk2ODc1fQ.pMxtN36NMMFxniS4J5Q4bip1gughWq-VKWlQz_m8ruQ"

# Decode the JWT (without verifying signature for this example)
# In production, you should verify it with the secret key
decoded = jwt.decode(jwt_token, options={"verify_signature": False})

print("Decoded JWT contents:")
print(f"Athlete ID: {decoded['athlete_id']}")
print(f"Strava Access Token: {decoded['access_token']}")
print(f"Expiration timestamp: {decoded['exp']}")
print(f"\nYour Athlete ID is: {decoded['athlete_id']}")
