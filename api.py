from flask import Flask
from flask_restful import Api

from resources.model_resource import ModelResource

app = Flask(__name__)
api = Api(app)

api.add_resource(ModelResource, '/')

if __name__ == '__main__':
    app.run(debug=True)
