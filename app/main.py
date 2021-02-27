from flask import Flask, request, jsonify
from PIL import Image
import base64
import io
import os
import glob
import numpy as np
from PIL import Image as Img
from PIL import ImageFilter
import cv2
from app.u2net_test import main as model

ALLOWED_EXTENSIONS = {'jpg'}
UPLOAD_FOLDER = 'images'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    # xxx.png
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/crop', methods=['POST'])

def crop():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})

        img_bytes = file.read()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        main()
        image = actions()
        data = {'stats': image}
        return jsonify(data)
    #move images to /images directory
    #run the model
    #process each image and from /results
    #convert each image to base64
    #return image array in JSON
    #delete the /images and /results directory content



def actions():
    image_dir = os.path.join(os.getcwd(), 'images')
    names = [name[:-4] for name in os.listdir(image_dir)]
    THRESHOLD = 0.9
    RESCALE = 255
    LAYER = 2
    COLOR = (0, 0, 0)
    THICKNESS = 4
    SAL_SHIFT = 100
    for name in names:
        # BACKGROUND REMOVAL
        output = Image.open('results/'+name+'.png')
        out_img = np.array(output, np.float64)
        out_img /= RESCALE

        out_img[out_img > THRESHOLD] = 1
        out_img[out_img <= THRESHOLD] = 0

        shape = out_img.shape
        a_layer_init = np.ones(shape = (shape[0],shape[1],1))
        mul_layer = np.expand_dims(out_img[:,:,0],axis=2)
        a_layer = mul_layer*a_layer_init
        rgba_out = np.append(out_img,a_layer,axis=2)

        input = Image.open('images/'+name+'.jpg')
        inp_img = np.array(input, np.float64)
        inp_img /= RESCALE

        a_layer = np.ones(shape = (shape[0],shape[1],1))
        rgba_inp = np.append(inp_img,a_layer,axis=2)

        rem_back = (rgba_inp*rgba_out)
        rem_back_scaled = rem_back*RESCALE

        # OUTPUT RESULTS
        rem_back = cv2.resize(rem_back_scaled,(int(shape[1]/3),int(shape[0]/3)))
        result_img = Img.fromarray(rem_back.astype('uint8'), 'RGBA')
        result_img = result_img.filter(ImageFilter.SMOOTH)

        return result_img
    
   