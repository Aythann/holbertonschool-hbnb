# HBnB API
## Project Overview

HBnB is a modular RESTful API built with Flask. The project follows a clean, layered architecture that separates concerns between the API layer, business logic, service layer (Facade pattern), and persistence layer.

The application currently uses an in-memory repository for data storage, which is designed to be replaced later with a database-backed solution such as SQLAlchemy without modifying the upper layers of the application.

## Project Structure
![alt text](image.png)

## Directory and File Description
### app/

Contains the core application logic.

### app/api/

Handles the presentation layer (API endpoints).
The v1/ directory organizes endpoints by API version.

 - users.py – User endpoints
 - places.py – Place endpoints
 - reviews.py – Review endpoints
 -  amenities.py – Amenity endpoints

### app/models/

Contains business logic and domain models:
 - user.py – User model
 - place.py – Place model
 - review.py – Review model
 - amenity.py – Amenity model

### app/services/

Implements the Facade Pattern.
facade.py – Contains the HBnBFacade class
  - Coordinates communication between API, models, and persistence layers
  - A singleton facade instance is created for global use

### app/persistence/

Handles data storage.

repository.py – Defines:
 - Repository (Abstract Base Class)
 - InMemoryRepository (current implementation)

This layer is designed to later support a database-backed repository.

### run.py

Application entry point.
Creates and runs the Flask application.

### config.py

Contains configuration classes for managing environment-specific settings.

### requirements.txt

Lists all required Python dependencies.

## Business Logic Layer

The business logic layer defines the core entities and their relationships:

### User

 - Attributes: id, first_name, last_name, email, is_admin, created_at, updated_at
 - Relationships:
  - One-to-many with Place
  - One-to-many with Review

#### Test:
```
from app.models.user import User

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")

test_user_creation()
```

```
# Create a new user
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'

# Get a single user by ID
curl -X GET http://127.0.0.1:5000/api/v1/users/<user_id>

# List all users
curl -X GET http://127.0.0.1:5000/api/v1/users/
```

### Place

 - Attributes: id, title, description, price, latitude, longitude, owner, created_at, updated_at

 - Relationships:
  - One-to-many with Review
  - Many-to-many with Amenity

#### Test:
```
from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")

test_place_creation()
```

### Review

 - Attributes: id, text, rating, place, user, created_at, updated_at

 - Relationships:
  - Belongs to a Place
  - Written by a User

### Amenity

 - Attributes: id, name, created_at, updated_at

 - Relationships:
  - Many-to-many with Place

#### Test:
```
from app.models.amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()
```

## Installation Instructions
1. Clone the Repository
    - git clone https://github.com/Your_Name/holbertonschool-hbnb.git
    - cd hbnb
2. Create a Virtual Environment
    - python3 -m venv venv

### Activate the virtual environment:

- source venv/bin/activate

3. Install Dependencies
    - pip install -r requirements.txt

4. Run the Application
    - python run.py

The application will start in development mode.

Swagger API documentation will be available at:

http://127.0.0.1:5000/api/v1/

### Desactivate the virtual environment:
- deactivate

## Author

Aythan CRISTOVAO and Vincent RENAUD C#28-Sens
