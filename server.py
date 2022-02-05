from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
import base64, json
from lib.image_processor import imageProcessor


app = Flask(__name__, template_folder='template')
cors = CORS(app)
socketio = SocketIO(app)


@app.route('/', methods=['POST', 'GET'])
def socket():
    return render_template('index.html')


@app.route('/processing', methods=['POST', 'GET'])
def processing():
    imgencode = imageProcessor(request.files['image'], request.headers['color'])
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