FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]

