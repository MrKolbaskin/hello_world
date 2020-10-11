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
import tensorflow

#model_path = 'efficientnetb0_v1'
#model_nn = tensorflow.keras.models.load_model(model_path)

with open('static/model_knn.pkl', 'rb') as f:
    model_knn = pickle.load(f)

class ModelResource(Resource):
    def __init__(self):
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

        self.max_price = 5844330
    

    def get_results(self, best_results, filter_results, us_results):
        result = {
            'hasBestMatch' : True
        }

        mark_best, p_best = best_results
        if mark_best not in self.model_dict or p_best < 0.7:
            mark_best, p_best = us_results
            if mark_best not in self.model_dict or p_best < 0.7:
                result['hasBestMatch'] = False
                result['result'] = self.special_prices
                return result
        
        result['best'] = [self.model_dict[mark_best]]
        result['result'] = [self.model_dict[mark_best]]
        neighbors_models = self.neighbors(
            self.make_feature(self.model_dict[mark_best]),
            self.model_dict[mark_best]['fullTitle'])
        
        result['result'].extend(neighbors_models)
        result['result'] = list(filter(
                lambda x: True \
                    if (filter_results['transportType'] or filter_results['price']) == None \
                        else \
                            ((filter_results['price'] and x['minPrice'] < int(filter_results['price'])) \
                                or \
                                    (filter_results['transportType'] and x['transportType'].lower() == filter_results['transportType'].lower())),
                result['result']
                ))
        
        return result

    def neighbors(self, feature, fullTitle):
        neighbors = model_knn.kneighbors(feature, return_distance=False).tolist()[0]
        neighbors_models = list(operator.itemgetter(*neighbors)(self.all_models))

        result = [model for model in neighbors_models if fullTitle.lower() not in model['fullTitle'].lower()]

        return result
    
    def make_feature(self, model):
        return np.array([[model['minPrice'] / self.max_price, model['transportType'] == 'Легковые']])
    
    def post(self):
        filter_response = {"price": request.form.get('price'), "transportType": request.form.get('transportType')}
        img = request.files['img'].read()
        b64img = base64.b64encode(img)
        body = {
            "content": b64img.decode("utf-8")
        }

        response = requests.post('https://gw.hackathon.vtb.ru/vtb/hackathon/car-recognize', json=body, headers=self.headers)
        second_res = json.loads(requests.post('https://localhost:5000/car-recognize', files={'content': img}).content.decode('utf-8'), verify=False)

        response_dict = json.loads(response.content.decode('utf-8'))
        print(second_res)

        best_results = sorted(response_dict['probabilities'].items(), key=operator.itemgetter(1), reverse=True)[0]
        us_results = sorted(second_res['probabilities'].items(), key=operator.itemgetter(1), reverse=True)[0]

        res = self.get_results(best_results, filter_response, us_results)

        return res, 200