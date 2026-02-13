# HBnB Evolution – Part 1  
## UML Technical Documentation

---

## 1. Introduction

This document provides the UML technical documentation for the HBnB Evolution project.

Its objective is to define the system’s architecture, core business logic design, and interaction flows before implementation begins.

By modeling the system using standard UML diagrams, this document:

- Establishes a clear architectural structure  
- Defines responsibilities across system layers  
- Ensures separation of concerns  
- Serves as a reference blueprint for development  

This documentation guarantees that implementation decisions remain aligned with the designed architecture.

---

## 2. High-Level Architecture (Package Diagram)

### 2.1 Architectural Overview

HBnB Evolution follows a layered architecture composed of three main layers:

- Presentation Layer – Handles API endpoints, request validation, authentication, and response formatting.
- Business Logic Layer – Contains domain models and enforces business rules.
- Persistence Layer – Manages data storage and retrieval through repositories.

A Facade Pattern (HBnBFacade) centralizes communication between the Presentation Layer and the Business Logic Layer.

This ensures:

- Decoupling between API and domain logic  
- Clear responsibility separation  
- Improved maintainability  
- Better scalability for future extensions  

---

### 2.2 High-Level Package Diagram

📄 `01_architecture.mmd`

This diagram illustrates:

- The three-layered structure  
- The central role of HBnBFacade  
- The communication flow between layers  

The Presentation Layer communicates only with the Facade.  
The Business Logic Layer interacts with the Persistence Layer through repositories.  

This strict layering prevents cross-layer coupling.

---

## 3. Business Logic Layer (Class Diagram)

### 3.1 Overview

The Business Logic Layer models the core entities of the HBnB system:

- User  
- Place  
- Review  
- Amenity  

All entities:

- Use UUID as unique identifiers  
- Track creation and update timestamps  
- Inherit from a shared abstract BaseEntity  

This ensures consistency across the domain model.

---

### 3.2 Design Principles

The Business Logic Layer follows object-oriented design principles:

- Encapsulation of entity behavior  
- Separation of domain rules from infrastructure  
- Clear relationship definitions with explicit multiplicities  

Business rules are enforced at this layer rather than in the API or persistence layer.

Examples of enforced rules:

- Email must be unique  
- Price must be positive  
- Latitude and longitude must be valid  
- Review rating must be between 1 and 5  

---

### 3.3 Detailed Class Diagram

📄 `02_class_diagram.mmd`

This diagram describes:

- Attributes and methods of each entity  
- Inheritance from BaseEntity  
- Relationships between entities  
- Association multiplicities  

Key relationships:

- One User owns many Places  
- One Place has many Reviews  
- One User writes many Reviews  
- Place and Amenity have a many-to-many relationship  

---

## 4. API Interaction Flow (Sequence Diagrams)

This section presents sequence diagrams illustrating how the system processes key API requests.

Each diagram demonstrates:

- Strict layer separation  
- The role of the Facade  
- Business rule validation  
- Repository interaction  
- Error handling  

The general flow pattern is:

Client → API → Facade → Business Logic → Repository → Response

---

### 4.1 User Registration

📄 `03_sequence_user_registration.mmd`

This diagram illustrates:

- Payload validation  
- Email uniqueness verification  
- User creation  
- Persistence via UserRepository  
- Proper error handling (409 Conflict if email exists)  

---

### 4.2 Place Creation

📄 `04_sequence_place_creation.mmd`

This diagram illustrates:

- Authentication and payload validation  
- Owner verification  
- Business rule validation (price, coordinates)  
- Optional amenity validation  
- Place persistence  

---

### 4.3 Review Submission

📄 `05_sequence_review_submission.mmd`

This diagram illustrates:

- Authentication  
- Place existence verification  
- User existence verification  
- Rating validation  
- Review creation and persistence  

---

### 4.4 Fetching a List of Places

📄 `06_sequence_list_places.mmd`

This diagram illustrates:

- Query parameter validation  
- Filter normalization  
- Repository search execution  
- Structured response return  

---

## 5. Design Decisions and Rationale

### 5.1 Layered Architecture

The layered architecture was chosen to:

- Improve modularity  
- Facilitate testing  
- Enable independent evolution of layers  
- Reduce tight coupling  

---

### 5.2 Facade Pattern

The HBnBFacade:

- Provides a unified entry point for use cases  
- Orchestrates business operations  
- Prevents direct interaction between API and domain logic  

This improves clarity and maintainability.

---

### 5.3 Repository Pattern

Repositories abstract data persistence.

This allows:

- Flexibility in database implementation  
- Clean separation between business rules and storage logic  
- Easier mocking during testing  

---

## 6. Conclusion

This document provides a complete UML-based representation of the HBnB Evolution system.

It includes:

- High-level architectural design  
- Detailed domain modeling  
- Interaction flows for core API operations  

This documentation serves as the structural reference for all implementation phases of the project.

It ensures architectural consistency, maintainability, and clarity throughout development.