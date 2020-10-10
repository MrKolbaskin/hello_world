from flask import request, send_file
from flask_restful import Resource

class SSLResource(Resource):
    def get(self):
        return send_file('5BF4B06DA0E86C7D0ABFB5B2AF195FAC.txt')