FROM python:3.10-slim

# Install system dependencies required for some packages (like lxml)
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt1-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
