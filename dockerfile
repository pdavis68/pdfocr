FROM python:slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get -y install software-properties-common python3 python3-pip poppler-utils tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

COPY src/* .
RUN pip install -r requirements.txt

EXPOSE 5200

CMD ["python3", "app.py"] 