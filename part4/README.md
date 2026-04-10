# HBnB Evolution – Part 4
## Simple Web Client – Technical Documentation

---

## 1. Introduction

This document provides the technical implementation documentation for HBnB Evolution – Part 4.

After implementing a fully functional back-end API in Part 3, this phase introduces a client-side web application built with:

- HTML5
- CSS3
- JavaScript ES6

The objective of this part is to create a dynamic and interactive web client that communicates with the API.

---

## 2. Objectives

- Build a user-friendly interface
- Interact with the API using the Fetch API
- Implement authentication using JWT stored in cookies
- Dynamically update the UI without page reloads
- Follow modern front-end development practices

---

## 3. Project Structure
```bash
front/
├── index.html
├── login.html
├── place.html
├── add_review.html
├── styles.css
├── scripts.js
└── images/
    ├── logo.png
    └── icon.png
```
---

## 4. Application Architecture

User → Browser → JavaScript → API (Flask backend)

---

## 5. Task 1 – Design Implementation

- Semantic HTML structure (header, main, footer)
- Reusable components (cards, navigation)
- Responsive layout using CSS Grid
- Consistent margins, padding and borders
- Pages implemented:
  - Login
  - Places list
  - Place details
  - Add review

---

## 6. Task 2 – Login Functionality

API endpoint:
```bash
POST /api/v1/auth/login
```
Process:

User submits email + password
Fetch API sends request
JWT token returned if valid
Token stored in cookie
Redirect to index page

Example:
document.cookie = "token=<JWT>; path=/";

Error handling:
Displays error message if login fails

---

7. Task 3 – View Places

API endpoint:
GET /api/v1/places/

Features:
- Dynamic rendering of places
- Display:
  - Title
  - Price
  - Details button

Filtering:
- Client-side filtering (10 / 50 / 100 / All)
- No page reload

Authentication:
- Login link hidden if authenticated

---

8. Task 4 – Place Details

API endpoint:
GET /api/v1/places/<id>

Displays:
- Title
- Host
- Price
- Description
- Amenities

Reviews:
- Displayed dynamically
- Includes:
  - User name
  - Comment
  - Rating (stars)

Access:
- Add review button visible only if logged in

---

9. Task 5 – Add Review

API endpoint:
POST /api/v1/reviews/

Process:
- Check authentication
- Retrieve place ID from URL
- Submit review (text + rating)

Validation:
- Text required
- Rating between 1 and 5

Result:
- Success message
- Redirect to place page

---

10. JavaScript Implementation

Centralized logic in scripts.js

Page detection:
document.body.dataset.page

Functions:
- initLoginPage()
- initIndexPage()
- initPlacePage()
- initAddReviewPage()

API handling:
apiFetch()

Authentication:
- getCookie()
- setCookie()
- deleteCookie()

---

11. UI Enhancements

Star rating display:
★★★★★
★★★★☆
★★★☆☆

Improvements:
- Clean review layout
- User name displayed instead of ID

---

12. Backend Dependency

Expected review format:
{
  "text": "Great place",
  "rating": 5,
  "user": {
    "first_name": "John",
    "last_name": "Doe"
  }
}

Implemented in:
Review.to_dict()

---

13. How to Test

Start backend:
python3 run.py

Open client:
Open index.html in browser

Test login:
- Go to login.html
- Enter credentials
- Verify cookie and redirect

Test places:
- View list
- Use filter
- Click details

Test reviews:
- Check stars
- Check user name

Test add review:
- Must be logged in
- Submit review
- Verify redirect

---

14. Code Quality

- Modular JavaScript
- Reusable functions
- Clean structure
- Error handling
- Separation of concerns

---

15. Conclusion

Part 4 introduces a fully functional front-end interacting with the API.

Features:
- Dynamic UI
- Authentication
- API integration
- Interactive experience

Full workflow:
Frontend → API → Database