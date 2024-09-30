# speech2text-container

Containerized solution for AI speech-to-text that can run locally

# Prerequisites

Docker installed on your system.

# Building the Docker Image

To build the Docker image, run the following command in the directory containing the Dockerfile:

```bash
    docker build -t speech2text-container .
```

# Running the Docker Container

```bash
docker run -p 2224:2224 speech2text-container
```

# Build and run

```bash
docker-compose up --build
```

# Usage

Send a Request: Send audio data to the exposed endpoint on http://localhost:2224/whisperaudio
Switches for the Python app:

- --host : Host address to run the server on (Default: 0.0.0.0)
- --port : Port number to run the server on (Default: 8000)
- --whispermodel : Whisper model to use for transcription (Default: medium) (https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages)

# Authentication

On server start up you will receive a api key in the console. This key changes on each start up of the software.
When making a request to the server in the headers include a key/value pair with key 'X-API-Key' and value 'You api key from console'.

# License

This project is licensed under the AGPL-3.0 License. See the LICENSE file for details.
