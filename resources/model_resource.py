from flask import request
from flask_restful import Resource
import pickle
import cv2
import os

class ModelResource(Resource):
    def __init__(self):
        with open('MnistNN.pickle', 'rb') as f:
            self.model = pickle.load(f)

    def get(self):
        file = request.files['file']
        file_path = f'uploads/{file.filename}'
        file.save(file_path)

        img = cv2.imread(file_path)
        input_nn = cv2.resize(img[:, :, 0], dsize=(28, 28), interpolation=cv2.INTER_CUBIC).reshape(1, -1) / 255
        res = self.model.predict(input_nn)[0]
        os.remove(file_path)
        return {
            "message": "GangBank welcomes you!",
            "filemame": file.filename,
            'result_nn': res
            }, 200