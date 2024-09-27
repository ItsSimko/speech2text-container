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

# License

This project is licensed under the AGPL-3.0 License. See the LICENSE file for details.
