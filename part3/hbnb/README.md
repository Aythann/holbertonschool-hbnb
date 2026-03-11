# HBnB Evolution – Part 3
## Implementation Technical Documentation

---

## 1. Introduction

This document provides the technical implementation documentation for the **HBnB Evolution project – Part 3**.

While **Part 2 implemented the application using an in-memory persistence layer**, this phase introduces a **database-backed architecture using SQLAlchemy** and adds **authentication and authorization mechanisms**.

The objectives of this phase are:

- Replace the in-memory persistence layer with **SQLAlchemy ORM**
- Implement **database models and relationships**
- Implement **JWT authentication**
- Enforce **role-based authorization (admin vs user)**
- Maintain the **Facade architecture**
- Ensure **data integrity through database constraints**
- Preserve the **layered architecture**

---

## 2. High-Level Architecture (Implementation View)

### 2.1 Architectural Overview

HBnB Evolution – Part 3 keeps the **three-layer architecture** introduced in previous parts.

The architecture remains composed of:

- **Presentation Layer**
- **Business Logic Layer**
- **Persistence Layer**

The **Facade Pattern (`HBnBFacade`)** continues to orchestrate interactions between layers.

Flow:

Client → API → Facade → Models → Repository → Database

Communication rules remain the same:

- The API layer communicates only with the Facade
- The Facade orchestrates validation and persistence
- The Business Logic layer remains independent from Flask
- Persistence is handled through a **SQLAlchemy repository**

This architecture guarantees:

- Low coupling
- High maintainability
- Clear separation of concerns
- Easy extensibility

---

## 3. Project Structure

```bash
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   │       └── auth.py
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
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

Directory responsibilities:

- api/: REST endpoints
- models/: SQLAlchemy models and validation
- services/: Facade orchestration
- persistence/: Repository abstraction
- config.py: Environment configuration

---

## 4. Database Integration

Part 3 replaces the **in-memory storage** used previously with a **relational database managed through SQLAlchemy ORM**.

The default configuration uses **SQLite**:
```bash
sqlite:///development.db
```
The database is initialized automatically when the application starts:
```bash
db.create_all()
```
---

## 5. SQLAlchemy Models

All models inherit from **BaseModel**, which provides common fields:

- id
- created_at
- updated_at

These fields are implemented using SQLAlchemy columns.

---

## 6. Domain Entities

### 6.1 User

Attributes:

- id
- first_name
- last_name
- email
- password
- is_admin

Features:

- Password hashing using **Flask-Bcrypt**
- Email uniqueness constraint
- Relationship with Places and Reviews

Relationships:
```bash
User 1 → N Places  
User 1 → N Reviews
```
---

### 6.2 Place

Attributes:

- id
- title
- description
- price
- latitude
- longitude
- owner_id

Relationships:
```bash
Place N → 1 User  
Place 1 → N Reviews  
Place N ↔ N Amenities
```
Amenities use a **many-to-many relationship table**.

---

### 6.3 Review

Attributes:

- id
- text
- rating
- user_id
- place_id

Database constraint:
```bash
Unique(user_id, place_id)
```
This prevents a user from reviewing the same place multiple times.

---

### 6.4 Amenity

Attributes:

- id
- name

Used through a **many-to-many relationship** with Places.

---

## 7. Authentication System

Part 3 introduces **JWT authentication** using:
```bash
flask-jwt-extended
```
Authentication endpoint:
```bash
POST /api/v1/auth/login
```
Users authenticate using:
```bash
email + password
```
If credentials are valid, the API returns a **JWT token**.

Example response:
```bash
{
  "access_token": "<JWT_TOKEN>"
}
```
The token must be included in the header:
```bash
Authorization: Bearer <token>
```
---

## 8. Authorization Rules

Role-based permissions are enforced.

### Admin privileges

Admins can:

- Create users
- Modify users
- Manage amenities
- Modify any place or review

### Regular users

Regular users can:

- Modify their own profile
- Create places
- Modify their own places
- Write reviews
- Modify their own reviews

Users cannot:

- Modify other users
- Review their own place
- Review the same place twice

---

## 9. Persistence Layer

The repository pattern remains in place.

`SQLAlchemyRepository` implements:

- add()
- get()
- get_all()
- update()
- delete()
- get_by_attribute()

The repository interacts directly with **SQLAlchemy session management**.

---

## 10. REST API Endpoints

Swagger documentation is available at:
```bash
http://127.0.0.1:5000/api/v1/
```
### Authentication
```bash
POST /api/v1/auth/login
```
### Users
```bash
POST /api/v1/users/  
GET /api/v1/users/  
GET /api/v1/users/<user_id>  
PUT /api/v1/users/<user_id>
```
User creation is restricted to **admin users**.

### Amenities
```bash
POST /api/v1/amenities/  
GET /api/v1/amenities/  
GET /api/v1/amenities/<amenity_id>  
PUT /api/v1/amenities/<amenity_id>
```
Only admins can create or modify amenities.

### Places
```bash
POST /api/v1/places/  
GET /api/v1/places/  
GET /api/v1/places/<place_id>  
PUT /api/v1/places/<place_id>  
GET /api/v1/places/<place_id>/reviews
```
### Reviews
```bash
POST /api/v1/reviews/  
GET /api/v1/reviews/  
GET /api/v1/reviews/<review_id>  
PUT /api/v1/reviews/<review_id>  
DELETE /api/v1/reviews/<review_id>
```
---

## 11. Setup and Execution

### Create a virtual environment
```bash
python3 -m venv venv  
source venv/bin/activate
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Run the application
```bash
python3 run.py
```
---

## 12. Conclusion

HBnB Evolution – Part 3 significantly enhances the application by introducing **database persistence and authentication**.

The project now includes:

- SQLAlchemy ORM integration
- Database-backed persistence
- JWT-based authentication
- Role-based authorization
- Entity relationships
- Data integrity constraints
- Modular architecture using the Facade pattern

The architecture remains clean, modular, and maintainable and prepares the system for further enhancements such as database migrations, pagination, and production deployment.
