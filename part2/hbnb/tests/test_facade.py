import unittest
from app.services.facade import HBnBFacade


class TestFacade(unittest.TestCase):
    def setUp(self):
        self.f = HBnBFacade()

    # ---------------- USERS ----------------

    def test_create_and_get_user(self):
        u = self.f.create_user(
            {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}
        )
        fetched = self.f.get_user(u.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.email, "john.doe@example.com")

    def test_get_user_by_email_case_insensitive(self):
        self.f.create_user(
            {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}
        )
        found = self.f.get_user_by_email("JOHN.DOE@EXAMPLE.COM")
        self.assertIsNotNone(found)
        self.assertEqual(found.email, "john.doe@example.com")

    def test_update_user_validation(self):
        u = self.f.create_user(
            {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}
        )

        updated = self.f.update_user(u.id, {"first_name": "Jane"})
        self.assertIsNotNone(updated)
        self.assertEqual(updated.first_name, "Jane")

        with self.assertRaises(ValueError):
            self.f.update_user(u.id, {"email": "bad-email"})

    # ---------------- AMENITIES ----------------

    def test_create_amenity_and_update_validation(self):
        a = self.f.create_amenity({"name": "Wi-Fi"})
        fetched = self.f.get_amenity(a.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Wi-Fi")

        updated = self.f.update_amenity(a.id, {"name": "Pool"})
        self.assertIsNotNone(updated)
        self.assertEqual(updated.name, "Pool")

        with self.assertRaises(ValueError):
            self.f.update_amenity(a.id, {"name": "   "})

    # ---------------- PLACES ----------------

    def test_create_place_owner_missing(self):
        with self.assertRaises(ValueError):
            self.f.create_place(
                {
                    "title": "Cozy",
                    "description": "",
                    "price": 100.0,
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "owner_id": "missing-owner",
                    "amenities": [],
                }
            )

    def test_create_place_with_amenity_validation(self):
        u = self.f.create_user(
            {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}
        )
        # amenity id invalide -> ValueError
        with self.assertRaises(ValueError):
            self.f.create_place(
                {
                    "title": "Cozy",
                    "description": "",
                    "price": 100.0,
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "owner_id": u.id,
                    "amenities": ["missing-amenity"],
                }
            )

    def test_place_update_partial_and_owner_forbidden(self):
        u = self.f.create_user(
            {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}
        )
        a = self.f.create_amenity({"name": "Wi-Fi"})
        p = self.f.create_place(
            {
                "title": "Cozy",
                "description": "ok",
                "price": 100.0,
                "latitude": 10.0,
                "longitude": 10.0,
                "owner_id": u.id,
                "amenities": [a.id],
            }
        )

        # update partiel OK
        updated = self.f.update_place(p.id, {"title": "Luxury Condo"})
        self.assertIsNotNone(updated)
        self.assertEqual(updated.title, "Luxury Condo")

        # update invalide latitude
        with self.assertRaises(ValueError):
            self.f.update_place(p.id, {"latitude": 999.0})

        # owner_id interdit
        with self.assertRaises(ValueError):
            self.f.update_place(p.id, {"owner_id": u.id})

    # ---------------- REVIEWS ----------------

    def test_create_review_requires_user_and_place(self):
        with self.assertRaises(ValueError):
            self.f.create_review({"text": "Nice", "rating": 5, "user_id": "u", "place_id": "p"})

    def test_review_full_flow_with_partial_update(self):
        u = self.f.create_user(
            {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}
        )
        a = self.f.create_amenity({"name": "Wi-Fi"})
        p = self.f.create_place(
            {
                "title": "Cozy",
                "description": "ok",
                "price": 100.0,
                "latitude": 10.0,
                "longitude": 10.0,
                "owner_id": u.id,
                "amenities": [a.id],
            }
        )
        r = self.f.create_review({"text": "Great", "rating": 5, "user_id": u.id, "place_id": p.id})
        self.assertIsNotNone(self.f.get_review(r.id))

        # list by place
        reviews = self.f.get_reviews_by_place(p.id)
        self.assertIsNotNone(reviews)
        self.assertTrue(any(x.id == r.id for x in reviews))

        # update partiel (doc)
        updated = self.f.update_review(r.id, {"text": "Amazing", "rating": 4})
        self.assertIsNotNone(updated)
        self.assertEqual(updated.rating, 4)

        # update invalide rating
        with self.assertRaises(ValueError):
            self.f.update_review(r.id, {"rating": 6})

        # user_id/place_id interdits (si tu as gardé le blocage côté facade)
        with self.assertRaises(ValueError):
            self.f.update_review(r.id, {"user_id": u.id})

        # delete
        self.assertTrue(self.f.delete_review(r.id))
        self.assertIsNone(self.f.get_review(r.id))


if __name__ == "__main__":
    unittest.main()