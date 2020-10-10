from flask import request
from flask_restful import Resource

class SSLResource(Resource):
    def get(self):
        with open('5BF4B06DA0E86C7D0ABFB5B2AF195FAC.txt', 'r') as f:
            return f.read(), 200