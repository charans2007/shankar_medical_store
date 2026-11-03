import os
import sys

# Ensure root directory is in sys.path so modules (app, config, models, utils) can be imported by Vercel
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app

# Vercel Serverless Function looks for the WSGI application instance 'app'
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
