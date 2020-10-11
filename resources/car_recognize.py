from flask import request
from flask_restful import Resource
import tensorflow
from tensorflow.keras.applications.efficientnet import preprocess_input
import cv2
import numpy as np
import os

model_path = 'efficientnetb0_v1'
model = tensorflow.keras.models.load_model(model_path)

class CarRecognize(Resource):
    def __init__(self):
        self.label_names = ['Hyundai Solaris', 'KIA Rio', 'SKODA OCTAVIA', 'Volkswagen Polo', 'Volkswagen Tiguan']

    def post(self):
        file = request.get_json['content']
        file_path = 'uploads/tmp.jpg'
        
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(imgb64))
        
        file.save(file_path)

        IMG_SIZE = 224
        try:
            img = cv2.resize(cv2.imread(file_path), (IMG_SIZE, IMG_SIZE))
            resized_img = np.expand_dims(img, axis=0)
            proc_img = preprocess_input(resized_img)
            os.remove(file_path)
        except:
            return {'message': "Invalid image"}, 400

        prop = model.predict(proc_img)
        
        dict_result = {}
        for i, label in enumerate(self.label_names):
            dict_result[label] = round(float(prop[0][i]), 5)
        
        return {'probabilities': dict_result}