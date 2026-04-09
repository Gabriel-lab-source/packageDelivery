from app import db


class Driver(db.Model):

    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(13), nullable=False)

    vehicle = db.Column(db.String(20), nullable=False)

    active = db.Column(db.Boolean, default=True)

    deliveries = db.relationship("Delivery", backref="driver")

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "vehicle": self.vehicle,
            "active": self.active
        }
