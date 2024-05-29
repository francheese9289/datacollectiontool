from flask import Flask, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from config import Config
from models import db, User, login_manager, AssessmentScore
from werkzeug.middleware.profiler import ProfilerMiddleware


def init_app():
    '''Initialize Application'''
    app = Flask(__name__)

    #app configuration
    app.config.from_object(Config)

    #plugins
    db.init_app(app) 
    login_manager.init_app(app)
    # ProfilerMiddleware(app)


    #database connection
    migrate = Migrate(app, db)
    CORS(app)

    @app.teardown_appcontext
    def teardown_db(exception=None):
        db.session.remove()
    
    # @app.before_request
    # def print_connection_status():
    #     print("Active connections:", db.engine.pool.status())


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

a = ProfilerMiddleware(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0')



app

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'AssessmentScore': AssessmentScore}

