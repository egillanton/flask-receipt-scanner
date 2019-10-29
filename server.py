from flask import Flask, render_template, request, url_for, jsonify, send_file, Response, abort
from flask_fontawesome import FontAwesome
from argparse import ArgumentParser
import os
import sys
import json

import scripts.vision as vision
import scripts.helper as helper


# Init Flask App
app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
fa = FontAwesome(app)


# ======== Routing =========================================================== #
# -------- Home ---------------------------------------------------------- #
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST' and request.json:
        file_name = request.json['file_name']
        attachment_extention = request.json['attachment_extention']
        attachment_data = request.json['attachment_data']

        if not helper.is_valid_file_type(attachment_extention):
            abort(415)

        # Save incoming data to a local file
        file_path = helper.secure_filename(
            f'{file_name}.{attachment_extention}')
        helper.convert_and_save_base64(attachment_data, file_path)

        if helper.is_image(file_path):
            image_path = file_path
        else:
            # Convert file to Image
            image_path = helper.file2img(file_path)

        # OCR Scan
        ocr_text = vision.get_document_text(image_path)
        # Extract receipts values
        receipt_prediction = vision.get_prediction(ocr_text)

        return jsonify(
            vendor=receipt_prediction.vendor,
            address=receipt_prediction.address,
            phone=receipt_prediction.phone,
            date=receipt_prediction.date,
            subtotal=receipt_prediction.subtotal,
            vat=receipt_prediction.vat,
            total=receipt_prediction.total,
            ocr=json.dumps(ocr_text),
        )

    else:
        abort(400)


# ======== Main ============================================================== #
if __name__ == '__main__':
    parser = ArgumentParser(description='Receipt Scanner')
    parser.add_argument("-p", "--port", type=int,
                        metavar="PORT", dest="port", default=5000, help='Port number')
    parser.add_argument("--host", type=str, metavar="HOST",
                        dest="host", default="localhost")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=True)
