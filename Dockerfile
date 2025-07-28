FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# use gunicorn to serve the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
