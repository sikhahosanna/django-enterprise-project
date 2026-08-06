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
# Authentication Module Development

## Epic

**Authentication Module Development**

---

# Objective

The objective of this module is to develop a complete authentication system for a mobile application using JWT (JSON Web Token) authentication.

The module provides secure user management functionality including:

- User Registration
- Email-based Login
- JWT Authentication
- Access and Refresh Token Management
- Protected APIs
- Change Password
- Logout with Token Blacklisting
- API Documentation
- Testing and Version Control


---

# Technology Stack

| Technology | Purpose |
|---|---|
| Django 6.x | Backend Framework |
| Django REST Framework | API Development |
| PostgreSQL | Database Management |
| Simple JWT | JWT Authentication |
| drf-spectacular | API Documentation |
| Postman | API Testing |
| Git | Version Control |


---

# Project Structure
myproject/

│
├── accounts/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│
├── core/
│
├── common/
│
├── myproject/
│ ├── settings.py
│ ├── urls.py
│
├── media/
│
├── manage.py
└── requirements.txt



---

# Task 1 — Study Authentication Flow

## Purpose

To understand the complete authentication lifecycle and security flow used in modern applications.


---

## Concepts Studied


## Registration

Registration allows a new user to create an account.

Flow:


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
Hash Password
|
Save User
|
Account Created



Purpose:

- Create new user account
- Validate user information
- Store encrypted password


---

## Login

Login verifies existing user credentials.


Flow:


User
|
Email + Password
|
Login API
|
Authentication Check
|
Generate JWT Tokens
|
Return Tokens



Purpose:

- Verify user identity
- Generate authentication tokens


---

## Authentication

Authentication identifies the user making an API request.


Flow:


Request
|
JWT Access Token
|
Token Verification
|
User Authentication



Purpose:

Allow only valid users to access protected resources.


---

## Authorization

Authorization controls user permissions after authentication.


Example:

- User can access own profile
- Unauthorized users cannot access protected APIs


---

## JWT (JSON Web Token)

JWT is a token-based authentication mechanism.


JWT contains:

- User identity
- Token expiry
- Signature


Types:


### Access Token

Purpose:

- Used for accessing APIs
- Short expiry duration


Example:


Authorization: Bearer access_token



### Refresh Token

Purpose:

- Generate new access tokens
- Maintain user session


---

# Task 2 — Registration API


## Purpose

Create API for new user account registration.


---

## Implementation


### Serializer Created

Purpose:

- Validate incoming request data
- Validate email
- Validate password
- Create user object


Implemented:

- Duplicate email validation
- Password validation using Django validators


---

### API View Created

Purpose:

Handle registration request.


Responsibilities:

- Receive user details
- Validate serializer
- Create user
- Return response


---

### Endpoint



POST /api/register/



Request:


```json
{
"email":"test@gmail.com",
"password":"Password@123"
}

Response:

{
"message":"Registration successful"
}
Testing Completed

Verified:

✅ Valid registration

✅ Invalid email

✅ Weak password

✅ Missing fields

✅ Duplicate email

Task 3 — Login API
Purpose

Authenticate users using email and password.

Implementation

Created login API using:

Email authentication
Password verification
JWT token generation

Generated:

Access Token

Used for API authentication.

Refresh Token

Used for token renewal.

Endpoint:

POST /api/login/

Request:

{
"email":"test@gmail.com",
"password":"Password@123"
}

Response:

{
"user":{
"email":"test@gmail.com"
},

"access":"JWT_ACCESS_TOKEN",

"refresh":"JWT_REFRESH_TOKEN"
}
Testing Completed

Verified:

✅ Valid login

✅ Invalid password

✅ Invalid email

✅ Missing fields

Task 4 — JWT Authentication
Purpose

Secure APIs using JWT authentication.

Configuration Completed

Added:

JWT Authentication class
Simple JWT configuration
Protected API access

settings.py:

REST_FRAMEWORK = {

"DEFAULT_AUTHENTICATION_CLASSES":(
"rest_framework_simplejwt.authentication.JWTAuthentication",
)

}
Protected APIs

Example:

GET /api/profile/

Without Token:

401 Unauthorized

With Valid Token:

200 OK
Verification Completed

Checked:

✅ Unauthorized access blocked

✅ Valid token access allowed

Task 5 — Change Password API
Purpose

Allow authenticated users to securely update passwords.

Features Implemented
Current Password Validation

System verifies old password before updating.

New Password Validation

Applied Django password validators.

Validation:

Minimum length
Common password check
Numeric password check
Secure Password Update

Password stored using Django password hashing.

Endpoint:

POST /api/change-password/

Request:

{
"current_password":"OldPassword@123",

"new_password":"NewPassword@123"
}
Testing Completed

Verified:

✅ Correct current password

✅ Wrong current password

✅ Password validation

✅ Successful password update

Task 6 — Logout API
Purpose

Securely logout users by invalidating refresh tokens.

Implementation

Used:

JWT Token Blacklist

Flow:

Logout Request

      |

Refresh Token

      |

Blacklist Token

      |

Token Invalid

Endpoint:

POST /api/logout/
Testing Completed

Verified:

✅ Logout success

✅ Blacklisted token rejection

Task 7 — Swagger Documentation
Purpose

Generate interactive API documentation and verify all endpoints.

Implementation

Installed:

drf-spectacular

Added:

drf_spectacular

in INSTALLED_APPS.

Configured:

"DEFAULT_SCHEMA_CLASS":
"drf_spectacular.openapi.AutoSchema"
Swagger URLs

Schema:

GET /api/schema/

Swagger UI:

GET /api/docs/
Documented APIs

Available endpoints:

POST /api/register/

POST /api/login/

GET /api/profile/

POST /api/profile/

POST /api/change-password/

POST /api/logout/

GET /api/profiles/
Verification Completed

Checked:

✅ All endpoints visible

✅ Request methods displayed

✅ Response schemas generated

✅ Swagger UI working

Task 8 — Testing & Git
Purpose

Verify complete functionality and maintain proper version control.

API Testing

Tested APIs:

Registration API

Checked:

Success response
Validation errors
Duplicate email
Login API

Checked:

Valid credentials
Invalid credentials
JWT generation
Profile API

Checked:

Authentication required
User profile access
Change Password API

Checked:

Old password verification
Password update
Logout API

Checked:

Token blacklist
Logout behaviour
Git Implementation
Repository Setup

Commands:

git init

git add .

git commit -m "Initial project setup"

git commit -m "Add registration API"

git commit -m "Add login JWT authentication"

git commit -m "Add change password API"

git commit -m "Add logout token blacklist"

git commit -m "Add swagger documentation"

git commit -m "Update README documentation"
Code Review Completed

Verified:

✅ Clean project structure

✅ Serializer validations

✅ Secure password handling

✅ JWT implementation

✅ API security

✅ Swagger documentation

✅ Error handling

End of Day Deliverables

Completed:

✅ Registration API

✅ Login API

✅ JWT Authentication

✅ Access Token

✅ Refresh Token

✅ Protected APIs

✅ Change Password API

✅ Logout API

✅ JWT Token Blacklist

✅ Swagger Documentation

✅ API Testing

✅ Git Commits

✅ README Documentation

Final Authentication Flow
User Registration

        |

        v

User Account Created

        |

        v

User Login

        |

        v

JWT Access + Refresh Token

        |

        v

Access Protected APIs

        |

        v

Password Management

        |

        v

Logout & Token Blacklist
Conclusion

The Authentication Module was successfully developed with complete JWT-based security implementation.

The system supports secure registration, authentication, authorization, password management, logout functionality, API documentation, testing, and version control following professional backend development practices.