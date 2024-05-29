from app import init_app
import os
from gunicorn.app.base import BaseApplication

class FlaskApplication(BaseApplication):
    def __init__(self, app):
        self.application = app
        super().__init__()

    def load_config(self):
        pass
    # self.cfg.set("workers", 2)
    # self.cfg.set("timeout", 30)

    def load(self):
        return self.application

app = init_app()

if __name__ == "__main__":
    # Set Flask environment to production
    os.environ['FLASK_ENV'] = 'production'

    # Run the Flask application using Gunicorn
    FlaskApplication(app).run()
