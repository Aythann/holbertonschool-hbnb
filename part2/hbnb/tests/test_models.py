import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestModels(unittest.TestCase):

    # ---------------- USER ----------------

    def test_user_creation_ok(self):
        u = User(first_name="John", last_name="Doe", email="John.Doe@Example.com")
        self.assertIsInstance(u.id, str)
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Doe")
        self.assertEqual(u.email, "john.doe@example.com")

    def test_user_creation_invalid(self):
        with self.assertRaises(ValueError):
            User(first_name="   ", last_name="Doe", email="john.doe@example.com")

        with self.assertRaises(ValueError):
            User(first_name="John", last_name="   ", email="john.doe@example.com")

        with self.assertRaises(ValueError):
            User(first_name="John", last_name="Doe", email="bad-email")

    def test_user_update_validation(self):
        u = User(first_name="John", last_name="Doe", email="john.doe@example.com")

        u.update({"first_name": "Jane"})
        self.assertEqual(u.first_name, "Jane")

        with self.assertRaises(ValueError):
            u.update({"email": "not-an-email"})

    # ---------------- AMENITY ----------------

    def test_amenity_creation_and_update(self):
        a = Amenity(name="Wi-Fi")
        self.assertIsInstance(a.id, str)
        self.assertEqual(a.name, "Wi-Fi")

        a.update({"name": "Pool"})
        self.assertEqual(a.name, "Pool")

        with self.assertRaises(ValueError):
            a.update({"name": "   "})

    # ---------------- PLACE ----------------

    def test_place_creation_ok(self):
        p = Place(
            title="Cozy Apartment",
            description="A nice place",
            price=100.0,
            latitude=37.7749,
            longitude=-122.4194,
            owner_id="owner-id",
            amenities=[],
        )
        self.assertIsInstance(p.id, str)
        self.assertEqual(p.title, "Cozy Apartment")
        self.assertEqual(p.price, 100.0)

    def test_place_validation_ranges(self):
        with self.assertRaises(ValueError):
            Place(
                title="X",
                description="",
                price=-1,
                latitude=0.0,
                longitude=0.0,
                owner_id="owner-id",
                amenities=[],
            )

        with self.assertRaises(ValueError):
            Place(
                title="X",
                description="",
                price=10.0,
                latitude=999.0,
                longitude=0.0,
                owner_id="owner-id",
                amenities=[],
            )

        with self.assertRaises(ValueError):
            Place(
                title="X",
                description="",
                price=10.0,
                latitude=0.0,
                longitude=999.0,
                owner_id="owner-id",
                amenities=[],
            )

    def test_place_update_validation(self):
        p = Place(
            title="Cozy",
            description="ok",
            price=10.0,
            latitude=0.0,
            longitude=0.0,
            owner_id="owner-id",
            amenities=[],
        )

        p.update({"title": "Luxury Condo"})
        self.assertEqual(p.title, "Luxury Condo")

        with self.assertRaises(ValueError):
            p.update({"latitude": 999.0})

    # ---------------- REVIEW ----------------

    def test_review_creation_ok(self):
        r = Review(text="Great stay!", rating=5, user_id="u", place_id="p")
        self.assertIsInstance(r.id, str)
        self.assertEqual(r.rating, 5)

    def test_review_validation_rating(self):
        with self.assertRaises(ValueError):
            Review(text="ok", rating=6, user_id="u", place_id="p")

        with self.assertRaises(ValueError):
            Review(text="ok", rating=0, user_id="u", place_id="p")

    def test_review_update_validation(self):
        r = Review(text="Nice", rating=5, user_id="u", place_id="p")

        r.update({"text": "Amazing"})
        self.assertEqual(r.text, "Amazing")

        r.update({"rating": 4})
        self.assertEqual(r.rating, 4)

        with self.assertRaises(ValueError):
            r.update({"rating": 10})


if __name__ == "__main__":
    unittest.main()
