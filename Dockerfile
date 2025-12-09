FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by psycopg2 and others
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specification and install first (better layer caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Expose app port
EXPOSE 8000

# Use production mode by default inside the container; override as needed
ENV ENVIRONMENT=production

# Start the FastAPI app via uvicorn
CMD ["uvicorn", "src.core.coa_main:app", "--host", "0.0.0.0", "--port", "8000"]
