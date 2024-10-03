# This software is released under the AGPL-3.0 license
# Copyright (c) 2023-2024 Braedon Hendy

# Further updates and packaging added in 2024 through the ClinicianFOCUS initiative, 
# a collaboration with Dr. Braedon Hendy and Conestoga College Institute of Applied 
# Learning and Technology as part of the CNERG+ applied research project, 
# "Unburdening Primary Healthcare: An Open-Source AI Clinician Partner Platform". 
# Prof. Michael Yingbull (PI), Dr. Braedon Hendy (Partner), 
# and Research Students - Software Developer Alex Simko, Pemba Sherpa (F24), and Naitik Patel.

from torch._C import NoneType
from fastapi import FastAPI, File, UploadFile, HTTPException, Security
from pydantic import BaseModel
from dotenv import load_dotenv
from utils import check_api_key, get_api_key, parse_arguments
import whisper
import uvicorn
import os
import tempfile
import magic

load_dotenv()
sessionApiKey = check_api_key()

# Initialize Whisper model
model = NoneType
app = FastAPI()

class TranscriptionResponse(BaseModel):
    text: str


@app.post("/whisperaudio", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...), api_key: str = Security(get_api_key)):
    
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
        raise HTTPException(status_code=500, detail=f"Error processing audio file: {e}")

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return response_data



if __name__ == '__main__':
    args = parse_arguments()

    model = whisper.load_model(args.whispermodel)
    sessionApiKey = check_api_key()

    print(f"Use this API key for requests with bearer header: {sessionApiKey}")

    uvicorn.run(app, host=args.host, port=args.port)
