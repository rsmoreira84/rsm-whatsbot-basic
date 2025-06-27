# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for some Python packages (e.g., psycopg2 if you had PostgreSQL)
# For a basic app, this might not be strictly necessary, but good practice.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port your app runs on (e.g., Flask/FastAPI default is 5000 or 8000)
# Adjust if your app uses a different port.
EXPOSE 8000

# Define the command to run your application
# This assumes 'app.py' is your entry point and uses a WSGI server like Gunicorn
# If you are using Flask's built-in server or FastAPI directly, adjust this command.
# For Flask: CMD ["python", "app.py"]
# For FastAPI: CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# Assuming a simple Flask app:
CMD ["python", "app.py"]
