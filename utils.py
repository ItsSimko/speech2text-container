# This software is released under the AGPL-3.0 license
# Copyright (c) 2023-2024 Braedon Hendy

# Further updates and packaging added in 2024 through the ClinicianFOCUS initiative, 
# a collaboration with Dr. Braedon Hendy and Conestoga College Institute of Applied 
# Learning and Technology as part of the CNERG+ applied research project, 
# "Unburdening Primary Healthcare: An Open-Source AI Clinician Partner Platform". 
# Prof. Michael Yingbull (PI), Dr. Braedon Hendy (Partner), 
# and Research Students - Software Developer Alex Simko, Pemba Sherpa (F24), and Naitik Patel.

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 

import os
import argparse
import secrets

# Initialize the HTTP Bearer scheme for token authentication
bearer_scheme = HTTPBearer()

def parse_arguments():
    """
    Parses command-line arguments for the FastAPI server.

    Returns:
    --------
    argparse.Namespace
        An object containing the parsed command-line arguments.

    Example:
    --------
    >>> args = parse_arguments()
    >>> print(args.host, args.port, args.whispermodel)
    '0.0.0.0' 2224 'medium'
    """
    # Define default values from environment variables
    default_host = os.getenv("WHISPER_HOST", "0.0.0.0")
    default_port = int(os.getenv("WHISPER_PORT", 2224))
    default_whispermodel = os.getenv("WHISPER_MODEL", "medium")

    # Create an argument parser
    # These overwirte the env, if none passed rely on env/defaults
    parser = argparse.ArgumentParser(description="FastAPI server for Whisper audio transcription")
    parser.add_argument("--host", type=str, default=default_host, help="Host address to run the server on")
    parser.add_argument("--port", type=int, default=default_port, help="Port number to run the server on")
    parser.add_argument("--whispermodel", type=str, default=default_whispermodel, help="Whisper model to use for transcription")
    
    return parser.parse_args()

def generate_api_key():
    """
    Generates a secure API key.

    This function uses the `secrets` module to generate a secure, URL-safe
    API key. The key is 32 characters long.

    Returns:
    --------
    str
        A securely generated API key.

    Example:
    --------
    >>> api_key = generate_api_key()
    >>> print(api_key)
    'aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890'
    """
    return secrets.token_urlsafe(32)

def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    """
    Retrieves and validates the API key from the request headers.

    This function retrieves the API key from the request headers using the
    `HTTPBearer` scheme. It checks if the provided token matches the one stored
    in the environment variable `SESSION_API_KEY`. If the token is invalid or
    missing, it raises an HTTPException with a 401 status code.

    Parameters:
    -----------
    credentials : HTTPAuthorizationCredentials
        The credentials extracted from the request headers.

    Returns:
    --------
    str
        The validated API key.

    Raises:
    -------
    HTTPException
        401: If the provided token is invalid or missing.

    Example:
    --------
    >>> api_key = get_api_key(credentials)
    >>> print(api_key)
    'aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890'
    """
    token = credentials.credentials
    if token == os.getenv('SESSION_API_KEY'):
        return token
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing Bearer Token",
    )

def check_api_key():
    """
    Checks and retrieves the API key from the environment variables.

    This function checks if the `SESSION_API_KEY` environment variable is set.
    If not, it generates a new API key and sets it in the environment variables.

    Returns:
    --------
    str
        The API key stored in the environment variables.

    Example:
    --------
    >>> api_key = check_api_key()
    >>> print(api_key)
    'aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890'
    """
    api_key = os.getenv('SESSION_API_KEY')

    if not api_key:
        # If not found, generate a new one and every session
        api_key = generate_api_key()
        os.environ['SESSION_API_KEY'] = api_key
    
    return api_key