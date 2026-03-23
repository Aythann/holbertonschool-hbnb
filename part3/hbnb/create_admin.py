from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    existing_user = User.query.filter_by(email="admin@hbnb.io").first()

    if existing_user:
        print("Admin already exists:", existing_user.email)
    else:
        admin = User(
            first_name="admin",
            last_name="hbnb",
            email="admin@hbnb.io",
            password="admin123",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully.")