from flask_restx import Namespace, Resource, fields
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
    def post(self):
        amenity = facade.create_amenity(api.payload)
        return amenity.to_dict(), 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    def put(self, amenity_id):
        amenity = facade.update_amenity(amenity_id, api.payload)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {"message": "Amenity updated successfully"}, 200