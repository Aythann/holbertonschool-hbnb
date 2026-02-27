# HolbertonSchool HBnB Project

## Description

This project consists of building a simplified clone of the Airbnb platform, named **HBnB**, following a progressive and modular approach.

The project is divided into multiple parts, each focusing on a specific aspect of software engineering:

- UML modeling
- Business logic implementation
- REST API development
- Authentication and authorization
- Database integration
- Frontend implementation

The main objective is to design and build a complete web application from conception to implementation while applying industry-standard methodologies such as UML modeling and layered architecture.

---

## Project Objectives

The goals of this project are to:

- Understand and apply UML modeling to describe a software system
- Identify and model a business domain
- Design a clean and scalable application architecture
- Implement backend logic using a layered approach
- Manage authentication and data persistence
- Develop a functional frontend interface
- Apply software engineering best practices
- Work both collaboratively and individually depending on the phase

---

## Project Structure

holbertonschool-hbnb/
├── README.md
├── part1/
│   ├── 01_architecture.mmd
│   ├── 02_class_diagram.mmd
│   ├── 03_sequence_user_registration.mmd
│   ├── 04_sequence_place_creation.mmd
│   ├── 05_sequence_review_submission.mmd
│   ├── 06_sequence_list_places.mmd
│   └── README.md
├── part2/
│   └── hbnb/
│       ├── app/
│       ├── tests/
│       ├── TESTING.md
│       ├── config.py
│       ├── run.py
│       ├── requirements.txt
│       └── README.md
└── part3/
    └── README.md

Each part contains its own documentation explaining objectives, architecture, and implementation details.

---

## Project Parts Overview

### Part 1 – UML & Conception

- Definition of the business domain
- Package Diagram
- Class Diagram
- Sequence Diagrams
- Architectural modeling before implementation

See: part1/README.md

---

### Part 2 – Business Logic & REST API

- Implementation of domain models
- Validation logic
- Facade pattern orchestration
- Repository pattern (in-memory persistence)
- REST API using Flask-RESTx
- Automated unit and integration tests

See:
- part2/hbnb/README.md
- part2/hbnb/TESTING.md

---

### Part 3 – Authentication & Database

- User authentication and authorization
- Database integration (SQLAlchemy)
- Application security
- Final application assembly
- Frontend implementation (individual phase)

See: part3/README.md

---

## Architecture Overview

The application follows a layered architecture separating responsibilities into distinct layers:

- Presentation Layer (API / Frontend)
- Business Logic Layer
- Domain Layer (Entities & Rules)
- Persistence Layer (Data Storage)

This separation ensures:

- Maintainability
- Scalability
- Testability
- Clear responsibility boundaries

---

## Methodology

- UML used as a modeling reference before implementation
- Incremental and iterative development
- Layered architecture enforcement
- Automated testing for validation
- Git-based workflow with structured commits
- Manual code reviews at the end of each phase

---

## Technical Stack

- Python 3
- Flask
- Flask-RESTx
- In-memory Repository Pattern (Part 2)
- SQLAlchemy (Part 3)
- Git version control

---

## Technical Constraints

- Developed following Holberton School guidelines
- Respect of clean architecture principles
- Code quality prioritized over feature quantity
- Manual project validation

---

## Limitations

This project is an educational and simplified version of Airbnb.

Some real-world features are intentionally excluded:

- Online payments
- Messaging system
- Advanced search and filtering
- Refund and cancellation policies
- Production-level security mechanisms

---

## Authors

Project developed by:

- Vincent Renaud
- Aythan Cristovao
