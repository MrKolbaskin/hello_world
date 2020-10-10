from flask import Flask
from flask_restful import Api
from flask_sslify import SSLify
import ssl

from resources.model_resource import ModelResource
from resources.ssl_verification import SSLResource

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain('ssl/certificate.crt', 'ssl/private.key')

api.add_resource(ModelResource, '/')
api.add_resource(SSLResource, '/.well-known/pki-validation/5BF4B06DA0E86C7D0ABFB5B2AF195FAC.txt')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", ssl_context=context, port=5000)
