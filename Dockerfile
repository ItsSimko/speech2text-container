# Use the official Python image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY ./requirements.txt .
COPY ./server.py .

# Expose the port the app runs on
EXPOSE 2224

# Command to run the FastAPI application
CMD ["python", "server.py", "--port", "2224"]
