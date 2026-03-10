from app.models.base_model import BaseModel


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

        self.title = str(title).strip()[:100]
        self.description = (str(description).strip() if description is not None else "")[:1000]
        self.price = float(price)
        self.latitude = lat
        self.longitude = lon

        self.owner_id = owner_id
        self.amenities = list(amenities or [])
        self.reviews = []

    def update(self, data: dict):
        data = data or {}

        if "title" in data:
            v = data["title"]
            if v is None or not str(v).strip():
                raise ValueError("title cannot be empty")
            self.title = str(v).strip()[:100]

        if "description" in data:
            v = data["description"]
            self.description = (str(v).strip() if v is not None else "")[:1000]

        if "price" in data:
            v = data["price"]
            if v is None or float(v) < 0:
                raise ValueError("price must be positive")
            self.price = float(v)

        if "latitude" in data:
            v = float(data["latitude"])
            if not -90.0 <= v <= 90.0:
                raise ValueError("latitude must be between -90 and 90")
            self.latitude = v

        if "longitude" in data:
            v = float(data["longitude"])
            if not -180.0 <= v <= 180.0:
                raise ValueError("longitude must be between -180 and 180")
            self.longitude = v

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
