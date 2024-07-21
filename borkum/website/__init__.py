import json
import os
from pathlib import Path
from flask import Flask
from flask.cli import with_appcontext

from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

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

    with app.app_context():
        (Path(app.config["STORAGE_PATH"]) / "database").mkdir(parents=True, exist_ok=True)
        db.create_all()
        print('Created Database!')

    return app


