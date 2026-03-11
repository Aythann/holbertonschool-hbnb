from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace(
    "amenities",
    description="Amenity operations"
)

amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(
            required=True,
            description="Name of the amenity"
        ),
    },
)


@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        current_jwt = get_jwt()

        if not current_jwt.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        try:
            amenity = facade.create_amenity(api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400

        return amenity.to_dict(), 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(403, "Admin privileges required")
    @api.response(404, "Amenity not found")
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        current_jwt = get_jwt()

        if not current_jwt.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        try:
            updated_amenity = facade.update_amenity(
                amenity_id,
                api.payload
            )
        except ValueError as e:
            return {"error": str(e)}, 400

        return updated_amenity.to_dict(), 200
