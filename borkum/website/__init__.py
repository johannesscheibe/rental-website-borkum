from flask import Flask


def create_app():
    app = Flask(__name__)

    from .blueprints.home import home
    from .blueprints.location import location
    from .blueprints.gallery import gallery

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(location, url_prefix='/')
    app.register_blueprint(gallery, url_prefix='/')

    return app


