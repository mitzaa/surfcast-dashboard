FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app.py and any other necessary files from backend directory to /app inside the container
COPY app.py .

CMD ["python", "app.py"]
