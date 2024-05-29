from app import init_app
import os


app = init_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    app.config['ENV'] = 'production'
    # Run the Flask application
    app.run()

