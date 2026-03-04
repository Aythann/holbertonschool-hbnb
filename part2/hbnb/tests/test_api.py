import unittest
from app import create_app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # ---------------- USERS ----------------

    def test_user_crud_and_validation(self):
        # Create valid user
        res = self.client.post("/api/v1/users/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        })
        self.assertEqual(res.status_code, 201)
        user_id = res.get_json()["id"]

        # Invalid email
        res = self.client.post("/api/v1/users/", json={
            "first_name": "Bad",
            "last_name": "Email",
            "email": "invalid"
        })
        self.assertEqual(res.status_code, 400)

        # Duplicate email
        res = self.client.post("/api/v1/users/", json={
            "first_name": "John",
            "last_name": "Dup",
            "email": "john@example.com"
        })
        self.assertEqual(res.status_code, 400)

        # Get existing
        res = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(res.status_code, 200)

        # Get non-existing
        res = self.client.get("/api/v1/users/invalid")
        self.assertEqual(res.status_code, 404)

        # Partial update
        res = self.client.put(f"/api/v1/users/{user_id}", json={
            "first_name": "Johnny"
        })
        self.assertEqual(res.status_code, 200)

        # Invalid update
        res = self.client.put(f"/api/v1/users/{user_id}", json={
            "email": "bad"
        })
        self.assertEqual(res.status_code, 400)

        # Update non-existing
        res = self.client.put("/api/v1/users/invalid", json={
            "first_name": "X"
        })
        self.assertEqual(res.status_code, 404)

    # ---------------- AMENITIES ----------------

    def test_amenity_crud(self):
        res = self.client.post("/api/v1/amenities/", json={"name": "WiFi"})
        self.assertEqual(res.status_code, 201)
        amenity_id = res.get_json()["id"]

        # Invalid name
        res = self.client.post("/api/v1/amenities/", json={"name": ""})
        self.assertEqual(res.status_code, 400)

        # Get existing
        res = self.client.get(f"/api/v1/amenities/{amenity_id}")
        self.assertEqual(res.status_code, 200)

        # Get non-existing
        res = self.client.get("/api/v1/amenities/invalid")
        self.assertEqual(res.status_code, 404)

        # Update
        res = self.client.put(f"/api/v1/amenities/{amenity_id}", json={"name": "Pool"})
        self.assertEqual(res.status_code, 200)

        # Invalid update
        res = self.client.put(f"/api/v1/amenities/{amenity_id}", json={"name": ""})
        self.assertEqual(res.status_code, 400)

    # ---------------- PLACES ----------------

    def test_place_crud_and_validation(self):
        # Create user + amenity first
        user = self.client.post("/api/v1/users/", json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": "owner@example.com"
        }).get_json()

        amenity = self.client.post("/api/v1/amenities/", json={
            "name": "WiFi"
        }).get_json()

        # Create valid place
        res = self.client.post("/api/v1/places/", json={
            "title": "Nice Place",
            "description": "Cool",
            "price": 100,
            "latitude": 45.0,
            "longitude": 3.0,
            "owner_id": user["id"],
            "amenities": [amenity["id"]]
        })
        self.assertEqual(res.status_code, 201)
        place_id = res.get_json()["id"]

        # Invalid latitude
        res = self.client.post("/api/v1/places/", json={
            "title": "Bad Place",
            "description": "Invalid",
            "price": 100,
            "latitude": 200,
            "longitude": 3,
            "owner_id": user["id"],
            "amenities": []
        })
        self.assertEqual(res.status_code, 400)

        # Get list (minimal fields check)
        res = self.client.get("/api/v1/places/")
        self.assertEqual(res.status_code, 200)
        place = res.get_json()[0]
        self.assertIn("id", place)
        self.assertIn("title", place)
        self.assertIn("latitude", place)
        self.assertIn("longitude", place)
        self.assertNotIn("price", place)

        # Partial update
        res = self.client.put(f"/api/v1/places/{place_id}", json={
            "title": "Updated Title"
        })
        self.assertEqual(res.status_code, 200)

        # Forbidden owner update
        res = self.client.put(f"/api/v1/places/{place_id}", json={
            "owner_id": user["id"]
        })
        self.assertEqual(res.status_code, 400)

        # Non-existing place
        res = self.client.get("/api/v1/places/invalid")
        self.assertEqual(res.status_code, 404)

        # Reviews for non-existing place
        res = self.client.get("/api/v1/places/invalid/reviews")
        self.assertEqual(res.status_code, 404)

    # ---------------- REVIEWS ----------------

    def test_review_crud_and_validation(self):
        user = self.client.post("/api/v1/users/", json={
            "first_name": "User",
            "last_name": "Review",
            "email": "review@example.com"
        }).get_json()

        place = self.client.post("/api/v1/places/", json={
            "title": "Review Place",
            "description": "Test",
            "price": 50,
            "latitude": 40,
            "longitude": 2,
            "owner_id": user["id"],
            "amenities": []
        }).get_json()

        # Create review
        res = self.client.post("/api/v1/reviews/", json={
            "text": "Great",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        })
        self.assertEqual(res.status_code, 201)
        review_id = res.get_json()["id"]

        # Invalid rating
        res = self.client.post("/api/v1/reviews/", json={
            "text": "Bad",
            "rating": 10,
            "user_id": user["id"],
            "place_id": place["id"]
        })
        self.assertEqual(res.status_code, 400)

        # List minimal fields
        res = self.client.get("/api/v1/reviews/")
        review = res.get_json()[0]
        self.assertIn("id", review)
        self.assertIn("text", review)
        self.assertIn("rating", review)
        self.assertNotIn("user_id", review)

        # Partial update
        res = self.client.put(f"/api/v1/reviews/{review_id}", json={
            "text": "Updated"
        })
        self.assertEqual(res.status_code, 200)

        # Forbidden relation update
        res = self.client.put(f"/api/v1/reviews/{review_id}", json={
            "user_id": user["id"]
        })
        self.assertEqual(res.status_code, 400)

        # Delete
        res = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertEqual(res.status_code, 200)

        # Delete non-existing
        res = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
