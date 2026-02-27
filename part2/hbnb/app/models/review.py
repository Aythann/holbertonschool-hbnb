from app.models.base_model import BaseModel
from app.models.validators import require_str, require_int


class Review(BaseModel):
    def __init__(self, text: str, rating: int, user_id: str, place_id: str):
        super().__init__()
        self.text = require_str("text", text, min_len=1, max_len=2000)
        self.rating = require_int("rating", rating, min_value=1, max_value=5)
        self.user_id = user_id
        self.place_id = place_id

    def update(self, data: dict):
        if "text" in data:
            self.text = require_str("text", data["text"], min_len=1, max_len=2000)
        if "rating" in data:
            self.rating = require_int("rating", data["rating"], min_value=1, max_value=5)
        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
        }