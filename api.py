from flask import Flask
from flask_restful import Api
import ssl

from resources.model_resource import ModelResource
from resources.ssl_verification import SSLResource
from resources.specialPrices_resource import SpecialPrice
from resources.car_recognize import CarRecognize

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain('ssl/certificate.crt', 'ssl/private.key')

api.add_resource(ModelResource, '/')
#api.add_resource(SSLResource, '/.well-known/pki-validation/5BF4B06DA0E86C7D0ABFB5B2AF195FAC.txt')
api.add_resource(SpecialPrice, '/specialsprices')
api.add_resource(CarRecognize, '/car-recognize')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0", ssl_context=context)

#host="0.0.0.0" ssl_context=context