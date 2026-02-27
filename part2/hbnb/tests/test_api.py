import unittest

from app import create_app
from app.services.facade import HBnBFacade

import app.services as services_module
import app.api.v1.users as users_api
import app.api.v1.amenities as amenities_api
import app.api.v1.places as places_api
import app.api.v1.reviews as reviews_api


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        fresh = HBnBFacade()

        services_module.facade = fresh
        users_api.facade = fresh
        amenities_api.facade = fresh
        places_api.facade = fresh
        reviews_api.facade = fresh

        self.facade = fresh

    def test_users_crud(self):
        # POST create
        resp = self.client.post(
            "/api/v1/users/",
            json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        )
        self.assertEqual(resp.status_code, 201)
        user = resp.get_json()
        self.assertIn("id", user)
        user_id = user["id"]

        # GET list
        resp = self.client.get("/api/v1/users/")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(any(u["id"] == user_id for u in data))

        # GET by id
        resp = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(resp.status_code, 200)

        # PUT update (validate=True => payload complet requis)
        resp = self.client.put(
            f"/api/v1/users/{user_id}",
            json={"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com"},
        )
        self.assertEqual(resp.status_code, 200)

        # Duplicate email => 400 (conforme doc)
        resp = self.client.post(
            "/api/v1/users/",
            json={"first_name": "X", "last_name": "Y", "email": "jane.doe@example.com"},
        )
        self.assertEqual(resp.status_code, 400)

    def test_amenities_crud(self):
        # POST create
        resp = self.client.post("/api/v1/amenities/", json={"name": "Wi-Fi"})
        self.assertEqual(resp.status_code, 201)
        amenity = resp.get_json()
        amenity_id = amenity["id"]

        # GET list
        resp = self.client.get("/api/v1/amenities/")
        self.assertEqual(resp.status_code, 200)

        # GET by id
        resp = self.client.get(f"/api/v1/amenities/{amenity_id}")
        self.assertEqual(resp.status_code, 200)

        # PUT update
        resp = self.client.put(f"/api/v1/amenities/{amenity_id}", json={"name": "Air Conditioning"})
        self.assertEqual(resp.status_code, 200)

    def test_places_and_reviews_flow(self):
        # Create user
        resp = self.client.post(
            "/api/v1/users/",
            json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        )
        self.assertEqual(resp.status_code, 201)
        user_id = resp.get_json()["id"]

        # Create amenity
        resp = self.client.post("/api/v1/amenities/", json={"name": "Wi-Fi"})
        self.assertEqual(resp.status_code, 201)
        amenity_id = resp.get_json()["id"]

        # Create place
        place_payload = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user_id,
            "amenities": [amenity_id],
        }
        resp = self.client.post("/api/v1/places/", json=place_payload)
        self.assertEqual(resp.status_code, 201)
        place_id = resp.get_json()["id"]

        # GET place
        resp = self.client.get(f"/api/v1/places/{place_id}")
        self.assertEqual(resp.status_code, 200)

        # Invalid latitude => 400
        bad_place = dict(place_payload)
        bad_place["latitude"] = 999.0
        resp = self.client.post("/api/v1/places/", json=bad_place)
        self.assertEqual(resp.status_code, 400)

        # Create review
        review_payload = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id,
        }
        resp = self.client.post("/api/v1/reviews/", json=review_payload)
        self.assertEqual(resp.status_code, 201)
        review_id = resp.get_json()["id"]

        # GET reviews list
        resp = self.client.get("/api/v1/reviews/")
        self.assertEqual(resp.status_code, 200)

        # GET review by id
        resp = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(resp.status_code, 200)

        # GET place reviews
        resp = self.client.get(f"/api/v1/places/{place_id}/reviews")
        self.assertEqual(resp.status_code, 200)
        reviews = resp.get_json()
        self.assertTrue(any(r["id"] == review_id for r in reviews))

        # PUT review (validate=True => payload complet requis)
        resp = self.client.put(
            f"/api/v1/reviews/{review_id}",
            json={
                "text": "Amazing stay!",
                "rating": 4,
                "user_id": user_id,
                "place_id": place_id,
            },
        )
        self.assertEqual(resp.status_code, 200)

        # DELETE review
        resp = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertEqual(resp.status_code, 200)

        # GET deleted => 404
        resp = self.client.get(f"/api/v1/reviews/{review_id}")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()