from app import db
from app.models.driver import Driver
from app.models.delivery import Delivery
from app.services.geolocation import get_coordinates, get_route
from sqlalchemy import select
from flask import request, jsonify, render_template, redirect, url_for


def init_routes(app):
    @app.route("/")
    def home():
        return "Hello"

    @app.route("/health")
    def health():
        return {"status": "ok"}

    @app.route("/create-driver", methods=["GET", "POST"])
    def create_driver():

        if request.method == "POST":
            new_driver = Driver(
                name=request.form.get("name"),
                phone=request.form.get("phone"),
                vehicle=request.form.get("vehicle")
            )

            db.session.add(new_driver)
            db.session.commit()

            return redirect(url_for("create_driver", message="Motorista criado com sucesso"))

        success = request.args.get("success")
        return render_template("create-driver.html", success=success)

    @app.route("/list-drivers", methods=["GET"])
    def list_drivers():

        drivers = db.session.scalars(select(Driver)).all()
        return render_template("get-drivers.html", drivers=drivers)

    @app.route("/list-driver/<int:id>", methods=["GET"])
    def list_driver(id):

        driver = db.session.get(Driver, id)

        if not driver:
            return {"error": "Driver not found"}, 404

        result = driver.to_dict()

        return jsonify(result)

    @app.route("/edit-driver/<int:id>", methods=["GET", "POST"])
    def edit_driver(id):

        driver = db.session.get(Driver, id)

        if not driver:
            return {"error": "Driver not found"}, 404

        if request.method == "POST":

            driver.name = request.form.get("name")
            driver.phone = request.form.get("phone")
            driver.vehicle = request.form.get("vehicle")
            driver.active = request.form.get("active")

            db.session.commit()

            return redirect(url_for("list_drivers"))

        return render_template("edit-driver.html", driver=driver)

    @app.route("/delete-driver/<int:id>", methods=["POST"])
    def delete_driver(id):
        driver = db.session.get(Driver, id)

        if driver:
            db.session.delete(driver)
            db.session.commit()

        return redirect(url_for("list_drivers"))

    @app.route("/deliveries", methods=["POST"])
    def insert_deliveries():
        data = request.get_json()
        print(data)
        origin_lat, origin_lng = get_coordinates(data.get("origin_address"))
        destination_lat, destination_lng = get_coordinates(data.get("destination_address"))

        driver = db.session.get(Driver, data.get("driver_id"))

        delivery = Delivery(
            description=data.get("description"),
            origin_address=data.get("origin_address"),
            origin_lat=origin_lat,
            origin_lng=origin_lng,
            current_lat=origin_lat,
            current_lng=origin_lng,
            destination_address=data.get("destination_address"),
            destination_lat=destination_lat,
            destination_lng=destination_lng,
            status=data.get("status"),
            driver=driver
        )

        db.session.add(delivery)

        db.session.commit()

        return {"message": "created"}, 201

    @app.route("/deliveries", methods=["GET"])
    def list_deliveries():

        deliveries = db.session.scalars(select(Delivery)).all()
        dict_deliveries = [deliveries.to_dict() for deliveries in deliveries]
        return jsonify(dict_deliveries)

    @app.route("/deliveries/<int:id>", methods=["GET"])
    def get_deliveries(id):

        deliveries = db.session.get(Delivery, id)

        if not deliveries:
            return {"error": "deliveries not found"}, 404

        result = deliveries.to_dict()
        return jsonify(result)

    @app.route("/deliveries/<int:id>", methods=["PUT"])
    def edit_deliveries(id):

        delivery = db.session.get(Delivery, id)

        if not delivery:
            return {"error": "deliveries not found"}, 404

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
    def delete_deliveries(id):

        deliveries = db.session.get(Delivery, id)

        if not deliveries:
            return {"error": "deliveries not found"}, 404

        db.session.delete(deliveries)

        db.session.commit()

        return {"message": "deleted"}

    @app.route("/drivers/<int:id>/deliveries", methods=["GET"])
    def get_driver_deliveries(id):

        driver = db.session.get(Driver, id)

        if not driver:
            return {"error": "Driver not found"}, 404

        deliveries = [deliveries.to_dict() for deliveries in driver.deliveries]

        return jsonify(deliveries)

    @app.route("/deliveries/<int:id>/real-eta", methods=["GET"])
    def get_real_eta(id):
        delivery = db.session.get(Delivery, id)

        if not delivery:
            return {"error": "Delivery not found"}, 404

        if not delivery.current_lat:
            return {"error": "Current location not available"}, 400

        distance, duration = get_route(
            delivery.current_lat,
            delivery.current_lng,
            delivery.destination_lat,
            delivery.destination_lng
        )

        if not distance:
            return {"error": "Could not calculate route"}, 400

        return {
            "delivery_id": delivery.id,
            "distance_km": round(distance, 2),
            "eta_minutes": round(duration)
        }

    @app.route("/deliveries/<int:id>/location", methods=["PUT"])
    def update_delivery_location(id):
        delivery = db.session.get(Delivery, id)

        if not delivery:
            return {"error": "Delivery not found"}, 404

        data = request.get_json()

        delivery.current_lat = data.get("lat")
        delivery.current_lng = data.get("lng")

        db.session.commit()

        return {"message": "Location updated"}
