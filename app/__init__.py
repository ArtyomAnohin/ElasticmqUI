import os
from flask import Flask

from app.route import application


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.register_blueprint(application)
    filename = os.path.join(app.instance_path, 'application.cfg')
    return app

