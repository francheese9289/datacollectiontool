from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, login_manager


def init_app():
    '''Initialize Application'''
    app = Flask(__name__)

    #app configuration
    app.config.from_object(Config)

    #plugins
    db.init_app(app) 
    login_manager.init_app(app)

    #database connection
    migrate = Migrate(app, db)
    CORS(app)
    

    with app.app_context():
        # blueprints 
        from .main.routes import main
        from .authentication.routes import auth
        from .api.routes import api
        
        # register blueprints
        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(api)

        # dash app
        #might change to blueprint?
        from .app_dash.dashboard import init_dashboard
        init_dashboard(app)
        

    return app

