# pdfocr
Simple app to OCR PDF files.

# Overview

This is a simple flask app that uses pdf2image to convert PDF files to JPEG files and then uses tesseract to OCR the pages. 
The app makes use of the ProcessPoolExecutor so that it can spread the work across multiple CPU, if available.

The app runs on port 5200.

You might prefer running it under something like gunicorn. I run this for my personal use only and so it's not tuned for a production environment at all.

I run it under docker, so:

```
docker-compose build
docker-compose up -d
```

Or you can just run it directly from the source directory, though I'd recommend creating a virtual environment. You'll also need to install Tesseract separately (the dockerfile handles this for you.) If you're running Windows, you can download the executable here: [Tesseract Installer (https://github.com/UB-Mannheim/tesseract/wiki)]. For linux or Mac, you can use: `apt install tesseract-ocr`.

```
python3 -m venv .venv
.\.venv\scripts\activate   # for Windows. For Mac or Linux, use: source ./.venv/bin/activate
cd src
pip install -r requirements.txt
python app.py
```

The `OMP_THREAD_LIMIT=1` bit in the docker-compose.yml is crucial for performance. It makes a 70x or so difference on my machine (3 seconds vs ~220 seconds) when running in a docker container. Otherwise it's unnecessary.
