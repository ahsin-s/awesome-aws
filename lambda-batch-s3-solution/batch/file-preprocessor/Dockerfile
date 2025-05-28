# --------------------
# Stage 1: Build stage
# --------------------
FROM python:3.11-alpine AS builder

# Set environment
ENV VENV_PATH="/opt/venv"
ENV PATH="$VENV_PATH/bin:$PATH"

# Install build tools and create venv
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
    python3-dev \
    libpq-dev \
    ffmpeg \
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
FROM python:3.11-alpine

# Set environment
ENV VENV_PATH="/opt/venv"
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy virtualenv from builder
COPY --from=builder $VENV_PATH $VENV_PATH

# Create non-root user (security step)
RUN adduser -D appuser
RUN apk add ffmpeg
USER appuser

# Set working directory and copy code
WORKDIR /app
COPY --chown=appuser:appuser . .

ENTRYPOINT ["python", "main.py"]
