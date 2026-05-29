from app.extensions import db
from app.models.driver import Driver
from app.models.delivery import Delivery
from app.models.user import User
from app.services.geolocation import get_route
from sqlalchemy import select
from flask import request, render_template, redirect, url_for, session, Blueprint

driver_bp = Blueprint(
    "driver",
    __name__
)


@driver_bp.route("/create-driver", methods=["GET", "POST"])
def create_driver():

    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    if request.method == "POST":
        new_driver = Driver(
            user_id=session["user_id"],
            name=request.form.get("name"),
            phone=request.form.get("phone"),
            vehicle=request.form.get("vehicle")
        )

        db.session.add(new_driver)
        db.session.commit()

        return redirect("/collect-deliveries")

    return render_template("create-driver.html", user=user)


@driver_bp.route("/collect-deliveries", methods=["POST", "GET"])
def collect_deliveries():

    if "user_id" not in session or session["role"] != "driver":
        return redirect("/login")

    packages = Delivery.query.filter_by(
        status="pending",
        driver_id=None
        ).all()

    if request.method == "POST":

        selected_packages = request.form.getlist("package_ids")

        driver = Driver.query.filter_by(
            user_id=session["user_id"]
            ).first()

        for package_id in selected_packages:

            delivery = db.session.get(Delivery, package_id)

            if delivery:
                delivery.driver_id = driver.id
                delivery.status = "in_progress"

            db.session.commit()

        return redirect(url_for("driver.driver_deliveries"))
    return render_template("collect-deliveries.html", packages=packages)


@driver_bp.route("/list-drivers", methods=["GET"])
def list_drivers():

    drivers = db.session.scalars(select(Driver)).all()
    return render_template("get-drivers.html", drivers=drivers)


@driver_bp.route("/edit-driver/<int:id>", methods=["GET", "POST"])
def edit_driver(id):

    if "user_id" not in session:
        return redirect("/login")

    driver = db.session.get(Driver, session["user_id"])

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


@driver_bp.route("/delete-driver/<int:id>", methods=["POST"])
def delete_driver(id):

    driver = db.session.get(Driver, id)

    if driver:

        db.session.delete(driver)
        db.session.commit()

    return redirect(url_for("list_drivers"))


@driver_bp.route("/driver-deliveries", methods=["GET"])
def driver_deliveries():

    driver = Driver.query.filter_by(user_id=session["user_id"]).first()

    if not driver:
        return {"error": "Driver not found"}, 404

    deliveries = driver.deliveries

    return render_template("driver-deliveries.html", deliveries=deliveries)


@driver_bp.route("/driver-deliveries/<int:id>/real-eta", methods=["GET"])
def get_real_eta(id):

    delivery = db.session.get(Delivery, id)

    if not delivery:
        return {"error": "Delivery not found"}, 404

    if not delivery.current_lat:
        return {"error": "Current location not available"}, 400

    route = get_route(
        delivery.current_lat,
        delivery.current_lng,
        delivery.destination_lat,
        delivery.destination_lng
    )

    if not route:
        return {"error": "Could not calculate route"}, 400

    return render_template("driver-deliveries-real-eta.html", route=route, delivery=delivery)


@driver_bp.route("/deliveries/<int:id>/location", methods=["PUT"])
def update_delivery_location(id):
    delivery = db.session.get(Delivery, id)

    if not delivery:
        return {"error": "Delivery not found"}, 404

    data = request.get_json()

    delivery.current_lat = data.get("lat")
    delivery.current_lng = data.get("lng")

    db.session.commit()

    return {"message": "Location updated"}
