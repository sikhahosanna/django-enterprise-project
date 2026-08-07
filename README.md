

# Django Enterprise Project

## Overview

A professional Django REST Framework backend project with JWT-based authentication, PostgreSQL database integration, API documentation, testing, and version control.

This project provides a complete authentication module for a mobile application backend.

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Django | Backend Framework |
| Django REST Framework | API Development |
| PostgreSQL | Database Management |
| Simple JWT | JWT Authentication |
| drf-spectacular | API Documentation |
| Postman | API Testing |
| Git | Version Control |

---

# Project Structure

```

myproject/

├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── core/
│
├── common/
│
├── myproject/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
└── requirements.txt

```

---

# Features Completed

- Django project setup
- PostgreSQL database configuration
- Environment variable configuration
- Django REST Framework setup
- Custom User Model
- Email based authentication
- JWT Authentication
- Access Token generation
- Refresh Token generation
- Protected APIs
- Change Password API
- Logout API with Token Blacklist
- Swagger Documentation
- Postman API Testing
- Git Version Control

---

# Authentication Module Development

## Epic

Authentication Module Development

---

# Objective

The objective of this module is to develop a secure authentication system using JWT authentication.

The module supports:

- User Registration
- Email Based Login
- JWT Authentication
- Access and Refresh Tokens
- Protected APIs
- Password Management
- Logout with Token Blacklisting
- API Documentation

---

# Task 1 — Study Authentication Flow

## Purpose

Understand complete authentication lifecycle and security flow.

---

## Registration Flow

```

User
|
Enter Email and Password
|
Registration API
|
Serializer Validation
|
Check Duplicate Email
|
Password Hashing
|
Save User
|
Account Created

```

Purpose:

- Create user account
- Validate user information
- Store encrypted password


---

## Login Flow

```

User
|
Email + Password
|
Login API
|
Credential Verification
|
Generate JWT Tokens
|
Return Access and Refresh Token

```

Purpose:

- Verify user identity
- Generate authentication tokens


---

## Authentication

Authentication verifies user identity using JWT token.

Flow:

```

API Request
|
JWT Access Token
|
Token Validation
|
Authenticated User

```

---

## Authorization

Authorization controls user permissions.

Examples:

- User can access own profile
- Admin can manage users


---

# Task 2 — Registration API

## Purpose

Create API for new user registration.


## Implementation

Created:

- Serializer
- Validation
- API View
- URL Configuration


## Validations

Implemented:

- Email validation
- Duplicate email checking
- Password validation
- Required field validation


## Endpoint

```

POST /api/register/

````


## Request

```json
{
    "email": "user@gmail.com",
    "password": "StrongPassword@123"
}
````

## Response

```json
{
    "message": "User registered successfully"
}
```

## Testing Completed

Verified:

* Valid registration
* Invalid email
* Weak password
* Missing fields
* Duplicate email

---

# Task 3 — Login API

## Purpose

Authenticate users using email and password.

## Implementation

Login process:

```
Email
 |
Password Verification
 |
Authentication
 |
Generate JWT
 |
Return Tokens
```

## Endpoint

```
POST /api/login/
```

## Request

```json
{
    "email":"user@gmail.com",
    "password":"StrongPassword@123"
}
```

## Response

```json
{
    "user":{
        "email":"user@gmail.com"
    },
    "access":"jwt_access_token",
    "refresh":"jwt_refresh_token"
}
```

## Testing

Verified:

* Correct credentials
* Wrong password
* Invalid email
* Missing fields

---

# Task 4 — JWT Authentication

## Purpose

Secure APIs using JWT authentication.

## Configuration

Configured:

* JWT Authentication Class
* Access Token Validation
* Protected API Access

Example:

```python
REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES":(
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )

}
```

## Protected API

Example:

```
GET /api/profile/
```

Without Token:

```
401 Unauthorized
```

With Valid Token:

```
200 OK
```

---

# Task 5 — Change Password API

## Purpose

Allow authenticated users to securely change passwords.

## Features

### Current Password Validation

Checks existing password before update.

### New Password Validation

Uses Django password validators.

### Secure Password Update

Password stored using Django hashing mechanism.

## Endpoint

```
POST /api/change-password/
```

## Request

```json
{
    "current_password":"OldPassword@123",
    "new_password":"NewPassword@123"
}
```

## Testing

Verified:

* Correct old password
* Wrong old password
* Weak password
* Successful update

---

# Task 6 — Logout API

## Purpose

Secure logout by invalidating refresh tokens.

## Implementation

Used:

JWT Token Blacklist

Flow:

```
Logout Request
 |
Refresh Token
 |
Blacklist Token
 |
Token Cannot Be Used Again
```

## Endpoint

```
POST /api/logout/
```

## Testing

Verified:

* Logout success
* Blacklisted token rejection

---

# Task 7 — Postman Documentation

## Purpose

Create API documentation for testing and team collaboration.

## Collections Created

### Registration Collection

Endpoint:

```
POST /api/register/
```

Purpose:

Create new user account.

---

### Login Collection

Endpoint:

```
POST /api/login/
```

Purpose:

Generate JWT tokens.

---

### Password Collection

Endpoints:

```
POST /api/change-password/

POST /api/logout/
```

Purpose:

Manage user security operations.

Documentation Includes:

* Endpoint URL
* HTTP Method
* Request Body
* Headers
* Response Examples
* Error Responses

---

# Task 8 — Git & Code Review

## Purpose

Maintain clean version control and track development progress.

## Git Commit History

```bash
git init

git add .

git commit -m "Initial project setup"

git commit -m "Add registration API"

git commit -m "Add login JWT authentication"

git commit -m "Configure JWT authentication"

git commit -m "Add change password API"

git commit -m "Add logout token blacklist"

git commit -m "Add swagger documentation"

git commit -m "Update authentication documentation"
```

---

# Code Review Checklist

Verified:

* Code formatting
* Serializer validations
* API responses
* Password security
* JWT configuration
* Authentication classes
* Error handling
* API documentation

---

# API Documentation

Swagger Documentation:

```
GET /api/schema/
```

Swagger UI:

```
GET /api/docs/
```

Swagger provides:

* API endpoint details
* Request structure
* Response examples
* JWT authorization testing

---

# API Endpoints

| Endpoint              | Method | Purpose                   |
| --------------------- | ------ | ------------------------- |
| /api/register/        | POST   | Create user account       |
| /api/login/           | POST   | Login and generate tokens |
| /api/profile/         | GET    | View profile              |
| /api/profile/         | POST   | Update profile            |
| /api/change-password/ | POST   | Change password           |
| /api/logout/          | POST   | Logout user               |
| /api/profiles/        | GET    | List profiles             |

---

# Running Project Locally

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Migration

```bash
python manage.py makemigrations

python manage.py migrate
```

---

## Run Server

```bash
python manage.py runserver
```

Server:

```
http://127.0.0.1:8000/
```

---

# Final Deliverables

Completed:

* Registration API
* Login API
* JWT Authentication
* Access Token
* Refresh Token
* Protected APIs
* Change Password API
* Logout API
* Token Blacklist
* Swagger Documentation
* Postman Collections
* API Testing
* Git Commit History
* Authentication Documentation

---

# Final Authentication Flow

```
User Registration

        |
        v

Create User Account

        |
        v

Login Using Email

        |
        v

Generate JWT Tokens

        |
        v

Access Protected APIs

        |
        v

Password Management

        |
        v

Logout

        |
        v

Blacklist Refresh Token

        |
        v

Secure Session Termination
```

---

# Conclusion

The Authentication Module was successfully developed using Django REST Framework and JWT authentication.

The system provides:

* Secure user registration
* Email based authentication
* JWT authorization
* Token management
* Password security
* Logout functionality
* API documentation
* Testing workflow
* Git based version control
