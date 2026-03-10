from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(
        self,
        text: str,
        rating: int,
        user_id: str,
        place_id: str,
    ):
        super().__init__()

        if text is None or not str(text).strip():
            raise ValueError("text cannot be empty")

        if isinstance(rating, bool) or not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("rating must be between 1 and 5")

        self.text = str(text).strip()[:2000]
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    def update(self, data: dict):
        data = data or {}

        if "text" in data:
            v = data["text"]
            if v is None or not str(v).strip():
                raise ValueError("text cannot be empty")
            self.text = str(v).strip()[:2000]

        if "rating" in data:
            v = data["rating"]
            if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 5:
                raise ValueError("rating must be between 1 and 5")
            self.rating = v


        self.save()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
        }
