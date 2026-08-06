# Django Enterprise Project

## Technologies Used
 Python
 Django
 Django REST Framework
 PostgreSQL

## Apps
### accounts
Custom User Model and authentication.
### core
Main project functionality.

### common
Reusable common features.

## Features Completed
 Django project setup
 PostgreSQL configuration
 Environment variables setup
 Django REST Framework installation
 Custom User Model with email login and UUID primary key
 Git repository setup

## Run Project

Activate virtual environment:

venv\Scripts\activate

Run migrations:

python manage.py migrate

Start server:

python manage.py runserver

TASK-2 (DAY 2)

# Authentication Module Development

## Epic

**Authentication Module Development**

---

# Objective

The objective of this module is to develop a complete and secure authentication system for a mobile application using **JWT (JSON Web Token) authentication**.

This module provides:

- User registration
- Email-based login
- JWT access and refresh token generation
- Protected API authentication
- Password change functionality
- Secure logout with token blacklist
- API documentation and testing

The authentication system follows industry-standard security practices to ensure user identity verification and authorization.

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Django | Backend framework |
| Django REST Framework | API development |
| PostgreSQL | Database |
| JWT | Authentication mechanism |
| Simple JWT | Token generation and validation |
| Postman | API testing and documentation |
| Git | Version control |


---

# Task 1 — Study Authentication Flow

## Purpose

Understand the complete lifecycle of user authentication and how users are verified and authorized in a secure application.

---

## Authentication Concepts

### 1. Registration

Registration is the process where a new user creates an account in the application.

During registration:

- User provides email and password
- Email uniqueness is verified
- Password strength is validated
- Password is securely hashed
- User record is stored in database


Flow:
User
|
| Enter Email + Password
|
API Request
|
Serializer Validation
|
Check Duplicate Email
|
Hash Password
|
Save User
|
Registration Success


---

### 2. Login

Login verifies the identity of an existing user.

Process:
User
|
| Email + Password
|
Login API
|
Validate Credentials
|
Generate JWT Tokens
|
Return Access + Refresh Token


---

### 3. Authentication

Authentication verifies who the user is.

Example:
Request
|
JWT Token
|
Token Verification
|
User Identity Confirmed

---

### 4. Authorization

Authorization decides what actions an authenticated user can perform.

Example:

- User can view own profile
- Admin can manage users


---

### 5. JWT (JSON Web Token)

JWT is a token-based authentication system.

JWT contains:

- User identity
- Token expiry time
- Signature for verification


JWT Types:

### Access Token

Purpose:

- Used for accessing protected APIs
- Short expiration time
- Sent with every request


Example:
Authorization: Bearer <access_token>


### Refresh Token

Purpose:

- Generate a new access token
- Long expiration time
- Used when access token expires


---

# Task 2 — Registration API

## Purpose

Create a secure API that allows new users to register into the application.


## Components Created

### Serializer

Purpose:

- Validate incoming data
- Check required fields
- Validate password rules
- Convert data into User object


Implemented validations:

- Email format validation
- Duplicate email checking
- Password strength validation


---

### Password Validation

Purpose:

Ensure users create strong passwords.

Validation includes:

- Minimum password length
- Common password rejection
- Numeric-only password rejection


---

### API View

Purpose:

Handle registration requests.

Responsibilities:

- Receive user data
- Validate serializer
- Create user
- Return response


---

### URL

Endpoint:
POST /api/register/



Request:

```json
{
    "email":"user@gmail.com",
    "password":"StrongPassword@123"
}

Response:

{
    "message":"User registered successfully"
}
Testing Completed
Valid Request

Result:

User created successfully
Invalid Request

Checked:

Invalid email
Weak password
Missing fields
Duplicate Email

Result:

Email already exists
Task 3 — Login API
Purpose

Authenticate registered users and generate JWT tokens.

Implementation

Login is performed using email and password.

Process:

Email
 |
Password Verification
 |
Authentication
 |
Generate JWT
 |
Return Tokens
Generated Tokens
Access Token

Used for API access.

Refresh Token

Used for generating new access tokens.

Endpoint:

POST /api/login/

Request:

{
 "email":"user@gmail.com",
 "password":"StrongPassword@123"
}

Response:

{
"user":{
    "email":"user@gmail.com"
},

"access":"jwt_access_token",

"refresh":"jwt_refresh_token"
}
Testing

Verified:

Correct credentials
Wrong password
Invalid email
Missing fields
Task 4 — JWT Authentication
Purpose

Secure APIs by allowing only authenticated users.

Configuration

Configured:

JWT Authentication class
Access token validation
Protected endpoints

settings.py:

REST_FRAMEWORK = {

"DEFAULT_AUTHENTICATION_CLASSES":(
"rest_framework_simplejwt.authentication.JWTAuthentication",
)

}
Protected APIs

Example:

GET /api/profile/

Without token:

Response:

401 Unauthorized

With valid JWT:

Response:

200 Success
Task 5 — Change Password API
Purpose

Allow authenticated users to securely change their password.

Features Implemented
Current Password Validation

System verifies existing password before update.

New Password Validation

New password follows Django password rules.

Secure Password Update

Password is updated using Django hashing mechanism.

Endpoint:

POST /api/change-password/

Request:

{
"current_password":"OldPassword@123",

"new_password":"NewPassword@123"
}

Testing:

Verified:

Correct old password
Incorrect old password
Weak new password
Successful update
Task 6 — Logout API
Purpose

Securely logout users by invalidating refresh tokens.

Implementation

Used:

JWT Token Blacklist

Process:

User Logout
 |
Refresh Token
 |
Blacklist Token
 |
Token Cannot Be Used Again

Endpoint:

POST /api/logout/

Testing:

Verified:

Logout success
Blacklisted token rejection
Task 7 — Postman Documentation
Purpose

Create API documentation for easy testing and team collaboration.

Collections Created
Registration Collection

Contains:

POST /api/register/

Purpose:

Test user creation.

Login Collection

Contains:

POST /api/login/

Purpose:

Generate JWT tokens.

Password Collection

Contains:

POST /api/change-password/

POST /api/logout/

Purpose:

Manage user security operations.

Documentation Includes

Each API contains:

Endpoint URL
HTTP method
Request body
Headers
Response example
Error responses
Task 8 — Git & Code Review
Purpose

Maintain clean version control and track development progress.

Git Commit Strategy

Each feature committed separately:

Example:

git commit -m "Add registration API"

git commit -m "Add login JWT authentication"

git commit -m "Add password change API"

git commit -m "Add logout token blacklist"

git commit -m "Add authentication documentation"
Code Review Checklist

Verified:

Code formatting
Serializer validations
API responses
Security practices
JWT configuration
Error handling
Documentation
End of Day Deliverables

Completed:

✅ Registration API

✅ Login API

✅ JWT Authentication

✅ Access Token Generation

✅ Refresh Token Generation

✅ Protected APIs

✅ Change Password API

✅ Logout API

✅ Token Blacklist

✅ Postman Collections

✅ Authentication Documentation

✅ Git Commit History

Final Authentication Flow
User Registration

        |
        v

Database User Creation

        |
        v

Login

        |
        v

JWT Access + Refresh Token

        |
        v

Access Protected APIs

        |
        v

Change Password / Logout

        |
        v

Secure User Session Management
Conclusion

The Authentication Module provides a complete JWT-based security layer for the mobile application.

The implementation supports secure user onboarding, authentication, authorization, password management, and session termination following modern backend development standards.

TASK-3 (DAY 3)
# Running the Project Locally

## 1. Clone Repository

```bash
git clone <repository-url>

cd myproject
2. Create Virtual Environment
python -m venv venv

Activate environment:

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
Environment Configuration

Create .env file in project root.

Example:

SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

Purpose:

Environment variables keep sensitive information secure and avoid hardcoding secrets inside settings.py.

Database Setup

This project uses PostgreSQL.

Create database:

CREATE DATABASE mydb;

Run migrations:

python manage.py makemigrations

python manage.py migrate

Create admin user:

python manage.py createsuperuser
Start Development Server

Run:

python manage.py runserver

Server:

http://127.0.0.1:8000/
API Documentation

Swagger documentation is available using drf-spectacular.

OpenAPI Schema
GET /api/schema/
Swagger UI
GET /api/docs/

Swagger provides:

API endpoint details
Request body structure
Response examples
Authentication testing
JWT authorization support
API Endpoints
Authentication APIs
API	Method	Purpose
/api/register/	POST	Create new user account
/api/login/	POST	Login and generate JWT tokens
/api/profile/	GET	Get authenticated user profile
/api/profile/	POST	Update user profile
/api/change-password/	POST	Change password securely
/api/logout/	POST	Logout and blacklist token
/api/profiles/	GET	List user profiles
JWT Authentication Usage

After successful login:

Response:

{
 "access":"access_token",
 "refresh":"refresh_token"
}

Use access token for protected APIs:

Header:

Authorization: Bearer <access_token>

Example:

GET /api/profile/

Without token:

401 Unauthorized

With valid token:

200 OK
Postman Testing

Created Postman collections for:

Registration Collection

Test cases:

Valid registration
Invalid email
Missing fields
Duplicate email
Login Collection

Test cases:

Valid credentials
Wrong password
Invalid email
Token generation
Password Collection

Test cases:

Correct old password
Wrong old password
Password validation
Successful update
Logout Collection

Test cases:

Valid refresh token
Blacklisted token validation
Testing Summary

All APIs verified successfully:

Registration API

Checked:

✅ User creation
✅ Email validation
✅ Password validation
✅ Duplicate email handling

Login API

Checked:

✅ Email authentication
✅ JWT access token
✅ JWT refresh token

Protected APIs

Checked:

✅ Unauthorized access blocked
✅ Authorized access allowed

Change Password API

Checked:

✅ Current password verification
✅ Secure password update

Logout API

Checked:

✅ Refresh token blacklist
✅ Session termination

Git Commit History

Feature-wise commits:

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

Purpose:

Maintain clean development history
Track feature implementation
Easy rollback and review
Code Review Checklist

Verified:

✅ Django project structure
✅ Serializer validations
✅ Password security
✅ JWT configuration
✅ Authentication classes
✅ Protected APIs
✅ Token blacklist implementation
✅ API documentation
✅ Error handling
✅ Git history

Final Deliverables

Completed:

✅ Registration API

✅ Login API

✅ JWT Authentication

✅ Access Token Generation

✅ Refresh Token Generation

✅ Protected APIs

✅ Change Password API

✅ Logout API

✅ Token Blacklist

✅ Swagger Documentation

✅ Postman Collections

✅ API Testing

✅ Git Commit History

✅ Authentication Documentation

Final Authentication Architecture
User Registration

        |
        v

Create User Account

        |
        v

Login Using Email

        |
        v

Generate JWT Access + Refresh Token

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
Conclusion

The Authentication Module was successfully developed using Django REST Framework and JWT authentication.

The implementation provides a secure authentication layer with:

User registration
Email based login
JWT authorization
Token management
Password security
Logout functionality
API documentation
Testing workflow
Git based version control

The module follows professional backend development practices and is ready for mobile application integration.