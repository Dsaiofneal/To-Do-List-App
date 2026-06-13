from flask import Flask

from database.connection import init_db
from routes.api import api_bp
from routes.views import views_bp


def create_app():
    app = Flask(__name__)

    # Initialize the database
    init_db()

    # Register blueprints
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
