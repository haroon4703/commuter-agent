FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Spaces uses PORT environment variable (default 7860)
# Expose the port (will be set by Hugging Face)
EXPOSE ${PORT:-7860}

# Use the PORT environment variable, fallback to 7860 for Hugging Face
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860}
