from flask import Flask, jsonify
import os
from dotenv import load_dotenv  # noqa: F401 — load environment variables from .env file
from app.controllers import routes  # noqa: F401 — register routes for Flask application
from app.extensions import db, migrate  # noqa: F401 — register db and migrate for Flask-Migrate
import app.repositories.models  # noqa: F401 — register models for Flask-Migrate

load_dotenv()


# Flask application configuration class
class ConfigClass(object):
    """ Flask application config """

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# Function to add error handlers to the Flask application
def add_error_handler(app):
    # Return validation errors as JSON
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code


# Factory function to create and configure the Flask application
def create_app():
    my_app = Flask(__name__)
    my_app.config.from_object(ConfigClass)
    add_error_handler(my_app)
    db.init_app(my_app)
    migrate.init_app(my_app, db)

    my_app.register_blueprint(routes)

    return my_app


if __name__ == "__main__":
    print("Starting Flask application...")
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=8080,
        use_reloader=False,
    )
