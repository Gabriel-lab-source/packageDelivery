from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///delivery.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Desativa sistema que monitora objetos do banco

    db.init_app(app)

    from app.routes import init_routes
    init_routes(app)

    with app.app_context():
        db.create_all()
    return app
