from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    from app.routes import init_routes
    init_routes(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///delivery.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
