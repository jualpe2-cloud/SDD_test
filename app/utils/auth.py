import jwt
from datetime import datetime, timedelta
import os

# Secret key to encode and decode the JWT
SECRET_KEY = os.getenv('JWT_SECRET', 'your_secret_key_here')

# Function to create a JWT token

def create_jwt_token(data, expiration_minutes=60):
    expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    data['exp'] = expiration
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

# Function to verify a JWT token

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Function to extract the token from the Authorization header

def extract_token_from_header(header):
    if header.startswith('Bearer '):
        return header.split(' ')[1]
    return None
