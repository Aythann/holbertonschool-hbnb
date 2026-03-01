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
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        if email is None:
            return None
        return self.user_repo.get_by_attribute("email", email.strip().lower())

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        # le modèle User.update gère la validation
        return self.user_repo.update(user_id, user_data)

    # ------- Amenities -------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        # le modèle Amenity.update gère la validation
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # ------- Places -------
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.get("amenities") or []
        for aid in amenity_ids:
            if not self.amenity_repo.get(aid):
                raise ValueError("Invalid amenity id")

        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        # Owner update non demandé dans la doc -> on refuse si quelqu'un essaye
        if "owner_id" in (place_data or {}):
            raise ValueError("owner_id cannot be updated")

        # Validation des amenities IDs si présentes
        if "amenities" in (place_data or {}):
            for aid in (place_data.get("amenities") or []):
                if not self.amenity_repo.get(aid):
                    raise ValueError("Invalid amenity id")

        # le modèle Place.update gère validations price/lat/lon/title...
        self.place_repo.update(place_id, place_data)
        return place

    # ------- Reviews -------
    def create_review(self, review_data):
        if not self.user_repo.get(review_data.get("user_id")):
            raise ValueError("User not found")
        if not self.place_repo.get(review_data.get("place_id")):
            raise ValueError("Place not found")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        if not self.place_repo.get(place_id):
            return None
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        if "user_id" in (review_data or {}) or "place_id" in (review_data or {}):
            raise ValueError("user_id/place_id cannot be updated")

        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        if not self.get_review(review_id):
            return False
        self.review_repo.delete(review_id)
        return True