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

    @app.teardown_appcontext
    def teardown_db(exception=None):
        db.session.remove()
    
    @app.before_request
    def print_connection_status():
        print("Active connections:", db.engine.pool.status())


    with app.app_context():
        # blueprints 
        from .main.routes import main
        from .authentication.routes import auth
        from .api.routes import api
        
        # register blueprints
        app.register_blueprint(main)
        app.register_blueprint(auth)
        app.register_blueprint(api)

    return app



app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

app
