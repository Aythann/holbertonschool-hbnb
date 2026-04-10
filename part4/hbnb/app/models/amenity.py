from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name: str):
        if name is None or not str(name).strip():
            raise ValueError("name cannot be empty")
        self.name = str(name).strip()[:50]

    def update(self, data: dict):
        data = data or {}

        if "name" in data:
            value = data["name"]
            if value is None or not str(value).strip():
                raise ValueError("name cannot be empty")
            self.name = str(value).strip()[:50]

        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
