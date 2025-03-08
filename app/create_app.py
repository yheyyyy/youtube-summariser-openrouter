from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()  # Load environment variables from .env file

    # Register blueprints or routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app