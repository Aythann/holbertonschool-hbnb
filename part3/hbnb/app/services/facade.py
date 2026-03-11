from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ------- Users -------
    def create_user(self, user_data):
        email = user_data.get("email")
        if email and self.get_user_by_email(email):
            raise ValueError("Email already registered")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        if email is None:
            return None
        email_clean = str(email).strip().lower()
        return self.user_repo.get_by_attribute("email", email_clean)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None

        incoming_email = user_data.get("email")
        if incoming_email:
            existing_user = self.get_user_by_email(incoming_email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

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

        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    # ------- Places -------
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.get("amenities") or []
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError("Invalid amenity id")
            amenities.append(amenity)

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner_id=place_data.get("owner_id"),
        )
        place.amenities = amenities

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

        if "owner_id" in (place_data or {}):
            raise ValueError("owner_id cannot be updated")

        cleaned_data = dict(place_data or {})

        if "amenities" in cleaned_data:
            amenity_ids = cleaned_data.pop("amenities") or []
            amenities = []
            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError("Invalid amenity id")
                amenities.append(amenity)
            place.amenities = amenities

        self.place_repo.update(place_id, cleaned_data)
        return self.get_place(place_id)

    # ------- Reviews -------
    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get("user_id"))
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data.get("place_id"))
        if not place:
            raise ValueError("Place not found")

        existing_review = Review.query.filter_by(
            user_id=review_data.get("user_id"),
            place_id=review_data.get("place_id"),
        ).first()
        if existing_review:
            raise ValueError("You have already reviewed this place.")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return Review.query.filter_by(
            place_id=place_id
        ).all()

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        if "user_id" in (review_data or {}):
            raise ValueError("user_id/place_id cannot be updated")
        if "place_id" in (review_data or {}):
            raise ValueError("user_id/place_id cannot be updated")

        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        if not self.get_review(review_id):
            return False
        self.review_repo.delete(review_id)
        return True
