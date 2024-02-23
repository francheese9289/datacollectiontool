from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
# from flask_session import Session
from config import Config
from models import db, login_manager
# session = Session()

def init_app():
    '''initialize application'''
    app = Flask(__name__)

    #app configuration
    app.config.from_object(Config)

    #plugins
    db.init_app(app) 
    # session.init_app(app)
    login_manager.init_app(app)

    #database connection
    migrate = Migrate(app)
    CORS(app)
    

    with app.app_context():
        # Blueprints 
        from .main.routes import main
        from .authentication.routes import auth
        from .api.routes import api
        
        # Register blueprints
        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(api)

        # Bring in Dash app
        from .app_dash.dashboard import init_dashboard
        init_dashboard(app)
        

    return app

