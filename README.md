# pdfocr
Simple app to OCR PDF and image files. Runs as a web api service on port 5200. The endpoints are /pdfocr and /imageocr. 

For /pdfocr, you pass in a PDF file and it returns the OCRed text as a JSON array of pages with a `page_number` and `text` fields.

`curl --location 'localhost:5200/pdfocr' --form 'file=@"/C:/documents/mydocument.pdf"'`

/imageocr is the same, except you pass an image (jpeg, png, gif, etc) and it will be OCRed.

You can run it in docker as I do, or you can run it directly with `python app.py`.

# Overview

This is a simple flask app that uses pdf2image to convert PDF files to JPEG files and then uses tesseract to OCR the pages. 
The app makes use of the ProcessPoolExecutor so that it can spread the work across multiple CPU, if available.

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

The `OMP_THREAD_LIMIT=1` bit in the docker-compose.yml is crucial for performance. It makes a 70x or so difference on my machine (3 seconds vs ~220 seconds) when running in a docker container. It's only needed in docker containers, though.

# Performance

Tesseract seems very performant for CPU-based OCR work and its quality is excellent. A multicore machine will make a big difference. I have an i7-3770 with 4 cores and 8 logical processors running at 3.4GHz. It generally averages less than 1 page per second (if you're doing more than 8 pages). So it's really taking about 8 seconds per page, but doing 8 pages at once. I find this performance to be more than adequate for my needs. With the default settings I was able to do a 620 page document in 8 minutes and 28 seconds (.8 seconds/page) running in a docker container.
Performance is also why I chose the `python:slim` base image.
