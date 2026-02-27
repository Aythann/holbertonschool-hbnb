from app.models.base_model import BaseModel
from app.models.validators import require_str, require_float


class Place(BaseModel):
    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        latitude: float,
        longitude: float,
        owner_id: str,
        amenities=None,
    ):
        super().__init__()
        self.title = require_str("title", title, min_len=1, max_len=100)
        self.description = require_str("description", description or "", min_len=0, max_len=1000)
        self.price = require_float("price", price, min_value=0.0)
        self.latitude = require_float("latitude", latitude, min_value=-90.0, max_value=90.0)
        self.longitude = require_float("longitude", longitude, min_value=-180.0, max_value=180.0)
        self.owner_id = owner_id
        self.amenities = list(amenities or [])
        self.reviews = []  # pourra être rempli plus tard

    def update(self, data: dict):
        if "title" in data:
            self.title = require_str("title", data["title"], min_len=1, max_len=100)
        if "description" in data:
            self.description = require_str("description", data.get("description", ""), min_len=0, max_len=1000)
        if "price" in data:
            self.price = require_float("price", data["price"], min_value=0.0)
        if "latitude" in data:
            self.latitude = require_float("latitude", data["latitude"], min_value=-90.0, max_value=90.0)
        if "longitude" in data:
            self.longitude = require_float("longitude", data["longitude"], min_value=-180.0, max_value=180.0)
        if "amenities" in data:
            self.amenities = list(data.get("amenities") or [])
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
            "amenities": self.amenities,
        }