from flask import request
from flask_restful import Resource
import pickle
import cv2
import os
import requests
import base64
import json
import operator
import numpy as np

class ModelResource(Resource):
    def __init__(self):
        with open('MnistNN.pickle', 'rb') as f:
            self.model = pickle.load(f)
        
        self.headers =  {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-IBM-Client-Id": "3a18e76867bf9ea5de2470b8c069cfd2"
        }

        with open('static/special_prices.json', 'r', encoding='utf-8') as f:
            self.special_prices = json.load(f)

        with open('static/model_dict.json', 'r', encoding='utf-8') as f:
            self.model_dict = json.load(f)
        
        with open('static/all_models.json', 'r', encoding='utf-8') as f:
            self.all_models = json.load(f)

        with open('static/model_knn.pkl', 'rb') as f:
            self.model_knn = pickle.load(f)

        self.max_price = 5844330
    

    def get_results(self, best_results):
        result = {
            'hasBestMatch' : True
        }

        mark_best, p_best = best_results[0]
        if mark_best not in self.model_dict or p_best < 0.8:
            result['hasBestMatch'] = False
            result['result'] = self.special_prices
            return result

        result['result'] = [self.model_dict[mark_best]]     
        result['result'].extend(self.neighbors(self.make_feature(self.model_dict[mark_best]), self.model_dict[mark_best]['fullTitle']))
        
        return result

    def neighbors(self, feature, fullTitle):
        neighbors = self.model_knn.kneighbors(feature, return_distance=False).tolist()[0]
        neighbors_models = list(operator.itemgetter(*neighbors)(self.all_models))

        result = [model for model in neighbors_models if fullTitle not in model['fullTitle']]

        return result
    
    def make_feature(self, model):
        return np.array([[model['minPrice'] / self.max_price, model['transportType'] == 'Легковые']])




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
    
    def post(self):
        img = request.files['img']
        b64img = base64.b64encode(img.read())
        body = {
            "content": b64img.decode("utf-8")
        }

        response = requests.post('https://gw.hackathon.vtb.ru/vtb/hackathon/car-recognize', json=body, headers=self.headers)

        response_dict = json.loads(response.content.decode('utf-8'))

        best_results = sorted(response_dict['probabilities'].items(), key=operator.itemgetter(1), reverse=True)[0:5]

        res = self.get_results(best_results)

        return res, 200