import unittest

from app.models.validators import require_email, require_float, require_int, require_str
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestValidators(unittest.TestCase):
    def test_require_str_ok(self):
        self.assertEqual(require_str("name", "  Wi-Fi  ", min_len=1, max_len=50), "Wi-Fi")

    def test_require_str_invalid_type(self):
        with self.assertRaises(ValueError):
            require_str("name", 123)

    def test_require_str_too_short(self):
        with self.assertRaises(ValueError):
            require_str("name", "  ", min_len=1)

    def test_require_email_ok(self):
        self.assertEqual(require_email("John.Doe@Example.com"), "john.doe@example.com")

    def test_require_email_invalid(self):
        with self.assertRaises(ValueError):
            require_email("not-an-email")

    def test_require_float_ok(self):
        self.assertEqual(require_float("price", "10.5", min_value=0.0), 10.5)

    def test_require_float_out_of_range(self):
        with self.assertRaises(ValueError):
            require_float("latitude", 200, min_value=-90.0, max_value=90.0)

    def test_require_int_ok(self):
        self.assertEqual(require_int("rating", "5", min_value=1, max_value=5), 5)

    def test_require_int_bool_rejected(self):
        with self.assertRaises(ValueError):
            require_int("rating", True, min_value=1, max_value=5)


class TestModels(unittest.TestCase):
    def test_user_creation(self):
        u = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.assertIsInstance(u.id, str)
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Doe")
        self.assertEqual(u.email, "john.doe@example.com")

    def test_user_update_validation(self):
        u = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        with self.assertRaises(ValueError):
            u.update({"email": "bad-email"})

    def test_amenity_creation(self):
        a = Amenity(name="Wi-Fi")
        self.assertIsInstance(a.id, str)
        self.assertEqual(a.name, "Wi-Fi")

    def test_place_validation_latitude(self):
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

    def test_review_validation_rating(self):
        with self.assertRaises(ValueError):
            Review(text="ok", rating=6, user_id="u", place_id="p")


if __name__ == "__main__":
    unittest.main()