from flask import Flask, render_template, request, send_from_directory
import requests
import re
import os
from PIL import Image
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# --------------------------------------------------------------------
# VARIABLES
# --------------------------------------------------------------------


# Path to the images directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(ROOT_DIR, 'static/images')

# create directories
os.makedirs(os.path.join(IMAGES_DIR, 'pred'), exist_ok=True)
os.makedirs(os.path.join(IMAGES_DIR, 'resize'), exist_ok=True)

# image directories
SOURCE_DIR = os.path.join(IMAGES_DIR, 'source')
MASK_DIR = os.path.join(IMAGES_DIR, 'masque')
PRED_DIR = os.path.join(IMAGES_DIR, 'pred')
RESIZE_DIR = os.path.join(IMAGES_DIR, 'resize')
PRES_DIR = os.path.join(IMAGES_DIR, 'pres')
PRES_MASK_DIR = os.path.join(IMAGES_DIR, 'pres_mask')

# Path to the generated directory in the backend
PREDICT_API_URL = 'https://projet9backend-fyasgqdcgnewhkck.francecentral-01.azurewebsites.net/predict'

# Input dimensions expected by your Keras model
MODEL_INPUT_WIDTH = 1024
MODEL_INPUT_HEIGHT = 520


# Extract image IDs and names from filenames in the leftimg directory
def extract_image_ids(folder):
    image_ids = []
    image_names = []
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            image_names.append(filename)
            match = re.search(r'_(\d{6})_leftImg8bit', filename)
            if match:
                image_ids.append(int(match.group(1)))

    # Sort lists
    image_names.sort()
    image_ids.sort()

    return image_ids, image_names

image_source_ids, image_source_names = extract_image_ids(SOURCE_DIR)
image_pres_ids, image_pres_names = extract_image_ids(PRES_DIR)
image_pres_mask_ids, image_pres_mask_names = extract_image_ids(PRES_MASK_DIR)


# --------------------------------------------------------------------
# IMAGES AND BASE ROUTE
# --------------------------------------------------------------------

app = Flask(__name__)

@app.route('/images/<image_type>/<path:filename>')
def serve_image(image_type, filename):
    if image_type == 'pres':
        directory = PRES_DIR
    elif image_type == 'pres_mask':
        directory = PRES_MASK_DIR
    elif image_type == 'source':
        directory = SOURCE_DIR
    elif image_type == 'masque':
        directory = MASK_DIR
    elif image_type == 'pred':
        directory = PRED_DIR
    else:
        return "Invalid image type", 404
    return send_from_directory(directory, filename)



# Index page
@app.route('/')
def index():
    return render_template('index.html', image_source_ids=image_source_ids, image_source_names=image_source_names, image_pres_names=image_pres_names, image_pres_mask_names=image_pres_mask_names)


# --------------------------------------------------------------------
# PREDICT AND DISPLAY ROUTES
# --------------------------------------------------------------------

# Prediction route
@app.route('/api/predict', methods=['POST'])
def predict():
    logging.info('----------------------------predict-frontend---------------------------')
    # Get the image URL from the form
    image_url = request.form['image_url']
    # Extract the filename
    real_image_filename = os.path.basename(image_url)
    # Get the image name before suffixe
    base_filename = real_image_filename.rsplit('_', 1)[0]
    # Add the mask suffixe
    real_mask_filename = f'{base_filename}_gtFine_color.png'
    # Add the predicted mask suffixe
    predicted_mask_filename = f'{base_filename}_pred.png'
    # Extract the image ID
    image_id = re.search(r'_(\d{6})_leftImg8bit', real_image_filename).group(1)

    # Resize and save the image
    image = Image.open(f"{SOURCE_DIR}/{real_image_filename}")
    logging.info('--- image opened')
    image = image.resize((MODEL_INPUT_WIDTH, MODEL_INPUT_HEIGHT))
    logging.info('--- image resized')
    image.save(f"{RESIZE_DIR}/{real_image_filename}")
    logging.info('--- image saved')

    # send the image to the API
    with open(f"{RESIZE_DIR}/{real_image_filename}", "rb") as img_file:
        files = {'image': img_file}
        response = requests.post(PREDICT_API_URL, files=files, data={'predicted_mask_filename': predicted_mask_filename})

    logging.info('--- response received')
    img_io = BytesIO(response.content)
    image = Image.open(img_io)
    logging.info('--- image opened')

    resized_image = image.resize((2048,1024), Image.Resampling.LANCZOS)

    save_path = os.path.join(PRED_DIR, predicted_mask_filename)
    resized_image.save(save_path)
    logging.info('--- image saved')

    return render_template('redirect_post.html', image_id=image_id, real_image_filename=real_image_filename, real_mask_filename=real_mask_filename, predicted_mask_filename=predicted_mask_filename)



# Display route 
@app.route('/display', methods=['POST'])
def display():
    logging.info('----------------------------display---------------------------')
    image_id = request.form['image_id']
    real_image_filename = request.form['real_image_filename']
    real_mask_filename = request.form['real_mask_filename']
    predicted_mask_filename = request.form['predicted_mask_filename']

    return render_template('display.html', image_id=image_id, real_image=real_image_filename, real_mask=real_mask_filename, predicted_mask=predicted_mask_filename)

if __name__ == '__main__':
    app.run(debug=True, port=8000)