from flask import Flask
from flask_restful import Api

from resources.model_resource import ModelResource
from resources.ssl_verification import SSLResource

from OpenSSL import SSL
context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
context.use_privatekey_file('ssl/private.key')
context.use_certificate_file('ssl/certificate.crt')

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

api.add_resource(ModelResource, '/')
api.add_resource(SSLResource, '/.well-known/pki-validation/5BF4B06DA0E86C7D0ABFB5B2AF195FAC.txt')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", ssl_context=context)
