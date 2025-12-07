FROM python:3.12-slim

# Install Tesseract OCR
RUN apt-get update && apt-get install -y \
    tesseract-ocr libtesseract-dev libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Run Flask app
CMD ["python", "app.py"]
