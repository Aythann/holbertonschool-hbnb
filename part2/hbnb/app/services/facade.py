from app.persistence.repository import InMemoryRepository

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ------- Users -------
    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email: str):
        return self.user_repo.get_by_attribute("email", (email or "").strip().lower())

    def update_user(self, user_id: str, user_data: dict):
        user = self.get_user(user_id)
        if not user:
            return None
        self.user_repo.update(user_id, user_data)
        return user

    # ------- Amenities -------
    def create_amenity(self, amenity_data: dict) -> Amenity:
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: dict):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # ------- Places -------
    def create_place(self, place_data: dict) -> Place:
        owner = self.user_repo.get(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        # amenities = liste d'IDs -> valider qu'ils existent
        amenity_ids = place_data.get("amenities") or []
        for aid in amenity_ids:
            if not self.amenity_repo.get(aid):
                raise ValueError("Invalid amenity id")

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id: str, place_data: dict):
        place = self.get_place(place_id)
        if not place:
            return None

        if "amenities" in place_data:
            for aid in (place_data.get("amenities") or []):
                if not self.amenity_repo.get(aid):
                    raise ValueError("Invalid amenity id")

        self.place_repo.update(place_id, place_data)
        return place

    # ------- Reviews -------
    def create_review(self, review_data: dict) -> Review:
        if not self.user_repo.get(review_data.get("user_id")):
            raise ValueError("User not found")
        if not self.place_repo.get(review_data.get("place_id")):
            raise ValueError("Place not found")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id: str):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str):
        if not self.place_repo.get(place_id):
            return None
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id: str, review_data: dict):
        review = self.get_review(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id: str):
        if not self.get_review(review_id):
            return False
        self.review_repo.delete(review_id)
        return True