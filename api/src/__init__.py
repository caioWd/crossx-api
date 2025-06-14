from flask import Flask
from database import db
from config import Config
from src.controllers.user_controller import user_ns
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(
        title='CrossX API',
        version='1.0',
        description='API para gestão da academia',
        prefix="/crossx/api"
    )

    api.init_app(app)
    api.add_namespace(user_ns, path="/users")

    return app


