from flask import Flask
from datetime import datetime


def create_app():
    app = Flask(__name__)

    # load config 
    app.config.from_object("config.Config")
    
    # Context processor for template variables
    @app.context_processor
    def inject_year():
        return {'current_year': datetime.now().year}
    
    from borkum.website.blueprints import home
    from borkum.website.blueprints import location
    from borkum.website.blueprints import gallery
    from borkum.website.blueprints import apartment
    from borkum.website.blueprints import picture_service
    from borkum.website.blueprints import legal_information
    from borkum.website.blueprints import seo

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(location, url_prefix='/')
    app.register_blueprint(gallery, url_prefix='/')
    app.register_blueprint(apartment, url_prefix='/')
    app.register_blueprint(picture_service, url_prefix='/')
    app.register_blueprint(legal_information, url_prefix='/')
    app.register_blueprint(seo, url_prefix='/')

    return app


