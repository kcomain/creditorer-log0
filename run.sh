#!/bin/bash

# Would've setup a venv but doesn't seem to be required.
pip3 install -r requirements.txt
gunicorn --bind "0.0.0.0:$PORT" wsgi:app

