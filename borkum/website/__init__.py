import json
import os
from flask import Flask
from flask.cli import with_appcontext
from .database import db, db_service

def create_app():
    app = Flask(__name__)

    # load config 
    app.config.from_object("config.Config")
    db.init_app(app)
    
    from borkum.website.blueprints import admin
    from borkum.website.blueprints import home
    from borkum.website.blueprints import location
    from borkum.website.blueprints import gallery
    from borkum.website.blueprints import rental_object
    from borkum.website.blueprints import image_service
    from borkum.website.blueprints import legal_information

    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(location, url_prefix='/')
    app.register_blueprint(gallery, url_prefix='/')
    app.register_blueprint(rental_object, url_prefix='/')
    app.register_blueprint(image_service, url_prefix='/')
    app.register_blueprint(legal_information, url_prefix='/')

    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        db.create_all()
        print('Created Database!')

