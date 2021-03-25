import os
import sys
import datetime
import requests
from flask import Flask, Response, request, abort, __version__

app = Flask(__name__)


@app.route('/')
def root():
    data = [
        "<b>Welcome</b>",
        f"Server is running Flask v{__version__} on Python "
        f"v{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}-{sys.version_info.releaselevel}",
    ]
    return '<br>'.join(data)


@app.route('/logproxy', methods=['post'])
def logproxy():
    # basic gatekeeping
    if not request.authorization:
        abort(401, {'error': 'Authorization header is missing.'})
    if request.authorization.password != os.environ.get('AUTH_PASS'):
        abort(401, {'error': 'You are not authorized to perform this action.'})

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
