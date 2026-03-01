# HBnB Evolution – Part 2
## Implementation Technical Documentation

---

## 1. Introduction

This document provides the technical implementation documentation for the HBnB Evolution project – Part 2.

While Part 1 focused on UML modeling and architectural design, Part 2 translates that design into a functional implementation using Python and Flask.

The objectives of this phase are:

- Implement the layered architecture defined in Part 1
- Develop the Business Logic layer (core domain models)
- Implement the Presentation layer (RESTful API endpoints)
- Implement an in-memory Persistence layer
- Enforce validation and business rules
- Maintain separation of concerns via the Facade pattern
- Implement automated unit and integration tests

---

## 2. High-Level Architecture (Implementation View)

### 2.1 Architectural Overview

HBnB Evolution – Part 2 follows the three-layer architecture:

- Presentation Layer
- Business Logic Layer
- Persistence Layer

The Facade Pattern (`HBnBFacade`) orchestrates interactions between layers.

Flow:

Client → API → Facade → Models (Business Rules) → Repository → Response

Communication rules:

- The API layer communicates only with the Facade.
- The Facade coordinates validation and repository access.
- The Business Logic layer does not depend on Flask.
- The Persistence layer is abstracted via repositories.

This ensures:

- Decoupling
- Modularity
- Testability
- Smooth transition to Part 3 (SQLAlchemy persistence)

---

## 3. Project Structure
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   └── persistence/
│       └── repository.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_facade.py
│   └── test_api.py
├── TESTING.md
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

Each directory has a specific responsibility:

- `api/`: REST endpoints using Flask-RESTx
- `models/`: Domain entities and validation logic
- `services/`: Facade implementation
- `persistence/`: Repository pattern implementation
- `tests/`: Automated unit and integration tests

---

## 4. Business Logic Layer Implementation

### 4.1 Base Model

All entities inherit from `BaseModel`, which provides:

- `id` (UUID string)
- `created_at` timestamp
- `updated_at` timestamp
- `save()` method
- `update()` method (overridden in models to enforce validation)

---

### 4.2 Domain Entities

#### User

Attributes:
- id
- first_name
- last_name
- email
- is_admin
- created_at
- updated_at

Business rules:
- first_name and last_name required
- email must follow a valid format
- email is normalized to lowercase in the model
- email uniqueness is enforced through the Facade before persistence

Updates:
- `User.update()` enforces the same validation rules as creation

---

#### Place

Attributes:
- id
- title
- description
- price
- latitude
- longitude
- owner_id
- amenities (list of amenity IDs)

Business rules:
- title required
- price must be ≥ 0
- latitude must be between -90 and 90
- longitude must be between -180 and 180
- owner must exist (validated via Facade)
- amenities must reference valid Amenity IDs (validated via Facade)

Updates:
- `Place.update()` enforces validation rules for updated fields
- `owner_id` is not updatable (rejected via Facade)

---

#### Review

Attributes:
- id
- text
- rating
- user_id
- place_id

Business rules:
- text required
- rating must be between 1 and 5
- user must exist (validated via Facade)
- place must exist (validated via Facade)

Updates:
- Review updates are partial (text and/or rating)
- `user_id` and `place_id` are not updatable (rejected via Facade)

---

#### Amenity

Attributes:
- id
- name

Business rules:
- name required
- max length enforced (50)

Updates:
- `Amenity.update()` validates name updates

---

## 5. Persistence Layer Implementation

### 5.1 Repository Pattern

An abstract Repository defines:

- add()
- get()
- get_all()
- update()
- delete()
- get_by_attribute()

### 5.2 InMemoryRepository

Uses a dictionary for storage:

`{ id: object }`

This enables:

- Fast testing
- No external dependencies
- Easy replacement in Part 3 (SQLAlchemy integration)

---

## 6. Facade Implementation

`HBnBFacade` centralizes all operations.

Repositories:
- user_repo
- place_repo
- review_repo
- amenity_repo

Responsibilities:
- Cross-entity validation (owner/user/place existence)
- Amenities ID validation for places
- Enforce update constraints for relationships:
  - owner_id cannot be updated on Place
  - user_id/place_id cannot be updated on Review

---

## 7. REST API Endpoints

Swagger UI is available at:

http://127.0.0.1:5000/api/v1/

---

### 7.1 Users

- POST `/api/v1/users/`
- GET `/api/v1/users/`
- GET `/api/v1/users/<user_id>`
- PUT `/api/v1/users/<user_id>`

No DELETE in Part 2.

Notes:
- Password is not part of this part.
- Email uniqueness is checked before creation/update.

---

### 7.2 Amenities

- POST `/api/v1/amenities/`
- GET `/api/v1/amenities/`
- GET `/api/v1/amenities/<amenity_id>`
- PUT `/api/v1/amenities/<amenity_id>`

No DELETE in Part 2.

---

### 7.3 Places

- POST `/api/v1/places/`
- GET `/api/v1/places/`  
  Returns a minimal representation (id, title, latitude, longitude)
- GET `/api/v1/places/<place_id>`  
  Returns an enriched representation including owner details and amenities
- PUT `/api/v1/places/<place_id>`  
  Partial update (only provided fields are updated)

Additional endpoint:
- GET `/api/v1/places/<place_id>/reviews`  
  Returns reviews for a place (minimal review representation)

---

### 7.4 Reviews

- POST `/api/v1/reviews/`
- GET `/api/v1/reviews/`  
  Returns a minimal representation (id, text, rating)
- GET `/api/v1/reviews/<review_id>`
- PUT `/api/v1/reviews/<review_id>`  
  Partial update (text and/or rating only)
- DELETE `/api/v1/reviews/<review_id>`

Review is the only entity supporting deletion in Part 2.

---

## 8. Testing Strategy

Automated tests are located in the `tests/` directory.

- `test_models.py`: Validates model rules and boundary conditions
- `test_facade.py`: Validates business logic, cross-entity rules, and forbidden updates
- `test_api.py`: Validates HTTP status codes and full CRUD flows (including error cases)

Detailed testing procedures and scenarios are documented in: `TESTING.md`

---

## 9. Setup and Execution

### 9.1 Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```
### 9.2 Install dependencies
```bash
python3 -m pip install -r requirements.txt
```
### 9.3 Run the application
```bash
python3 run.py
```
---

## 10. Running the Tests

From the project root (part2/hbnb):
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```
Optional: generate a test report file
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v | tee test_report.txt
```
---

## 11. Conclusion

HBnB Evolution – Part 2 successfully implements the core business logic and RESTful API defined in Part 1.

The project now provides:

- A strict layered architecture (Presentation, Business Logic, Persistence)
- Centralized orchestration through the Facade pattern
- In-memory persistence using the Repository pattern
- Model-level validation on both creation and updates
- Cross-entity integrity enforcement (owner, user, place validation)
- Partial updates for Places and Reviews, aligned with REST best practices
- Minimal and detailed response representations where appropriate
- Swagger-based API documentation
- Automated unit and integration test coverage

The system is modular, testable, and maintainable.  
It respects separation of concerns and prepares the codebase for Part 3, where the persistence layer will transition from in-memory storage to a database-backed solution.

HBnB Evolution – Part 2 therefore establishes a solid and scalable foundation for future enhancements.
