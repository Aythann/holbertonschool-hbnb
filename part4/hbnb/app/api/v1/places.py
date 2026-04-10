from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from app.services import facade

api = Namespace(
    "places",
    description="Place operations"
)

amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(
            description="Amenity ID"
        ),
        "name": fields.String(
            description="Amenity name"
        ),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(
            description="User ID"
        ),
        "first_name": fields.String(
            description="Owner first name"
        ),
        "last_name": fields.String(
            description="Owner last name"
        ),
        "email": fields.String(
            description="Owner email"
        ),
        "is_admin": fields.Boolean(
            description="Admin flag"
        ),
    },
)

review_model = api.model(
    "PlaceReview",
    {
        "id": fields.String(
            description="Review ID"
        ),
        "text": fields.String(
            description="Review text"
        ),
        "rating": fields.Integer(
            description="Rating 1 to 5"
        ),
        "user_id": fields.String(
            description="Author user id"
        ),
    },
)

place_model = api.model(
    "Place",
    {
        "title": fields.String(
            required=True,
            description="Place title"
        ),
        "description": fields.String(
            description="Place description"
        ),
        "price": fields.Float(
            required=True,
            description="Price per night"
        ),
        "latitude": fields.Float(
            required=True,
            description="Latitude"
        ),
        "longitude": fields.Float(
            required=True,
            description="Longitude"
        ),
        "amenities": fields.List(
            fields.String,
            description="Amenity ids"
        ),
    },
)

update_place_model = api.model(
    "UpdatePlace",
    {
        "title": fields.String(
            description="Place title"
        ),
        "description": fields.String(
            description="Place description"
        ),
        "price": fields.Float(
            description="Price per night"
        ),
        "latitude": fields.Float(
            description="Latitude"
        ),
        "longitude": fields.Float(
            description="Longitude"
        ),
        "amenities": fields.List(
            fields.String,
            description="Amenity ids"
        ),
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
    owner = None
    if place.owner_id:
        owner = facade.get_user(place.owner_id)

    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": owner.to_dict() if owner else None,
        "amenities": [
            amenity.to_dict()
            for amenity in place.amenities
        ],
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
    @api.response(201, "Place created")
    @api.response(400, "Invalid data")
    @jwt_required()
    def post(self):
        """Create a new place"""

        current_user = get_jwt_identity()

        data = dict(api.payload or {})
        data["owner_id"] = current_user

        try:
            place = facade.create_place(data)
        except ValueError as error:
            return {"error": str(error)}, 400

        return place_to_dict_detail(place), 201

    @api.response(200, "Places retrieved")
    def get(self):
        """Retrieve all places"""

        places = facade.get_all_places()

        return [
            place_to_dict_list(place)
            for place in places
        ], 200


@api.route("/<place_id>")
class PlaceResource(Resource):

    @api.response(200, "Place retrieved")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place by id"""

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return place_to_dict_detail(place), 200

    @api.expect(update_place_model, validate=True)
    @api.response(200, "Place updated")
    @api.response(400, "Invalid data")
    @api.response(403, "Unauthorized")
    @api.response(404, "Place not found")
    @jwt_required()
    def put(self, place_id):
        """Update a place"""

        current_jwt = get_jwt()
        current_user = get_jwt_identity()

        is_admin = current_jwt.get("is_admin", False)

        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        if not is_admin and place.owner_id != current_user:
            return {"error": "Unauthorized action"}, 403

        try:
            updated_place = facade.update_place(
                place_id,
                api.payload
            )
        except ValueError as error:
            return {"error": str(error)}, 400

        return place_to_dict_detail(updated_place), 200


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):

    @api.response(200, "Reviews retrieved")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get reviews for a place"""

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
