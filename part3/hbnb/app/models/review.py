from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "place_id",
            name="uq_review_user_place"
        ),
    )

    text = db.Column(db.String(2000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )
    place_id = db.Column(
        db.String(36),
        db.ForeignKey("places.id"),
        nullable=False
    )

    def __init__(
        self,
        text: str,
        rating: int,
        user_id: str,
        place_id: str,
    ):
        if text is None or not str(text).strip():
            raise ValueError("text cannot be empty")

        invalid_rating = (
            isinstance(rating, bool)
            or not isinstance(rating, int)
            or not 1 <= rating <= 5
        )
        if invalid_rating:
            raise ValueError("rating must be between 1 and 5")

        if user_id is None or not str(user_id).strip():
            raise ValueError("user_id cannot be empty")

        if place_id is None or not str(place_id).strip():
            raise ValueError("place_id cannot be empty")

        self.text = str(text).strip()[:2000]
        self.rating = rating
        self.user_id = str(user_id).strip()
        self.place_id = str(place_id).strip()

    def update(self, data: dict):
        data = data or {}

        if "text" in data:
            value = data["text"]
            if value is None or not str(value).strip():
                raise ValueError("text cannot be empty")
            self.text = str(value).strip()[:2000]

        if "rating" in data:
            value = data["rating"]
            invalid_rating = (
                isinstance(value, bool)
                or not isinstance(value, int)
                or not 1 <= value <= 5
            )
            if invalid_rating:
                raise ValueError("rating must be between 1 and 5")
            self.rating = value

        if "user_id" in data or "place_id" in data:
            raise ValueError("user_id/place_id cannot be updated")

        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
        }
