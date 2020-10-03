from flask import Flask
from flask_restful import Api

from resources.model_resource import ModelResource

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

api.add_resource(ModelResource, '/')

if __name__ == '__main__':
    app.run(debug=True)
