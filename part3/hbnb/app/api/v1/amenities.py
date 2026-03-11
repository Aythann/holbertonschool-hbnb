from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(required=True, description="Name of the amenity"),
    },
)


@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    
    @jwt_required()
    def post(self):
        """Register a new amenity"""
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
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


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
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")

    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_jwt = get_jwt()
        if not current_jwt.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        try:
            amenity = facade.update_amenity(amenity_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return {"message": "Amenity updated successfully"}, 200
