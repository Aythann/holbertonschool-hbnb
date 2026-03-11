from app import db
from app.models.base_model import BaseModel


place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id"), primary_key=True),
)


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False, default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    reviews = db.relationship(
        "Review",
        backref="place",
        lazy=True,
        cascade="all, delete-orphan",
    )
    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        lazy="subquery",
        backref=db.backref("places", lazy=True),
    )

    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        latitude: float,
        longitude: float,
        owner_id: str,
    ):
        if title is None or not str(title).strip():
            raise ValueError("title cannot be empty")

        if price is None or float(price) < 0:
            raise ValueError("price must be positive")

        lat = float(latitude)
        lon = float(longitude)

        if not -90.0 <= lat <= 90.0:
            raise ValueError("latitude must be between -90 and 90")

        if not -180.0 <= lon <= 180.0:
            raise ValueError("longitude must be between -180 and 180")

        if owner_id is None or not str(owner_id).strip():
            raise ValueError("owner_id cannot be empty")

        self.title = str(title).strip()[:100]
        self.description = (str(description).strip() if description is not None else "")[:1000]
        self.price = float(price)
        self.latitude = lat
        self.longitude = lon
        self.owner_id = str(owner_id).strip()

    def update(self, data: dict):
        data = data or {}

        if "title" in data:
            value = data["title"]
            if value is None or not str(value).strip():
                raise ValueError("title cannot be empty")
            self.title = str(value).strip()[:100]

        if "description" in data:
            value = data["description"]
            self.description = (str(value).strip() if value is not None else "")[:1000]

        if "price" in data:
            value = data["price"]
            if value is None or float(value) < 0:
                raise ValueError("price must be positive")
            self.price = float(value)

        if "latitude" in data:
            value = float(data["latitude"])
            if not -90.0 <= value <= 90.0:
                raise ValueError("latitude must be between -90 and 90")
            self.latitude = value

        if "longitude" in data:
            value = float(data["longitude"])
            if not -180.0 <= value <= 180.0:
                raise ValueError("longitude must be between -180 and 180")
            self.longitude = value

        if "owner_id" in data:
            raise ValueError("owner_id cannot be updated")

        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": [amenity.id for amenity in self.amenities],
        }
