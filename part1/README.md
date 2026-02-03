# HBnB Evolution – Part 1  
## UML Technical Documentation

---

## 1. Introduction

This document contains the **UML technical documentation** for the HBnB Evolution project.

The purpose of this documentation is to define the **architecture**, **business logic design**, and **interaction flows** of the system **prior to implementation**, using standard UML diagrams.

This document serves as a **design blueprint** for the next development phases.

---

## 2. High-Level Architecture (Package Diagram)

### 2.1 Overview

The HBnB application follows a **three-layered architecture**:

- **Presentation Layer**: Manages API endpoints and user interactions.
- **Business Logic Layer**: Contains the core domain models and business rules.
- **Persistence Layer**: Handles data storage and retrieval.

A **Facade Pattern** is used to centralize communication between the Presentation Layer and the Business Logic Layer, ensuring clear separation of concerns.

---

### 2.2 High-Level Package Diagram

📄 `01_architecture.mmd`

This UML package diagram illustrates:
- The separation between application layers
- The central role of the Facade
- Communication pathways between system components

---

## 3. Business Logic Layer (Class Diagram)

### 3.1 Overview

The Business Logic Layer models the main entities of the system:

- `User`
- `Place`
- `Review`
- `Amenity`

All entities:
- Use UUIDs as unique identifiers
- Track creation and update timestamps
- Inherit from a common abstract base entity

---

### 3.2 Detailed Class Diagram

📄 `02_class_diagram.mmd`

This UML class diagram describes:
- Entity attributes and methods
- Inheritance relationships
- Associations and multiplicities between entities

---

## 4. API Interaction Flow (Sequence Diagrams)

This section presents UML sequence diagrams that illustrate interactions between system layers for key API use cases.

Each sequence diagram shows the flow of messages between:
- Presentation Layer
- Business Logic Layer (Facade)
- Persistence Layer

---

### 4.1 User Registration

📄 `03_sequence_user_registration.mmd`

Illustrates the sequence of interactions required to register a new user.

---

### 4.2 Place Creation

📄 `04_sequence_place_creation.mmd`

Illustrates the creation of a new place associated with a user.

---

### 4.3 Review Submission

📄 `05_sequence_review_submission.mmd`

Illustrates the submission of a review by a user for a specific place.

---

### 4.4 Fetching a List of Places

📄 `06_sequence_list_places.mmd`

Illustrates the retrieval of a list of places based on request criteria.

---

## 5. Conclusion

This document provides a complete UML-based representation of the HBnB Evolution system, including:

- High-level architectural design
- Detailed business logic modeling
- Interaction flows for core API operations

It serves as the reference documentation for the implementation phases of the project.
