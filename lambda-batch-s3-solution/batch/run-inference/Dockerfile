# Start from NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV VENV_PATH="/opt/venv"
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="$VENV_PATH/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    ca-certificates \
    wget \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y python3.12 python3.12-venv python3.12-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN python3.12 -m venv $VENV_PATH && \
    . $VENV_PATH/bin/activate && \
    pip install --upgrade pip &&\
    pip install -r requirements.txt

WORKDIR /app
COPY . .

# Test CUDA availability
CMD ["python", "main.py"]
