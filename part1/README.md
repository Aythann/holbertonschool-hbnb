# HBnB Evolution – Part 1  
# UML Technical Documentation

---

# 1. Introduction

## 1.1 Purpose of This Document

This document provides the complete UML technical documentation for the HBnB Evolution project (Part 1).

Its purpose is to define the system architecture, domain model, and API interaction flows before implementation begins.

This document serves as a technical blueprint that:

- Establishes a clear architectural structure  
- Defines responsibilities across layers  
- Ensures strict separation of concerns  
- Guides implementation decisions  
- Maintains consistency throughout development  

All implementation phases must remain aligned with the architectural decisions described in this document.

---

## 1.2 Project Overview

HBnB Evolution is a simplified accommodation booking platform inspired by modern rental applications.

The system allows users to:

- Register and manage accounts  
- Create and manage places  
- Add and associate amenities  
- Submit reviews  
- Search for places using filters  

The objective of Part 1 is to design a clean and scalable architecture using UML diagrams before writing any production code.

---

# 2. High-Level Architecture

## 2.1 Architectural Overview

HBnB Evolution follows a strict layered architecture composed of three main layers:

- **Presentation Layer**  
  Handles HTTP requests, input validation, authentication, and response formatting.

- **Business Logic Layer**  
  Contains the domain models and enforces business rules.

- **Persistence Layer**  
  Manages data storage and retrieval through repositories.

A **Facade Pattern** is implemented through `HBnBFacade`, which centralizes communication between the Presentation Layer and the Business Logic Layer.

This ensures:

- Clear responsibility separation  
- Reduced coupling  
- Improved maintainability  
- Better scalability  

---

## 2.2 High-Level Package Diagram

📄 `01_architecture.mmd`

This diagram illustrates:

- The three-layered structure  
- The central role of `HBnBFacade`  
- The communication flow between layers  

The Presentation Layer communicates only with the Facade.  
The Business Logic Layer interacts with the Persistence Layer exclusively through repositories.

Strict layering prevents cross-layer dependencies and preserves architectural integrity.

---

# 3. Business Logic Layer

## 3.1 Overview

The Business Logic Layer models the core entities of the HBnB system:

- `User`  
- `Place`  
- `Review`  
- `Amenity`  

All entities:

- Use UUID as unique identifiers  
- Track creation and update timestamps  
- Inherit from a shared abstract `BaseEntity`  

This ensures structural consistency and centralized lifecycle management.

---

## 3.2 Design Principles

The Business Logic Layer follows object-oriented design principles:

- Encapsulation of entity behavior  
- Separation of domain rules from infrastructure  
- Explicit relationship definitions with multiplicities  
- Validation of business constraints within the domain  

Business rules are enforced at this layer rather than in the API or persistence layer.

Examples of enforced rules:

- Email must be unique  
- Price must be positive  
- Latitude must be between -90 and 90  
- Longitude must be between -180 and 180  
- Review rating must be between 1 and 5  

---

## 3.3 Detailed Class Diagram

📄 `02_class_diagram.mmd`

This diagram describes:

- Attributes and methods of each entity  
- Inheritance from `BaseEntity`  
- Relationships between entities  
- Association multiplicities  

Key relationships:

- One `User` owns many `Place`  
- One `Place` has many `Review`  
- One `User` writes many `Review`  
- `Place` and `Amenity` have a many-to-many relationship  

---

# 4. API Interaction Flow

Each API request follows a consistent lifecycle:

1. Client sends HTTP request  
2. API validates input and authentication  
3. API calls `HBnBFacade`  
4. Facade delegates to Business Logic  
5. Business Logic validates domain rules  
6. Repository handles persistence  
7. Structured response is returned to the client  

This strict sequence enforces clean separation and predictable behavior.

---

## 4.1 User Registration

📄 `03_sequence_user_registration.mmd`

This sequence diagram illustrates:

- Payload validation  
- Email uniqueness verification  
- User entity creation  
- Persistence through `UserRepository`  
- Error handling (409 Conflict if email already exists)  

---

## 4.2 Place Creation

📄 `04_sequence_place_creation.mmd`

This sequence diagram illustrates:

- Authentication and payload validation  
- Owner verification  
- Business rule validation (price, coordinates)  
- Optional amenity validation  
- Place creation and persistence  

---

## 4.3 Review Submission

📄 `05_sequence_review_submission.mmd`

This sequence diagram illustrates:

- Authentication  
- Place existence verification  
- User existence verification  
- Rating validation  
- Review creation and persistence  

---

## 4.4 Fetching a List of Places

📄 `06_sequence_list_places.mmd`

This sequence diagram illustrates:

- Query parameter validation  
- Business filter validation  
- Repository search execution  
- Structured response return  

---

# 5. Design Decisions and Rationale

## 5.1 Layered Architecture

The layered architecture was chosen to:

- Improve modularity  
- Facilitate testing  
- Allow independent layer evolution  
- Prevent tight coupling  

---

## 5.2 Facade Pattern

The `HBnBFacade`:

- Provides a unified entry point for use cases  
- Orchestrates business operations  
- Prevents direct interaction between API and domain logic  

This improves maintainability and clarity.

---

## 5.3 Repository Pattern

Repositories abstract data persistence.

This enables:

- Database flexibility  
- Clean separation between business rules and storage logic  
- Easier mocking during testing  

---

## 5.4 Strict Layer Separation

Strict separation:

- Prevents domain leakage into the API layer  
- Makes refactoring easier  
- Improves scalability  
- Supports potential migration to microservices  

---

# 6. Future Improvements

Possible future enhancements include:

- JWT-based authentication  
- Pagination for search endpoints  
- Caching layer for performance optimization  
- Advanced filtering capabilities  
- Asynchronous processing for heavy operations  

---

# 7. Conclusion

This document provides a complete UML-based representation of the HBnB Evolution system.

It includes:

- High-level architectural design  
- Detailed domain modeling  
- Interaction flows for core API operations  
- Architectural design decisions and rationale  

This documentation serves as the structural reference for all implementation phases of the project.

It ensures consistency, maintainability, and clarity throughout development.