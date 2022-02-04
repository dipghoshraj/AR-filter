from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit

from flask_cors import CORS, cross_origin
import base64
import json

from lib.image_processor import ImageProcessor

app = Flask(__name__, template_folder='template')
cors = CORS(app)
socketio = SocketIO(app)


@app.route('/index', methods=['POST', 'GET'])
def socket():
    return render_template('index.html')


@app.route('/processing', methods=['POST', 'GET'])
def processing():
    imgencode = ImageProcessor(request.files['image'], request.headers['color'])
    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    response = app.response_class(
        response=json.dumps({'Image': stringData}),
        status=200,
        mimetype='application/json'
    )
    return response


certs_dir = "/etc/letsencrypt/live/ar.dliticx.click/"

if __name__ == '__main__':
    # context = ( os.path.join(certs_dir, 'fullchain.pem'), os.path.join(certs_dir, 'privkey.pem') ) #certificate and key files
    # socketio.run(app, host='0.0.0.0', port= 5000, debug=True, ssl_context=context)
    socketio.run(app, host='0.0.0.0', debug=True, port=5000)
