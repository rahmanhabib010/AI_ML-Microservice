# Import the necessary modules
import requests
import numpy as np
import json
import tensorflow as tf
# Loading data
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# Data preprocessing (here, normalization)
x_train, x_test = x_train / 255.0, x_test / 255.0
# Format the image data so as to be sent as JSON
payload = json.dumps( { 'instances': x_test[:2].tolist() } )
# URL of the TensorFlow Serving container's API
#url = 'http://localhost:8501/v1/models/mymodel:predict' #For docker based service
url = 'http://192.168.49.2:30111/v1/models/mymodel:predict' #For kuburnetes based service
# Send the request
response = requests.post(url, data=payload)
# Parse the response
# prediction =  response.json()["predictions"]
# Print the result
# print(prediction)

prediction =  response.json()

# Extract logits (predictions)
logits = np.array(prediction['predictions'])

# Get the predicted label for each instance (index of max logit)
predicted_labels = np.argmax(logits, axis=1)

print(predicted_labels)
