from flask import Flask
from .db import create_table_if_not_exists
from .routes import register_routes


def create_app():
    app = Flask(__name__)

    # Set up the database table
    with app.app_context():
        create_table_if_not_exists()

    # Register all routes onto the app
    register_routes(app)

    return app