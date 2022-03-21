from flask import Flask


def create_app():
    app = Flask(__name__)

    from .blueprints.home import homepage
    app.register_blueprint(homepage, url_prefix='/')

    return app


