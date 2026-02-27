# HBnB Evolution – Part 2  
## Testing and Validation Report (Task 6)

---

## 1. Overview

This document describes how the HBnB Evolution – Part 2 implementation is validated through:

- Model validation tests (Business Logic)
- Facade tests (Business Logic orchestration)
- API endpoint tests (Presentation layer integration)

The goal is to ensure that:

- Each endpoint respects the expected input/output formats  
- Status codes follow REST conventions  
- Validation rules are enforced correctly  
- Core flows (create, retrieve, update, delete) work as expected  

---

## 2. Test Types

### 2.1 Model Tests (Unit Tests)

File: tests/test_models.py

Covers:

- require_str / require_email / require_float / require_int validations
- Entity instantiation validation:
  - User: email format
  - Place: latitude/longitude bounds
  - Review: rating bounds
  - Amenity: required fields

Expected behavior:

- Valid data creates objects successfully  
- Invalid data raises ValueError  

---

### 2.2 Facade Tests (Unit Tests)

File: tests/test_facade.py

Covers:

- User creation + retrieval
- Email uniqueness enforcement
- Amenity creation + retrieval
- Place creation:
  - Owner existence validation
  - Amenities existence validation
- Review creation:
  - User existence validation
  - Place existence validation
- Review update and delete flows
- Reviews listing by place

Expected behavior:

- Facade raises ValueError / KeyError depending on invalid references  
- Business rules are enforced at the Facade and model level  

---

### 2.3 API Tests (Integration Tests)

File: tests/test_api.py

Covers:

- Users endpoints:
  - POST /api/v1/users/
  - GET /api/v1/users/
  - GET /api/v1/users/<user_id>
  - PUT /api/v1/users/<user_id>
  - Duplicate email (expected 400)
- Amenities endpoints:
  - POST /api/v1/amenities/
  - GET /api/v1/amenities/
  - GET /api/v1/amenities/<amenity_id>
  - PUT /api/v1/amenities/<amenity_id>
- Places endpoints:
  - POST /api/v1/places/
  - GET /api/v1/places/
  - GET /api/v1/places/<place_id>
  - PUT /api/v1/places/<place_id>
  - Invalid latitude boundary (expected 400)
- Reviews endpoints:
  - POST /api/v1/reviews/
  - GET /api/v1/reviews/
  - GET /api/v1/reviews/<review_id>
  - PUT /api/v1/reviews/<review_id>
  - DELETE /api/v1/reviews/<review_id>
  - GET /api/v1/reviews/<review_id> after delete (expected 404)
- Place reviews endpoint:
  - GET /api/v1/places/<place_id>/reviews

Expected behavior:

- 201 Created on successful POST
- 200 OK on successful GET/PUT/DELETE
- 400 Bad Request on invalid payload or validation failure
- 404 Not Found on missing resource

---

## 3. Running the Tests

### 3.1 Setup environment

From the project root (part2/hbnb):

python3 -m venv venv  
source venv/bin/activate  
python3 -m pip install -r requirements.txt  

---

### 3.2 Execute all tests

python3 -m unittest discover -s tests -p "test_*.py" -v

---

### 3.3 Generate a test report file

python3 -m unittest discover -s tests -p "test_*.py" -v | tee test_report.txt

---

## 4. Test Results

Example successful run:

- 25 tests executed
- 0 failures
- 0 errors

Output:

Ran 25 tests in 0.032s

OK

---

## 5. Notes

- Tests are executed against an in-memory repository (Part 2 requirement).
- The test suite is designed to be compatible with Part 3, where the persistence layer will be replaced by a database-backed implementation.
