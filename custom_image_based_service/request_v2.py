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
payload = json.dumps( { 'instances': x_test[:5].tolist() } )
# URL of the TensorFlow Serving container's API
url = 'http://192.168.49.2:32529/predict' #For kuburnetes based service
# Send the request
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=payload, headers=headers)
#response = requests.post(url, data=payload)


print(response)

prediction =  response.json()

# Get the predicted label in json format for each input instance

print(prediction)

# Get the predicted label for each input instance

print(prediction['predictions'])

