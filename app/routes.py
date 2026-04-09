from app import db
from app.models.driver import Driver
from flask import request
from flask import jsonify
from sqlalchemy import select
from app.models.deliveries import Delivery


def init_routes(app):
    @app.route("/")
    def home():
        return "Hello"

    @app.route("/health")
    def health():
        return {"status": "ok"}

    @app.route("/drivers", methods=["POST"])
    def insert_drivers():

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

    @app.route("/deliveries", methods=["POST"])
    def insert_deliveries():
        data = request.get_json()

        driver = db.session.get(Driver, data.get("driver_id"))

        delivery = Delivery(
            description=data.get("description"),
            origin_address=data.get("origin_address"),
            destination_address=data.get("destination_address"),
            status=data.get("status"),
            driver=driver
        )

        db.session.add(delivery)

        db.session.commit()

        return {"message": "created"}, 201

    @app.route("/deliveries", methods=["GET"])
    def list_deliveries():

        deliveries = db.session.scalars(select(Delivery)).all()
        dict_deliveries = [package.to_dict() for package in deliveries]
        return jsonify(dict_deliveries)

    @app.route("/deliveries/<int:id>", methods=["GET"])
    def get_package(id):

        package = db.session.get(Delivery, id)

        if not package:
            return {"error": "Package not found"}, 404

        result = package.to_dict()
        return jsonify(result)

    @app.route("/deliveries/<int:id>", methods=["PUT"])
    def edit_package(id):

        delivery = db.session.get(Delivery, id)

        if not delivery:
            return {"error": "Package not found"}, 404

        data = request.get_json()

        if "description" in data:
            delivery.description = data["description"]

        if "origin_address" in data:
            delivery.origin_address = data["origin_address"]

        if "destination_address" in data:
            delivery.destination_address = data["destination_address"]

        if "status" in data:
            delivery.status = data["status"]

        if "driver" in data:
            delivery.driver_id = data["driver"]

        db.session.commit()

        return jsonify(delivery.to_dict())

    @app.route("/deliveries/<int:id>", methods=["DELETE"])
    def delete_package(id):

        package = db.session.get(Delivery, id)

        if not package:
            return {"error": "Package not found"}, 404

        db.session.delete(package)

        db.session.commit()

        return {"message": "deleted"}

    @app.route("/drivers/<int:id>/deliveries", methods=["GET"])
    def get_driver_deliveries(id):

        driver = db.session.get(Driver, id)

        if not driver:
            return {"error": "Driver not found"}, 404

        deliveries = [package.to_dict() for package in driver.deliveries]

        return jsonify(deliveries)
