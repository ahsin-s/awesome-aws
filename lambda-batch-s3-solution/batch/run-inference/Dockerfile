# Stage 1: Build and install dependencies
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /install

# Upgrade pip and install dependencies to a temp directory
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir --prefix=/install/deps -r requirements.txt

# Stage 2: Final minimal image
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install/deps /usr/local

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Entrypoint
ENTRYPOINT ["python", "main.py"]
