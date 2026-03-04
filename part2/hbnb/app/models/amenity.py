from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()

        if name is None or not str(name).strip():
            raise ValueError("name cannot be empty")

        self.name = str(name).strip()[:50]

    def update(self, data: dict):
        data = data or {}
        if "name" in data:
            v = data["name"]
            if v is None or not str(v).strip():
                raise ValueError("name cannot be empty")
            self.name = str(v).strip()[:50]
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
