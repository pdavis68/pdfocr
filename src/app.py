from flask import Flask, request, jsonify
from flask_cors import CORS
from pdf2image import convert_from_path
import pytesseract
import tempfile
import os
import shutil
import logging
from concurrent.futures import ProcessPoolExecutor

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

for logger_name in logging.root.manager.loggerDict:
    logging.getLogger(logger_name).setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app, origins="*")

def process_page(image, page_number):
    logging.debug(f'Processing page {page_number}')
    rgb_image = image.convert("RGB")
    text = pytesseract.image_to_string(rgb_image)
    return {
        "page_number": str(page_number),
        "text": text
    }

def pdf_to_images_concurrently(file):
    logging.debug('Starting PDF to images conversion')
    temp_dir = tempfile.mkdtemp()
    temp_file_name = os.path.join(temp_dir, 'temp.pdf')
    file.save(temp_file_name)
    images = convert_from_path(temp_file_name, fmt='jpg')
    num_pages = len(images)
    shutil.rmtree(temp_dir)
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_page, images, range(1, num_pages + 1)))

    logging.debug('Completed PDF to images conversion')
    return results

@app.route('/pdfocr', methods=['POST'])
def ocr_pdf():
    logging.debug('Received request: /pdfocr')

    if 'file' not in request.files:
        logging.error('No PDF file uploaded')
        return jsonify({'error': 'No PDF file uploaded'}), 400

    file = request.files['file']

    results = pdf_to_images_concurrently(file)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5200)
