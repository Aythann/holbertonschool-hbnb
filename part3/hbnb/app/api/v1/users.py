from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True,
            description="First name of the user"
        ),
        "last_name": fields.String(
            required=True,
            description="Last name of the user"
        ),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(
            required=True,
            description="Password of the user"
        ),
        "is_admin": fields.Boolean(description="Admin flag"),
    },
)

update_user_model = api.model(
    "UpdateUser",
    {
        "first_name": fields.String(description="First name of the user"),
        "last_name": fields.String(description="Last name of the user"),
        "email": fields.String(description="Email of the user"),
        "password": fields.String(description="Password of the user"),
        "is_admin": fields.Boolean(description="Admin flag"),
    },
)


def _normalize_email(value):
    if value is None:
        return None
    return str(value).strip().lower()


@api.route("/")
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        current_jwt = get_jwt()

        if not current_jwt.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        user_data = api.payload or {}

        email_norm = _normalize_email(user_data.get("email"))
        existing_user = (
            facade.get_user_by_email(email_norm) if email_norm else None
        )
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return {
            "message": "User created successfully",
            "id": new_user.id,
        }, 201

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200


@api.route("/protected")
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {"message": f"Hello, user {current_user}"}, 200


@api.route("/<user_id>")
class UserResource(Resource):
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.expect(update_user_model, validate=True)
    @api.response(200, "User updated successfully")
    @api.response(400, "Invalid input data")
    @api.response(400, "Email already registered")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id):
        """Update user information"""
        current_jwt = get_jwt()
        current_identity = get_jwt_identity()
        is_admin = current_jwt.get("is_admin", False)

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        user_data = dict(api.payload or {})

        if is_admin:
            email = _normalize_email(user_data.get("email"))
            if email:
                existing_user = facade.get_user_by_email(email)
                if existing_user and existing_user.id != user_id:
                    return {"error": "Email already registered"}, 400

            try:
                updated_user = facade.update_user(user_id, user_data)
            except ValueError as e:
                return {"error": str(e)}, 400

            return updated_user.to_dict(), 200

        if str(user.id) != str(current_identity):
            return {"error": "Unauthorized action"}, 403

        if "email" in user_data:
            return {"error": "You cannot modify email or password."}, 400
        if "password" in user_data:
            return {"error": "You cannot modify email or password."}, 400
        if "is_admin" in user_data:
            return {"error": "You cannot modify email or password."}, 400

        allowed_data = {
            key: value
            for key, value in user_data.items()
            if key in {"first_name", "last_name"}
        }

        try:
            updated_user = facade.update_user(user_id, allowed_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return updated_user.to_dict(), 200
