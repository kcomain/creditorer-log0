import os
import datetime
import requests
from flask import Flask, Response, request, abort

app = Flask(__name__)
#
#
# @app.route('/')
# def root():
#     return 'hi'


@app.route('/logproxy', methods=['post'])
def logproxy():
    if 'file' not in request.files:
        abort(400, {'error': 'Missing required field `file`', 'status': 400})
    if 'filename' not in request.values:
        filename = datetime.datetime.now().strftime('%Y%m%d-%H%M%S%f-') + request.files['file'].filename
    else:
        filename = request.values['filename']
    requests.post(os.environ.get('WEBHOOK_URL'), files={'file': (filename, request.files['file'])})
    return Response(status='204')


if __name__ == '__main__':
    app.run(host='0.0.0.0',)
