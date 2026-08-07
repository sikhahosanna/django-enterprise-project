

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

TASK-4


# Security & Performance Enhancement Tasks

## Objective

Secure the application and improve API performance using enterprise best practices.

The implementation focused on:

- Role-Based Access Control (RBAC)
- API security
- Soft delete functionality
- Audit tracking
- Centralized logging
- Exception handling
- ORM optimization
- Final testing and documentation

---

# Task 1 – RBAC (Role-Based Access Control)

## Overview

RBAC is a security approach where access to application resources is controlled based on user roles.

## Concepts Studied

### Roles

Roles define the type of user and their access level.

Implemented roles:

- Admin
- User


### Permissions

Permissions define what actions a role can perform.

Examples:

- Admin can view all profiles.
- User can access and update their own profile.


### Authorization

Authorization verifies whether a user has permission to perform a specific action.

Implemented using Django REST Framework custom permissions.

---

# Task 2 – Role Implementation

## Implemented Roles

### Admin Role

Admin users can:

- View all user profiles.
- Access protected admin APIs.
- Manage application data.


### User Role

Normal users can:

- View their own profile.
- Update their own profile.
- Access authorized resources only.


## Verification

Access rules were tested using:

- Admin JWT token
- Normal user JWT token
- Anonymous requests


---

# Task 3 – API Security

## Implementation

Protected APIs using custom permission classes.

Implemented:

- JWT Authentication
- IsAuthenticated permission
- Custom Admin/Owner permission


## Security Verification

### Anonymous User

Result:

```

Authentication credentials were not provided.

```

### Unauthorized User

Result:

```

You do not have permission to perform this action.

```

### Authorized User

Successfully accessed allowed resources.

---

# Task 4 – Soft Delete Implementation

## Implementation

Added:

```

is_deleted

```

field to Profile model.


## Functionality

### Delete

Instead of permanently deleting records:

```

is_deleted = True

```

is updated.


### Restore

Deleted records can be restored:

```

is_deleted = False

````


### Active Records Filtering

Only active records are displayed:

```python
Profile.objects.filter(
    is_deleted=False
)
````

## Verification

Tested:

* Delete profile
* Restore profile
* Active record filtering

---

# Task 5 – Audit Fields

## Added Fields

Implemented tracking fields:

```python
created_at
updated_at
created_by
updated_by
```

## Purpose

Audit fields help track:

* When a record was created.
* When a record was modified.
* Which user created the record.
* Which user updated the record.

## Verification

Confirmed automatic timestamp updates during create and update operations.

---

# Task 6 – Logging & Exception Handling

## Centralized Logging

Configured Django logging system.

Log location:

```
logs/error.log
```

## Features Implemented

* Error logging
* Application error tracking
* Custom exception responses
* API error handling

## Verification

Generated errors and verified logs were stored successfully.

---

# Task 7 – ORM Performance Optimization

## Objective

Improve database performance by reducing unnecessary queries.

## Implemented Optimization

### select_related()

Used for ForeignKey and OneToOne relationships.

Example:

```python
Profile.objects.select_related(
    "user"
).filter(
    is_deleted=False
)
```

### prefetch_related()

Used for handling multiple related objects efficiently.

## Query Optimization Result

Before optimization:

```
Multiple database queries executed
```

After optimization:

```
Single optimized query executed
```

## Verification

Used Django query count:

```python
len(connection.queries)
```

Confirmed reduced database queries.

---

# Task 8 – Final Testing & Documentation

## API Testing

All APIs tested end-to-end using Postman.

Tested:

* Registration API
* Login API
* JWT authentication
* Profile CRUD APIs
* Image upload
* Password change
* Logout
* Soft delete
* Restore functionality
* Filtering
* Pagination

## Project Review

Reviewed:

* Project structure
* Database models
* API endpoints
* Permissions
* Exception handling
* Logging configuration

## Bug Fixing

Resolved:

* Authentication issues
* Permission issues
* Migration issues
* API response issues

## Git Commit

Completed work committed to Git repository.

Implemented:

* Security enhancements
* Performance optimization
* Documentation updates

---

# Final Implementation Summary

| Feature               | Status    |
| --------------------- | --------- |
| RBAC                  | Completed |
| Custom Permissions    | Completed |
| JWT Security          | Completed |
| Profile APIs          | Completed |
| Image Upload          | Completed |
| Soft Delete           | Completed |
| Restore Functionality | Completed |
| Audit Fields          | Completed |
| Logging               | Completed |
| Exception Handling    | Completed |
| ORM Optimization      | Completed |
| API Testing           | Completed |
| Documentation         | Completed |

## Blockers

```
0
```

## Project Status

Completed Successfully ✅

```
