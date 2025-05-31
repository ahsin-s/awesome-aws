# --------------------
# Stage 1: Build stage
# --------------------
FROM python:3.12-slim AS builder

# Set environment
ENV VENV_PATH="/opt/venv"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    libssl-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv $VENV_PATH

# Set workdir and install dependencies
WORKDIR /app
COPY requirements.txt .
RUN . $VENV_PATH/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ----------------------
# Stage 2: Runtime stage
# ----------------------
FROM python:3.12-slim AS runtime

# Set environment
ENV VENV_PATH="/opt/venv"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder $VENV_PATH $VENV_PATH

# Create non-root user (security step)
RUN adduser -D appuser
USER appuser

# Set working directory and copy code
WORKDIR /app
COPY --chown=appuser:appuser . .

# Default command
CMD ["python", "main.py"]
