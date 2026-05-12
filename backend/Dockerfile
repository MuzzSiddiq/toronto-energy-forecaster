FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Fix: Point to the backend folder specifically
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Fix: Copy the contents of the backend folder into the container's /app
COPY backend/ .

# Start the FastAPI server (Note: 'main:app' assumes main.py is now in /app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]