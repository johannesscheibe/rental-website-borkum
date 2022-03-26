from flask import Flask


def create_app():
    app = Flask(__name__)

    # load config 
    app.config.from_object("config.Config")
    
    from borkum.website.blueprints import home
    from borkum.website.blueprints import location
    from borkum.website.blueprints import gallery
    from borkum.website.blueprints import apartment
    from borkum.website.blueprints import picture_service

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(location, url_prefix='/')
    app.register_blueprint(gallery, url_prefix='/')
    app.register_blueprint(apartment, url_prefix='/')
    app.register_blueprint(picture_service, url_prefix='/')

    return app


