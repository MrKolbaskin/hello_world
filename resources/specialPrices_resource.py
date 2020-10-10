from flask_restful import Resource
import json

class SpecialPrice(Resource):
    def __init__(self):
        with open('static/special_prices.json', 'r', encoding='utf-8') as f:
            self.special_prices = json.load(f)
    
    def get(self):
        return self.special_prices