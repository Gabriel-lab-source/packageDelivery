from flask import Flask
from app.extensions import db


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "minha-chave-secreta"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///delivery.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Desativa sistema que monitora objetos do banco

    db.init_app(app)

    from app.routes.driver_routes import driver_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.main_routes import main_bp

    app.register_blueprint(driver_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
    return app
