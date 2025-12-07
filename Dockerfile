# Use a slim Python base image
FROM python:3.12-slim

WORKDIR /app

RUN pip uninstall -y opencv-python opencv-contrib-python || true

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]