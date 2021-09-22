from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import io
import base64
from PIL import ImageFile
from rembg.bg import remove

ALLOWED_EXTENSIONS = {'jpg'}
UPLOAD_FOLDER = 'app/images'
ImageFile.LOAD_TRUNCATED_IMAGES = True

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
        imageBinary = np.fromfile(file)
        result = remove(imageBinary)
        image = io.BytesIO(result)
        base64Image = "data:image/png;base64,"+base64.b64encode(result).decode('ascii') 
        data = {'image': base64Image}
        response = jsonify(data)
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)