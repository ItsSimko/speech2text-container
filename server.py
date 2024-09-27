# This software is released under the AGPL-3.0 license

from torch._C import NoneType
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import whisper
import uvicorn
import os
import tempfile
import argparse

# Initialize Whisper model
model = NoneType

app = FastAPI()

class TranscriptionResponse(BaseModel):
    text: str

@app.post("/whisperaudio", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    if file.content_type != "audio/mpeg" and file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Invalid content type. Please upload an audio file.")

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
        raise HTTPException(status_code=500, detail="Error processing audio file.")

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return response_data

if __name__ == '__main__':
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="FastAPI server for Whisper audio transcription")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address to run the server on")
    parser.add_argument("--port", type=int, default=8000, help="Port number to run the server on")
    parser.add_argument("--whispermodel", type=str, default="medium", help="Whisper model to use for transcription (https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages)")

    args = parser.parse_args()

    model = whisper.load_model(args.whispermodel)

    uvicorn.run(app, host=args.host, port=args.port)
