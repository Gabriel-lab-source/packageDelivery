from app import db
from app.models.driver import Driver
from flask import request
from flask import jsonify
from sqlalchemy import select


def init_routes(app):
    @app.route("/")
    def home():
        return "Hello"

    @app.route("/health")
    def health():
        return {"status": "ok"}

    @app.route("/drivers", methods=["POST"])
    def drivers():
        data = request.get_json()
        driver = Driver(
            name=data.get("name"),
            phone=data.get("phone"),
            vehicle=data.get("vehicle"))
        db.session.add(driver)
        db.session.commit()
        return {"message": "created"}, 201

    @app.route("/drivers", methods=["GET"])
    def list_drivers():
        drivers = db.session.scalars(select(Driver)).all()
        dictDrivers = [driver.to_dict() for driver in drivers]
        return jsonify(dictDrivers)

    @app.route("/drivers/<int:id>", methods=["GET"])
    def get_driver(id):
        driver = db.session.get(Driver, id)
        if not driver:
            return {"error": "Driver not found"}, 404
        result = driver.to_dict()
        return jsonify(result)

    @app.route("/drivers/<int:id>", methods=["PUT"])
    def edit_driver(id):
        driver = db.session.get(Driver, id)
        if not driver:
            return {"error": "Driver not found"}, 404
        data = request.get_json()
        driver.name = data.get("name", driver.name)
        driver.phone = data.get("phone", driver.phone)
        driver.vehicle = data.get("vehicle", driver.vehicle)
        driver.active = data.get("active", driver.active)
        db.session.commit()
        result = driver.to_dict()
        return jsonify(result), 200

    @app.route("/drivers/<int:id>", methods=["DELETE"])
    def delete_driver(id):
        driver = db.session.get(Driver, id)
        if not driver:
            return {"error": "Driver not found"}, 404
        db.session.delete(driver)
        db.session.commit()
        return {"message": "deleted"}
