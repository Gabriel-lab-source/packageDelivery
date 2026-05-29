from app.extensions import db
from app.models.delivery import Delivery
from app.models.user import User
from app.services.geolocation import get_coordinates
from sqlalchemy import select
from flask import request, jsonify, render_template, redirect, url_for, Blueprint, session

sender_bp = Blueprint(
    "sender",
    __name__
)


@sender_bp.route("/create-delivery", methods=["GET", "POST"])
def insert_delivery():

    if "user_id" not in session or session["role"] != "sender":
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    if request.method == "POST":

        origin_lat, origin_lng = get_coordinates(request.form.get("origin_address"))
        destination_lat, destination_lng = get_coordinates(request.form.get("destination_address"))

        delivery = Delivery(
            description=request.form.get("description"),
            sender=request.form.get("sender"),
            recipient=request.form.get("recipient"),
            origin_address=request.form.get("origin_address"),
            origin_lat=origin_lat,
            origin_lng=origin_lng,
            current_lat=origin_lat,
            current_lng=origin_lng,
            destination_address=request.form.get("destination_address"),
            destination_lat=destination_lat,
            destination_lng=destination_lng,
        )

        db.session.add(delivery)
        db.session.commit()

        return redirect(url_for("sender.insert_delivery", message="Entrega criada com sucesso"))

    return render_template("create-delivery.html", user=user)


@sender_bp.route("/deliveries", methods=["GET"])
def list_deliveries():

    deliveries = db.session.scalars(select(Delivery)).all()
    dict_deliveries = [deliveries.to_dict() for deliveries in deliveries]
    return jsonify(dict_deliveries)


@sender_bp.route("/deliveries/<int:id>", methods=["GET"])
def get_deliveries(id):

    deliveries = db.session.get(Delivery, id)

    if not deliveries:
        return {"error": "deliveries not found"}, 404

    result = deliveries.to_dict()
    return jsonify(result)


@sender_bp.route("/deliveries/<int:id>", methods=["PUT"])
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


@sender_bp.route("/deliveries/<int:id>", methods=["DELETE"])
def delete_deliveries(id):

    deliveries = db.session.get(Delivery, id)

    if not deliveries:
        return {"error": "deliveries not found"}, 404

    db.session.delete(deliveries)

    db.session.commit()

    return {"message": "deleted"}


@sender_bp.route("/sender-deliveries", methods=["GET"])
def sender_deliveries():

    user = db.session.get(User, session["user_id"])

    if not user:
        return {"error": "user not found"}, 404

    deliveries = Delivery.query.filter_by(sender=user.name).all()

    if not deliveries:
        return {"error": "deliveries not found"}, 404

    return render_template("sender-deliveries.html", deliveries=deliveries)
