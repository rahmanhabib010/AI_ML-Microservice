import tensorflow as tf
import json
from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.preprocessing import image
from datetime import datetime
import os

app = Flask(__name__)

# Load the saved model
model = tf.keras.models.load_model('./mymodel/v1/mnist_model.h5')

# Get the last modified date of the model file
model_path = './mymodel/v1/mnist_model.h5'
last_modified_timestamp = os.path.getmtime(model_path)
last_modified_date = datetime.fromtimestamp(last_modified_timestamp).strftime('%Y-%m-%d')

model_metadata = {
    "model_name": "MNIST Digit Classifier",
    "version": "1.0",
    "description": "A simple MNIST digit classifier built with TensorFlow/Keras.",
    "input_shape": model.input_shape,
    "output_classes": 10,
    "framework": "TensorFlow/Keras",
    "last_updated": last_modified_date  # Set to current date
}


@app.route('/predict', methods=['POST'])
def predict():
    # Get the image as dictionary from the POST request
    # request.get_json() will return the Python dictionary
    # payload = request.get_json()  # Assuming image data is in JSON format
    
    # Try to get the JSON payload from the request
    try:
        payload = request.get_json(force=True)  # force=True allows us to parse the body as JSON even without 'Content-Type: application/json'
    except Exception as e:
        return jsonify({"error": "Invalid JSON data"}), 400

    data = payload.get('instances', [])
        
    if len(data) == 0:
        return jsonify({'error': 'No instances found in the request'}), 400

    # Convert the data into a NumPy array
    img_data = np.array(data)

    # Perform inference
    predictions = model.predict(img_data)

    # Get the predicted class (index of the highest score)
    predicted_class = np.argmax(predictions, axis=1)

    return jsonify({'predictions': predicted_class.tolist()})

# New route to provide model metadata
@app.route('/metadata', methods=['GET'])
def metadata():
    return jsonify(model_metadata)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
