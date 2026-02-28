# Use official Python image
FROM python:3.11-slim
# Prevent Python from writing pyc files & enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
# Upgrade pip
RUN pip install --upgrade pip
# Copy requirements first (for Docker layer caching)
COPY requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy project files
COPY . .
# Create non-root user for security
RUN useradd -m appuser
USER appuser
# Expose application port
EXPOSE 5000
# Health check
HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1
# Run application
CMD ["python", "app.py"]
