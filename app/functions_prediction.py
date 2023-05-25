import numpy as np
import pandas as pd
import csv
import cv2
from keras.models import load_model 
from keras.utils import img_to_array
import requests


def predict_class(image, image_size=(160,160)):

    '''
    Function takes image as input to: resize, transform to numpy array, scales and predict.

    Input: image and size (default (160,160))
    Output: predicted class

    '''
    # load model:
    model = load_model('../Models/cnn_mobilnet.h5', compile=True)
    # Resize the image using OpenCV
    #image = cv2.imread(image)
    image = cv2.cvtColor(np.float32(image), cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(image, image_size)

    # Convert the image to a NumPy array
    input_arr = img_to_array(resized_image)
    image_array = np.array([input_arr], dtype = 'float32')

    # make predictions
    predictions = model.predict(image_array)
    pred_label = np.argmax(predictions, axis = 1)

    # classes
    classes = ['Glass', 'Organic', 'Paper', 'Recycling Point', 'Yellow']

    predicted_class = classes[pred_label[0]]

    
    return predicted_class

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_data():
    data = pd.read_csv('counter_vertical.csv')
    return data


def update_csv(file_path, result):
    # Read the CSV file and update the appropriate values based on the result
    rows = []

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        rows = list(reader)

        # Update the values for the matching class in the 'values' column
        for row in rows:
            if row['classes'] == result:
                if row['values'].isdigit():
                    row['values'] = str(int(row['values']) + 1)

    # Write the updated values back to the CSV file
    with open(file_path, 'w', newline='') as file:
        fieldnames = ['classes', 'values']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)