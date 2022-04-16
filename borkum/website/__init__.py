import os
from flask import Flask
from .database import db

def create_app():
    app = Flask(__name__)

    # load config 
    app.config.from_object("config.Config")
    db.init_app(app)
    
    from borkum.website.blueprints import home
    from borkum.website.blueprints import location
    from borkum.website.blueprints import gallery
    from borkum.website.blueprints import apartment
    from borkum.website.blueprints import picture_service
    from borkum.website.blueprints import legal_information

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(location, url_prefix='/')
    app.register_blueprint(gallery, url_prefix='/')
    app.register_blueprint(apartment, url_prefix='/')
    app.register_blueprint(picture_service, url_prefix='/')
    app.register_blueprint(legal_information, url_prefix='/')

    return app

def create_database(app):
    if not os.path.exists(app.config['DB_PATH'] + app.config['DB_NAME'] + '.db'):
        with app.app_context():
            db.create_all(app=app)
            print('Created Database!')
