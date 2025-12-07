# Use a slim Python base image
FROM python:3.12-slim

WORKDIR /app

# Source - https://stackoverflow.com/a
# Posted by Awanish Kumar Golwara
# Retrieved 2025-12-07, License - CC BY-SA 4.0

RUN apt-get update && apt-get install libgl1


# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]