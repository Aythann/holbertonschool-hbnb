from app.models.base_model import BaseModel
from app.models.validators import require_str


class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        self.name = require_str("name", name, min_len=1, max_len=50)

    def update(self, data: dict):
        if "name" in data:
            self.name = require_str("name", data["name"], min_len=1, max_len=50)
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }