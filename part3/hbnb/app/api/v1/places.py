from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace("places", description="Place operations")

amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(description="Amenity ID"),
        "name": fields.String(description="Name of the amenity"),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name of the owner"),
        "last_name": fields.String(description="Last name of the owner"),
        "email": fields.String(description="Email of the owner"),
        "is_admin": fields.Boolean(description="Admin flag"),
    },
)

review_model = api.model(
    "PlaceReview",
    {
        "id": fields.String(description="Review ID"),
        "text": fields.String(description="Text of the review"),
        "rating": fields.Integer(description="Rating (1-5)"),
        "user_id": fields.String(description="ID of the user"),
    },
)

place_model = api.model(
    "Place",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "amenities": fields.List(fields.String, description="List of amenities IDs"),
    },
)

update_place_model = api.model(
    "UpdatePlace",
    {
        "title": fields.String(description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(description="Price per night"),
        "latitude": fields.Float(description="Latitude of the place"),
        "longitude": fields.Float(description="Longitude of the place"),
        "amenities": fields.List(fields.String, description="List of amenities IDs"),
    },
)


def place_to_dict_list(place):
    return {
        "id": place.id,
        "title": place.title,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
    }


def place_to_dict_detail(place):
    owner = facade.get_user(place.owner_id) if place.owner_id else None

    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": owner.to_dict() if owner else None,
        "amenities": [amenity.to_dict() for amenity in place.amenities],
        "reviews": [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
            }
            for review in place.reviews
        ],
    }


@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()
        data = dict(api.payload or {})
        data["owner_id"] = current_user

        try:
            place = facade.create_place(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return place_to_dict_detail(place), 201

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place_to_dict_list(place) for place in places], 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place_to_dict_detail(place), 200

    @api.expect(update_place_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_jwt = get_jwt()
        current_user = get_jwt_identity()
        is_admin = current_jwt.get("is_admin", False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if not is_admin and place.owner_id != current_user:
            return {"error": "Unauthorized action"}, 403

        try:
            updated_place = facade.update_place(place_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400

        return place_to_dict_detail(updated_place), 200


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404

        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
            }
            for review in reviews
        ], 200
