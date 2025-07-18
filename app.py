from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import io

app = Flask(__name__)
CORS(app)

# Load model
model = load_model('waste_classifier_cnn.h5')
class_names = {0: "Organic", 1: "Recyclable"}  # Adjust based on your dataset
IMG_SIZE = 150

def preprocess(img):
    img = img.resize((IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    return np.expand_dims(img_array, axis=0)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    img_file = request.files['file']
    img_bytes = img_file.read()
    img = image.load_img(io.BytesIO(img_bytes), target_size=(IMG_SIZE, IMG_SIZE))


    input_arr = preprocess(img)
    prediction = model.predict(input_arr)[0][0]
    
    predicted_label = class_names[int(prediction > 0.5)]
    confidence = float(prediction) if predicted_label == "Recyclable" else float(1 - prediction)

    return jsonify({"predictedLabel": predicted_label, "confidence": confidence})

if __name__ == '__main__':
    app.run(debug=True)
