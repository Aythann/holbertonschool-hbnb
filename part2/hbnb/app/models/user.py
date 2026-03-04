import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        if first_name is None or not str(first_name).strip():
            raise ValueError("first_name cannot be empty")

        if last_name is None or not str(last_name).strip():
            raise ValueError("last_name cannot be empty")

        if email is None:
            raise ValueError("Invalid email format")

        email_clean = str(email).strip().lower()
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email_clean):
            raise ValueError("Invalid email format")

        self.first_name = str(first_name).strip()[:50]
        self.last_name = str(last_name).strip()[:50]
        self.email = email_clean
        self.is_admin = bool(is_admin)

        self.places = []
        self.reviews = []

    def update(self, data: dict):
        data = data or {}

        if "first_name" in data:
            v = data["first_name"]
            if v is None or not str(v).strip():
                raise ValueError("first_name cannot be empty")
            self.first_name = str(v).strip()[:50]

        if "last_name" in data:
            v = data["last_name"]
            if v is None or not str(v).strip():
                raise ValueError("last_name cannot be empty")
            self.last_name = str(v).strip()[:50]

        if "email" in data:
            v = data["email"]
            if v is None:
                raise ValueError("Invalid email format")
            email_clean = str(v).strip().lower()
            if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email_clean):
                raise ValueError("Invalid email format")
            self.email = email_clean

        if "is_admin" in data:
            self.is_admin = bool(data["is_admin"])

        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
