from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import io
import os
import glob
from PIL import Image
from rembg.bg import remove

ALLOWED_EXTENSIONS = {'jpg'}
UPLOAD_FOLDER = 'app/images'

app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CORS_HEADERS'] = 'Content-Type'


def allowed_file(filename):
    # xxx.png
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/crop', methods=['POST'])
@cross_origin(origin='*', allow_headers=['Content-Type'])

def crop():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})
        print(file)
        result = remove(file)
        data = {'image': result}
        response = jsonify(data)
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')