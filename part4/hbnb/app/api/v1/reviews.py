from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model(
    "Review",
    {
        "text": fields.String(required=True, description="Text of review"),
        "rating": fields.Integer(
            required=True,
            description="Rating of the place (1-5)"
        ),
        "place_id": fields.String(
            required=True,
            description="ID of the place"
        ),
    },
)

update_review_model = api.model(
    "UpdateReview",
    {
        "text": fields.String(description="Text of the review"),
        "rating": fields.Integer(description="Rating of the place (1-5)"),
    },
)


@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Place not found")
    @jwt_required()
    def post(self):
        """Create a new review"""
        current_user = get_jwt_identity()
        current_jwt = get_jwt()
        is_admin = current_jwt.get("is_admin", False)

        data = dict(api.payload or {})
        place = facade.get_place(data.get("place_id"))
        if not place:
            return {"error": "Place not found"}, 404

        if not is_admin and place.owner_id == current_user:
            return {"error": "You cannot review your own place."}, 400

        data["user_id"] = current_user

        try:
            review = facade.create_review(data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return review.to_dict(), 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200


@api.route("/<review_id>")
class ReviewResource(Resource):
    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(update_review_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt_identity()
        current_jwt = get_jwt()
        is_admin = current_jwt.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user_id != current_user:
            return {"error": "Unauthorized action"}, 403

        try:
            updated_review = facade.update_review(review_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400

        return updated_review.to_dict(), 200

    @api.response(200, "Review deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        current_jwt = get_jwt()
        is_admin = current_jwt.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user_id != current_user:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
