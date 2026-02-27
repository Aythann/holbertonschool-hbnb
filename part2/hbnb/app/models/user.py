from app.models.base_model import BaseModel
from app.models.validators import require_str, require_email


class User(BaseModel):
    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        super().__init__()
        self.first_name = require_str("first_name", first_name, min_len=1, max_len=50)
        self.last_name = require_str("last_name", last_name, min_len=1, max_len=50)
        self.email = require_email(email)
        self.is_admin = bool(is_admin)

    def update(self, data: dict):
        # Validation + mise à jour contrôlée
        if "first_name" in data:
            self.first_name = require_str("first_name", data["first_name"], min_len=1, max_len=50)
        if "last_name" in data:
            self.last_name = require_str("last_name", data["last_name"], min_len=1, max_len=50)
        if "email" in data:
            self.email = require_email(data["email"])
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        }