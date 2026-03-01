# HBnB Evolution – Part 2  
## Testing and Validation Report (Task 6)

---

## 1. Overview

This document describes how the HBnB Evolution – Part 2 implementation is validated through:

- Model validation tests (Business Logic layer)
- Facade tests (Business Logic orchestration)
- API endpoint tests (Presentation layer integration)

The objective is to ensure that:

- All validation rules are enforced at model and facade level
- Relationship integrity between entities is respected
- REST endpoints follow correct input/output formats
- HTTP status codes comply with REST conventions
- Full CRUD flows behave as expected

---

## 2. Test Types

### 2.1 Model Tests (Unit Tests)

File: `tests/test_models.py`

Covers:

- Entity instantiation validation:
  - User: required fields and email format
  - Place: price ≥ 0, latitude/longitude bounds
  - Review: rating between 1 and 5
  - Amenity: required name
- Model update validation:
  - User.update() enforces email format and required fields
  - Place.update() enforces bounds and numeric constraints
  - Review.update() enforces rating range
  - Amenity.update() enforces required name

Expected behavior:

- Valid data creates objects successfully
- Invalid data raises `ValueError`
- Update operations respect the same constraints as creation

---

### 2.2 Facade Tests (Unit Tests)

File: `tests/test_facade.py`

Covers:

- User creation and retrieval
- Case-insensitive email lookup
- Email uniqueness enforcement
- Amenity creation and update validation
- Place creation:
  - Owner existence validation
  - Amenities existence validation
- Place update:
  - Partial update support
  - Rejection of owner_id modification
- Review creation:
  - User existence validation
  - Place existence validation
- Review update:
  - Partial update support
  - Rejection of user_id/place_id modification
- Review deletion
- Reviews retrieval by place

Expected behavior:

- `ValueError` is raised when business rules are violated
- Cross-entity constraints are enforced at the Facade level
- Relationship integrity is preserved

---

### 2.3 API Tests (Integration Tests)

File: `tests/test_api.py`

Covers full endpoint integration:

#### Users
- POST `/api/v1/users/`
- GET `/api/v1/users/`
- GET `/api/v1/users/<user_id>`
- PUT `/api/v1/users/<user_id>` (partial update)
- Duplicate email (expected 400)
- Invalid email (expected 400)
- Non-existing user (expected 404)

#### Amenities
- POST `/api/v1/amenities/`
- GET `/api/v1/amenities/`
- GET `/api/v1/amenities/<amenity_id>`
- PUT `/api/v1/amenities/<amenity_id>`
- Invalid name (expected 400)
- Non-existing amenity (expected 404)

#### Places
- POST `/api/v1/places/`
- GET `/api/v1/places/` (minimal representation)
- GET `/api/v1/places/<place_id>` (detailed representation)
- PUT `/api/v1/places/<place_id>` (partial update)
- Invalid latitude/longitude (expected 400)
- Invalid owner or amenity reference (expected 400)
- Non-existing place (expected 404)
- GET `/api/v1/places/<place_id>/reviews`

#### Reviews
- POST `/api/v1/reviews/`
- GET `/api/v1/reviews/` (minimal representation)
- GET `/api/v1/reviews/<review_id>`
- PUT `/api/v1/reviews/<review_id>` (partial update)
- DELETE `/api/v1/reviews/<review_id>`
- Invalid rating (expected 400)
- Forbidden relationship update (expected 400)
- Non-existing review (expected 404)

Expected HTTP behavior:

- 201 Created on successful POST
- 200 OK on successful GET/PUT/DELETE
- 400 Bad Request on validation failure
- 404 Not Found on missing resource

---

## 3. Running the Tests

### 3.1 Setup environment

From the project root (`part2/hbnb`):

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```
### 3.2 Execute all tests

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```
### 3.3 Generate a test report file

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v | tee test_report.txt
```
## 4. Test Results

Example successful execution:

- 25 tests executed  
- 0 failures  
- 0 errors  

Sample output:

Ran 25 tests in 0.032s

OK

The successful execution confirms that:

- All validation rules are correctly enforced
- Cross-entity constraints behave as expected
- REST endpoints return appropriate HTTP status codes
- Partial updates function correctly
- Relationship integrity is preserved
- Error handling (400 / 404 cases) works as intended

---

## 5. Notes

- All tests are executed against the in-memory repository implementation, as required for Part 2.
- The test suite combines unit tests (models and facade) with integration tests (API endpoints).
- The architecture allows the persistence layer to be replaced in Part 3 without impacting business logic tests.
- The separation of concerns ensures that validation remains consistent across model, facade, and API layers.

The test coverage provides confidence that the system behaves reliably under both valid and invalid input scenarios.
