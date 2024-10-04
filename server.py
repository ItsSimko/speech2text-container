# This software is released under the AGPL-3.0 license
# Copyright (c) 2023-2024 Braedon Hendy

# Further updates and packaging added in 2024 through the ClinicianFOCUS initiative, 
# a collaboration with Dr. Braedon Hendy and Conestoga College Institute of Applied 
# Learning and Technology as part of the CNERG+ applied research project, 
# "Unburdening Primary Healthcare: An Open-Source AI Clinician Partner Platform". 
# Prof. Michael Yingbull (PI), Dr. Braedon Hendy (Partner), 
# and Research Students - Software Developer Alex Simko, Pemba Sherpa (F24), and Naitik Patel.

from torch._C import NoneType
from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Request
from pydantic import BaseModel
from dotenv import load_dotenv
from utils import check_api_key, get_api_key, parse_arguments
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
import whisper
import uvicorn
import os
import tempfile
import magic
import logging

# Load environment variables from a .env file
load_dotenv()

# Check and retrieve the API key
sessionApiKey = check_api_key()

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO)

# Initialize the Whisper model as NoneType
model = NoneType

# set a default rate limit of 5 requests per minute
limiter = Limiter(key_func=get_remote_address, default_limits=["2/second"])  # Example: Limit to 5 requests per minute


# Create a FastAPI application instance
app = FastAPI()
app.state.limiter = limiter

# Define the response model for transcription
class TranscriptionResponse(BaseModel):
    text: str

# Add middleware for rate limiting
@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except RateLimitExceeded as e:
        logging.warning(f"Rate limit exceeded: {e}")
        return PlainTextResponse("Rate limit exceeded. Try again later.", status_code=429)
    


# Define the endpoint for transcribing audio files
@app.post("/whisperaudio", response_model=TranscriptionResponse)
@limiter.limit("5/minute")
async def transcribe_audio(request: Request, file: UploadFile = File(...), api_key: str = Security(get_api_key)):
    """
    Transcribes an uploaded audio file using the Whisper model.

    This endpoint accepts an audio file (MP3 or WAV) and an API key for authentication.
    It validates the file type, saves the file temporarily, transcribes it using the
    Whisper model, and returns the transcribed text.

    Parameters:
    -----------
    file : UploadFile
        The audio file to be transcribed. Must be an MP3 or WAV file.
    api_key : str
        The API key for authentication. Retrieved using the `get_api_key` function.

    Returns:
    --------
    TranscriptionResponse
        A JSON response containing the transcribed text.

    Raises:
    -------
    HTTPException
        - 400: If the uploaded file is not an MP3 or WAV file.
        - 500: If there is an error processing the audio file.

    Example:
    --------
    POST /whisperaudio
    Content-Type: multipart/form-data
    Authorization: Bearer <api_key>

    {
        "file": <audio_file>
    }

    Response:
    {
        "text": "Transcribed text from the audio file."
    }
    """
    # Check if the file is an audio file
    mime = magic.Magic(mime=True)
    file_content = await file.read()
    file_type = mime.from_buffer(file_content)

    if file_type not in ["audio/mpeg", "audio/wav", "audio/x-wav"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an MP3 or WAV file.")

    # Save the audio file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
            contents = await file.read()
            temp_audio_file.write(contents)
            temp_file_path = temp_audio_file.name

        # Process the file with Whisper
        result = model.transcribe(temp_file_path)
        response_data = {"text": result["text"]}
    except Exception as e:
        logging.error(f"Error processing audio file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing audio file: {e}")

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return response_data

# Main entry point for running the Whisper server
if __name__ == '__main__':
    # Parse command-line arguments
    args = parse_arguments()

    # Load the Whisper model using the specified model name
    model = whisper.load_model(args.whispermodel)

    # Check and retrieve the API key
    sessionApiKey = check_api_key()

    # Print the API key for reference
    print(f"Use this API key for requests with bearer header: {sessionApiKey}")

    # Run the Whiser server application using Uvicorn
    uvicorn.run(app, host=args.host, port=args.port)