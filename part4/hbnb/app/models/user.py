import re
from app import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    places = db.relationship(
        "Place",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan",
    )
    reviews = db.relationship(
        "Review",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        if first_name is None or not str(first_name).strip():
            raise ValueError("first_name cannot be empty")

        if last_name is None or not str(last_name).strip():
            raise ValueError("last_name cannot be empty")

        if email is None:
            raise ValueError("Invalid email format")

        email_clean = str(email).strip().lower()
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email_clean):
            raise ValueError("Invalid email format")

        if password is None or len(str(password)) < 6:
            raise ValueError("Password must be at least 6 characters")

        self.first_name = str(first_name).strip()[:50]
        self.last_name = str(last_name).strip()[:50]
        self.email = email_clean
        self.is_admin = bool(is_admin)
        self.hash_password(str(password))

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data: dict):
        data = data or {}

        if "first_name" in data:
            value = data["first_name"]
            if value is None or not str(value).strip():
                raise ValueError("first_name cannot be empty")
            self.first_name = str(value).strip()[:50]

        if "last_name" in data:
            value = data["last_name"]
            if value is None or not str(value).strip():
                raise ValueError("last_name cannot be empty")
            self.last_name = str(value).strip()[:50]

        if "email" in data:
            value = data["email"]
            if value is None:
                raise ValueError("Invalid email format")
            email_clean = str(value).strip().lower()
            if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email_clean):
                raise ValueError("Invalid email format")
            self.email = email_clean

        if "password" in data:
            password = data["password"]
            if password is None or len(str(password)) < 6:
                raise ValueError("Password must be at least 6 characters")
            self.hash_password(str(password))

        if "is_admin" in data:
            self.is_admin = bool(data["is_admin"])

        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        }
