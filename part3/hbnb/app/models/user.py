import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
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

        if password is None or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")

        self.first_name = str(first_name).strip()[:50]
        self.last_name = str(last_name).strip()[:50]
        self.email = email_clean
        self.is_admin = bool(is_admin)

        self.places = []
        self.reviews = []
        
    def hash_password(self, password):
        """Hashes the password before storing it."""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify provided password."""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)

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
            
        if "password" in data:
            self.hash_password(data["password"])

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
