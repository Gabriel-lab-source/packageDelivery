from app import db
from datetime import datetime, timezone


class Delivery(db.Model):
    __tablename__ = "deliveries"

    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.String(150), nullable=False)

    origin_address = db.Column(db.String(150), nullable=False)

    origin_lat = db.Column(db.Float)

    origin_lng = db.Column(db.Float)

    destination_address = db.Column(db.String(150), nullable=False)

    destination_lat = db.Column(db.Float)

    destination_lng = db.Column(db.Float)

    status = db.Column(db.String(20), nullable=False, default="pending")

    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "origin_address": self.origin_address,
            "destination_address": self.destination_address,
            "status": self.status,
            "driver_id": self.driver_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
