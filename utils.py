from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 


import os
import argparse
import secrets

bearer_scheme = HTTPBearer()

def parse_arguments():
    parser = argparse.ArgumentParser(description="FastAPI server for Whisper audio transcription")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address to run the server on")
    parser.add_argument("--port", type=int, default=2224, help="Port number to run the server on")
    parser.add_argument("--whispermodel", type=str, default="medium", help="Whisper model to use for transcription")
    
    return parser.parse_args()

def generate_api_key():
    return secrets.token_urlsafe(32)

def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    token = credentials.credentials
    if token == os.getenv('SESSION_API_KEY'):
        return token
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing Bearer Token",
    )

def check_api_key():
    api_key = os.getenv('SESSION_API_KEY')

    if not api_key:
        # If not found, generate a new one and every session
        api_key = generate_api_key()
        os.environ['SESSION_API_KEY'] = api_key
    
    return api_key
