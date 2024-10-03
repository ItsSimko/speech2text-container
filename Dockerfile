# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the Speech2text server code into the container
COPY ./requirements.txt .
COPY ./server.py .
COPY ./utils.py .
COPY ./Caddyfile /etc/caddy/Caddyfile

# Install the required packages for python magic
RUN apt-get update && apt-get install -y \
    libmagic1 \
    && apt-get clean

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 2224

# Command to run the FastAPI application
CMD ["python", "server.py", "--port", "2224"]
        