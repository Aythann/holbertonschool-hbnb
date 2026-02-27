# HBnB Evolution – Part 2  
## Implementation Technical Documentation

---

## 1. Introduction

This document provides the technical implementation documentation for the HBnB Evolution project – Part 2.

While Part 1 focused on UML modeling and architectural design, Part 2 translates that design into a fully functional implementation using Python and Flask.

The objectives of this phase are:

- Implement the layered architecture defined in Part 1  
- Develop the Business Logic layer (core domain models)  
- Implement the Presentation layer (RESTful API endpoints)  
- Implement an in-memory Persistence layer  
- Enforce validation and business rules  
- Maintain strict separation of concerns  
- Implement automated unit and integration tests  

This document ensures that the implementation remains aligned with the architectural blueprint defined previously.

---

## 2. High-Level Architecture (Implementation View)

### 2.1 Architectural Overview

HBnB Evolution – Part 2 follows the same three-layer architecture defined in Part 1:

- Presentation Layer  
- Business Logic Layer  
- Persistence Layer  

The Facade Pattern (HBnBFacade) remains the central orchestrator between layers.

Flow:

Client → API → Facade → Business Logic → Repository → Response

Strict communication rules:

- The API layer communicates only with the Facade.  
- The Facade coordinates business logic and repositories.  
- The Business Logic layer does not depend on Flask.  
- The Persistence layer is abstracted via repositories.  

This preserves:

- Decoupling  
- Modularity  
- Testability  
- Scalability for Part 3 (database integration)  

---

## 3. Project Structure

```hbnb/
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
│   │   ├── validators.py
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

- api/: REST endpoints using Flask-RESTx  
- models/: Domain entities and validation logic  
- services/: Facade implementation  
- persistence/: Repository pattern implementation  
- tests/: Automated unit and integration tests  

---

## 4. Business Logic Layer Implementation

### 4.1 Base Model

All entities inherit from BaseModel, which provides:

- id (UUID string)  
- created_at timestamp  
- updated_at timestamp  
- update() method  
- save() method  

This ensures consistency across domain entities.

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
- email must follow valid format  
- email uniqueness validated via Facade  

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
- price must be ≥ 0  
- latitude must be between -90 and 90  
- longitude must be between -180 and 180  
- owner must exist  
- amenities must reference valid Amenity IDs  

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
- user must exist  
- place must exist  

---

#### Amenity

Attributes:
- id  
- name  

Business rules:
- name required  
- max length enforced  

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

{ id: object }

This enables:

- Fast testing  
- No external dependencies  
- Easy replacement in Part 3 (SQLAlchemy integration)  

---

## 6. Facade Implementation

HBnBFacade centralizes all business operations.

It instantiates:

- user_repo  
- place_repo  
- review_repo  
- amenity_repo  

Responsibilities:

- Enforce cross-entity validation  
- Coordinate repository access  
- Provide clean methods for API layer  

Example responsibilities:

- Verify email uniqueness before user creation  
- Validate owner existence before place creation  
- Validate rating and entity existence before review creation  

---

## 7. REST API Endpoints

Swagger UI available at:

http://127.0.0.1:5000/api/v1/

---

### 7.1 Users

POST /api/v1/users/  
GET /api/v1/users/  
GET /api/v1/users/<user_id>  
PUT /api/v1/users/<user_id>  

No DELETE in Part 2.

---

### 7.2 Amenities

POST /api/v1/amenities/  
GET /api/v1/amenities/  
GET /api/v1/amenities/<amenity_id>  
PUT /api/v1/amenities/<amenity_id>  

No DELETE in Part 2.

---

### 7.3 Places

POST /api/v1/places/  
GET /api/v1/places/  
GET /api/v1/places/<place_id>  
PUT /api/v1/places/<place_id>  

Additional endpoint:

GET /api/v1/places/<place_id>/reviews  

---

### 7.4 Reviews

POST /api/v1/reviews/  
GET /api/v1/reviews/  
GET /api/v1/reviews/<review_id>  
PUT /api/v1/reviews/<review_id>  
DELETE /api/v1/reviews/<review_id>  

Review is the only entity supporting deletion in Part 2.

---

## 8. Testing Strategy

Automated tests are located in the tests/ directory.

- test_models.py: Validates model validation and boundary conditions  
- test_facade.py: Validates business logic and cross-entity rules  
- test_api.py: Validates HTTP status codes and full CRUD flows  

Detailed testing procedures and scenarios are documented in: TESTING.md

---

## 9. Setup and Execution

### 9.1 Create and activate a virtual environment

python3 -m venv venv  
source venv/bin/activate  

### 9.2 Install dependencies

python3 -m pip install -r requirements.txt

### 9.3 Run the application

python3 run.py

---

## 10. Running the Tests

From the project root (part2/hbnb):

python3 -m unittest discover -s tests -p "test_*.py" -v

Optional: generate a test report file

python3 -m unittest discover -s tests -p "test_*.py" -v | tee test_report.txt

Example output (successful run):

Ran 25 tests in 0.032s

OK

---

## 11. Conclusion

HBnB Evolution – Part 2 successfully transforms the UML design from Part 1 into a working RESTful API implementation.

The system maintains:

- Strict layered architecture  
- Facade-based orchestration  
- Repository abstraction  
- Model-level validation  
- Swagger-based documentation  
- Automated test coverage  

This implementation provides a stable and scalable foundation for Part 3, where persistence will transition from in-memory storage to a database-backed solution.
