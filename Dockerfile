# Use a slim Python base image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies required by EasyOCR + Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    zlib1g-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Install CPU-only PyTorch (no CUDA)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install Pillow and EasyOCR
RUN pip install --no-cache-dir flask pillow easyocr

# Copy your app code
COPY . .

CMD ["python", "app.py"]
