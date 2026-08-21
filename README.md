

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
# Ride Booking Backend – Database & Business Module Documentation

## 1. Business Domain

**Domain:** Ride Booking

The application allows users to book rides, drivers to accept rides, and vehicles to be associated with drivers.

### Main Business Entities

* User
* Profile
* DriverProfile
* VehicleType
* Vehicle
* RideStatus
* Ride

---

# 2. ER Diagram

```text
                         ┌─────────────────┐
                         │      User       │
                         │─────────────────│
                         │ PK: id (UUID)   │
                         │ email           │
                         └────────┬────────┘
                                  │
                       1          │          1
                                  │
                 ┌────────────────┴──────────────┐
                 │                               │
                 ▼                               ▼
       ┌─────────────────┐             ┌──────────────────┐
       │     Profile     │             │  DriverProfile   │
       │─────────────────│             │──────────────────│
       │ PK: user_id     │             │ PK: id (UUID)    │
       │ first_name      │             │ FK: user_id      │
       │ last_name       │             │ license_number   │
       │ phone           │             │ status           │
       └─────────────────┘             └────────┬─────────┘
                                                │
                                                │ 1
                                                │
                                                │ N
                                                ▼
                                      ┌──────────────────┐
                                      │     Vehicle      │
                                      │──────────────────│
                                      │ PK: id (UUID)    │
                                      │ FK: driver_id    │
                                      │ FK: vehicle_type │
                                      │ registration_no  │
                                      │ model            │
                                      └────────┬─────────┘
                                               │
                                               │ N
                                               │
                                               │ 1
                                               ▼
                                      ┌──────────────────┐
                                      │   VehicleType    │
                                      │──────────────────│
                                      │ PK: id (UUID)    │
                                      │ name             │
                                      └──────────────────┘


                         ┌─────────────────┐
                         │      User       │
                         └────────┬────────┘
                                  │
                                  │ 1
                                  │
                                  │ N
                                  ▼
                         ┌─────────────────┐
                         │      Ride       │
                         │─────────────────│
                         │ PK: id (UUID)   │
                         │ FK: rider_id    │
                         │ FK: driver_id   │
                         │ FK: status_id   │
                         │ pickup location │
                         │ dropoff location│
                         │ fare            │
                         └──────┬──────┬───┘
                                │      │
                                │      │
                         N      │      │ N
                                │      │
                                ▼      ▼
                     DriverProfile   RideStatus
```

---

# 3. Models

## User

Represents a registered application user.

Important fields:

* `id` – UUID primary key
* `email` – unique email address
* Authentication fields from Django `AbstractUser`

---

## Profile

Stores additional information about a user.

Important fields:

* `user` – One-to-One relationship with User
* `first_name`
* `last_name`
* `phone`
* `profile_image`
* `is_deleted`

---

## DriverProfile

Represents a user who works as a driver.

Important fields:

* `id` – UUID primary key
* `user` – One-to-One relationship with User
* `license_number` – unique
* `status`
* `created_at`
* `updated_at`

Driver status choices:

* Active
* Inactive
* Suspended

---

## VehicleType

Represents the type/category of vehicle.

Supported vehicle types:

* Bike
* Auto
* Car
* SUV

Important fields:

* `id` – UUID primary key
* `name` – unique vehicle type
* `created_at`
* `updated_at`

---

## Vehicle

Represents a vehicle owned/assigned to a driver.

Important fields:

* `id` – UUID primary key
* `driver` – Foreign Key to DriverProfile
* `vehicle_type` – Foreign Key to VehicleType
* `registration_number` – unique
* `model`
* `created_at`
* `updated_at`

---

## RideStatus

Represents the current status of a ride.

Available statuses:

* Requested
* Accepted
* Started
* Completed
* Cancelled

Important fields:

* `id` – UUID primary key
* `name` – unique
* `created_at`
* `updated_at`

---

## Ride

Represents a ride booking.

Important fields:

* `id` – UUID primary key
* `rider` – Foreign Key to User
* `driver` – optional Foreign Key to DriverProfile
* `status` – Foreign Key to RideStatus
* `pickup_address`
* `pickup_latitude`
* `pickup_longitude`
* `dropoff_address`
* `dropoff_latitude`
* `dropoff_longitude`
* `fare`
* `created_at`
* `updated_at`

---

# 4. Relationships

### One-to-One Relationships

**User → Profile**

One user has one profile.

```text
User 1 ───── 1 Profile
```

**User → DriverProfile**

A user can have one driver profile.

```text
User 1 ───── 1 DriverProfile
```

---

### One-to-Many Relationships

**DriverProfile → Vehicle**

One driver can have multiple vehicles.

```text
DriverProfile 1 ───── N Vehicle
```

**VehicleType → Vehicle**

One vehicle type can be used by multiple vehicles.

```text
VehicleType 1 ───── N Vehicle
```

**User → Ride**

One user can create multiple rides.

```text
User 1 ───── N Ride
```

**DriverProfile → Ride**

One driver can have multiple rides.

```text
DriverProfile 1 ───── N Ride
```

**RideStatus → Ride**

One status can be associated with multiple rides.

```text
RideStatus 1 ───── N Ride
```

---

### Many-to-Many Relationships

No direct Many-to-Many relationship is required in the current database design.

The required relationships can be represented using Foreign Keys.

---

# 5. Business Rules

1. Each user must have a unique email address.

2. A user can have only one profile.

3. A user can have only one driver profile.

4. Each driver must have a unique driving license number.

5. A driver can have multiple vehicles.

6. Every vehicle must belong to a valid driver.

7. Every vehicle must have a valid vehicle type.

8. Vehicle registration numbers must be unique.

9. A ride must have a rider.

10. A ride may initially have no driver because a driver can be assigned later.

11. Every ride must have a valid ride status.

12. Ride fare cannot be negative.

13. Driver status must use one of the predefined choices.

14. Vehicle type must use one of the predefined choices.

15. Ride status must use one of the predefined statuses.

---

# 6. Database Constraints

## Primary Keys

UUID primary keys are used for the main business models.

```text
User
Profile
DriverProfile
VehicleType
Vehicle
RideStatus
Ride
```

UUIDs provide unique identifiers for records.

---

## Unique Constraints

The following fields are unique:

```text
User.email
DriverProfile.license_number
VehicleType.name
Vehicle.registration_number
RideStatus.name
```

This prevents duplicate values.

---

## NOT NULL Constraints

Required fields are not nullable by default.

Examples:

```text
User.email
DriverProfile.license_number
Vehicle.registration_number
Vehicle.model
Ride.rider
Ride.status
Ride.pickup_address
Ride.dropoff_address
Ride.fare
```

The `Ride.driver` field is nullable because a driver may be assigned after the ride is requested.

---

## Choices

### Driver Status

```text
active
inactive
suspended
```

### Vehicle Type

```text
bike
auto
car
suv
```

### Ride Status

```text
requested
accepted
started
completed
cancelled
```

---

## Database Indexes

Indexes are created for frequently queried fields.

Examples:

```text
DriverProfile.status
Vehicle.driver
Vehicle.vehicle_type
VehicleType.name
RideStatus.name
Ride.rider
Ride.driver
Ride.status
Ride.created_at
```

Indexes improve query performance when filtering or searching these fields.

---

## Check Constraint

The Ride model contains a database-level check constraint:

```text
fare >= 0
```

This prevents negative ride fares from being stored in the database.

Constraint name:

```text
ride_fare_non_negative
```

---

# 7. Timestamp Management

Business models use:

```text
created_at
updated_at
```

`created_at` records when the record was created.

`updated_at` records when the record was last updated.

---

# 8. Database Migration Verification

Django migrations were created and applied successfully.

Migration verification was performed using:

```bash
python manage.py showmigrations accounts
```

All migrations were successfully applied.

PostgreSQL database tables were also verified using:

```sql
\dt
```

The following business tables were confirmed:

```text
accounts_user
accounts_profile
accounts_driverprofile
accounts_vehicletype
accounts_vehicle
accounts_ridestatus
accounts_ride
```

---

# 9. Django Admin

The following models were registered in Django Admin:

* User
* Profile
* DriverProfile
* VehicleType
* Vehicle
* RideStatus
* Ride

Admin configuration includes:

* List display
* Search
* Filters
* Ordering

---

# 10. Conclusion

The Ride Booking business module database has been designed using Django ORM and PostgreSQL.

The implementation includes:

* UUID primary keys
* Foreign Key relationships
* One-to-One relationships
* One-to-Many relationships
* Unique constraints
* Check constraints
* Choices
* Database indexes
* Timestamps
* Django Admin configuration
* PostgreSQL migration verification

The database structure provides a foundation for implementing the REST API and business logic layer of the Ride Booking mobile application backend.
  

  11/8/26
   # Django Driver & Vehicle Management API

A Django REST Framework based backend API for managing users, profiles, drivers, and vehicles with JWT authentication, role-based permissions, validation, filtering, searching, ordering, and pagination.

## Features

### Authentication

* User registration
* User login
* JWT access and refresh tokens
* Password change
* Logout with refresh-token blacklisting

### Profile Management

* Create and update profile
* View own profile
* Profile image upload
* Soft delete profile
* Restore deleted profile
* Admin profile listing

### Driver Management

* Admin can create drivers
* Admin can list all drivers
* Admin and driver owner can view driver details
* Driver owner can update own driver details
* Driver status management
* Driver search
* Active/inactive filtering

### Vehicle Management

* Create vehicles
* List vehicles
* View vehicle details
* Update vehicles
* Delete vehicles
* Driver-based vehicle access
* Vehicle type filtering
* Registration number validation
* Duplicate registration number prevention

### Filtering, Searching & Pagination

* Driver search
* Driver status filtering
* Vehicle type filtering
* Pagination
* Ordering

### API Error Handling

The API handles:

* Driver not found
* Vehicle not found
* Duplicate registration number
* Authentication errors
* Permission errors
* Invalid request data
* Missing required fields
* Invalid vehicle type
* Invalid driver ID

## Technology Stack

* Python
* Django
* Django REST Framework
* Django REST Framework Simple JWT
* django-filter
* SQLite / PostgreSQL
* Postman
* drf-spectacular / Swagger

## Project Structure

```text
myproject/
│
├── accounts/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── admin.py
│
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the project

```bash
cd myproject
```

### 3. Create virtual environment

```bash
python -m venv venv
```

### 4. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create admin user

```bash
python manage.py createsuperuser
```

### 8. Run development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## API Endpoints

### Authentication

| Method | Endpoint                | Description     |
| ------ | ----------------------- | --------------- |
| POST   | `/api/register/`        | Register user   |
| POST   | `/api/login/`           | Login           |
| POST   | `/api/change-password/` | Change password |
| POST   | `/api/logout/`          | Logout          |

### Profile

| Method   | Endpoint                | Description                    |
| -------- | ----------------------- | ------------------------------ |
| GET/POST | `/api/profile/`         | View/Create/Update own profile |
| GET      | `/api/profiles/`        | Admin profile list             |
| DELETE   | `/api/profile/delete/`  | Soft delete profile            |
| POST     | `/api/profile/restore/` | Restore profile                |

### Drivers

| Method    | Endpoint               | Description    |
| --------- | ---------------------- | -------------- |
| GET       | `/api/drivers/`        | List drivers   |
| POST      | `/api/drivers/`        | Create driver  |
| GET       | `/api/drivers/<uuid>/` | Driver details |
| PUT/PATCH | `/api/drivers/<uuid>/` | Update driver  |

### Vehicles

| Method    | Endpoint                | Description     |
| --------- | ----------------------- | --------------- |
| GET       | `/api/vehicles/`        | List vehicles   |
| POST      | `/api/vehicles/`        | Create vehicle  |
| GET       | `/api/vehicles/<uuid>/` | Vehicle details |
| PUT/PATCH | `/api/vehicles/<uuid>/` | Update vehicle  |
| DELETE    | `/api/vehicles/<uuid>/` | Delete vehicle  |

## Authentication

The API uses JWT authentication.

After login, the API returns:

```json
{
    "user": {
        "id": "user-id",
        "email": "user@example.com"
    },
    "refresh": "refresh-token",
    "access": "access-token"
}
```

Use the access token in Postman:

```text
Authorization: Bearer <access-token>
```

## Permissions

### Admin

Admin users can:

* Manage drivers
* View all drivers
* Manage all vehicles
* View all profiles
* Access administrative APIs

### Driver

Drivers can:

* View their own driver details
* Update their own driver details
* View their own vehicles
* Create vehicles for themselves
* Update their own vehicles
* Delete their own vehicles

Users cannot access protected APIs without authentication.

## Filtering

### Driver status

```text
GET /api/drivers/?status=active
```

```text
GET /api/drivers/?status=inactive
```

### Driver search

```text
GET /api/drivers/?search=DL123456
```

### Vehicle type

```text
GET /api/vehicles/?vehicle_type=<vehicle-type-id>
```

## Ordering

Example:

```text
GET /api/drivers/?ordering=created_at
```

Descending order:

```text
GET /api/drivers/?ordering=-created_at
```

## Pagination

The API supports pagination.

Example:

```text
GET /api/drivers/?page=1
```

Example response:

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": []
}
```

## Validation

### Registration Number

Vehicle registration numbers are validated before creation.

Example:

```text
TS09CD1234
```

Duplicate registration numbers are rejected.

Example error:

```json
{
    "success": false,
    "error": {
        "registration_number": [
            "vehicle with this registration number already exists."
        ]
    }
}
```

### Required Fields

Missing required fields return validation errors.

Example:

```json
{
    "success": false,
    "error": {
        "vehicle_type": [
            "This field is required."
        ],
        "registration_number": [
            "This field is required."
        ],
        "model": [
            "This field is required."
        ]
    }
}
```

## Error Handling

### Authentication Error

```json
{
    "success": false,
    "error": {
        "detail": "Authentication credentials were not provided."
    }
}
```

### Driver Not Found

```json
{
    "success": false,
    "error": {
        "detail": "No DriverProfile matches the given query."
    }
}
```

### Vehicle Not Found

```json
{
    "success": false,
    "error": {
        "detail": "No Vehicle matches the given query."
    }
}
```

## API Documentation

Swagger documentation is available at:

```text
/api/docs/
```

OpenAPI schema:

```text
/api/schema/
```

## Postman Testing

The API was tested using Postman for:

### Positive Tests

* Successful registration
* Successful login
* Successful profile creation/update
* Successful driver creation
* Successful driver retrieval
* Successful vehicle creation
* Successful vehicle retrieval
* Successful vehicle update
* Successful vehicle deletion
* Filtering
* Searching
* Ordering
* Pagination

### Negative Tests

* Invalid login credentials
* Missing authentication token
* Unauthorized access
* Driver not found
* Vehicle not found
* Duplicate registration number
* Invalid driver ID
* Invalid vehicle type
* Missing required fields
* Invalid request data

### Permission Tests

* Admin access
* Driver owner access
* Unauthorized user access
* Driver accessing another driver's resources

## Running Tests

Run Django checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

## Git

The project is maintained using Git for version control.

```bash
git status
git add .
git commit -m "Complete driver and vehicle management APIs"
git push
```

## Author

Developed as a Django REST Framework backend project implementing authentication, driver management, vehicle management, permissions, validation, filtering, pagination, and API testing.

12/08/2026

Sure. **README lo direct ga paste chesukune professional notes format** lo ila pettuko:

````markdown
# Ride Management API – Development Notes

## Project Overview

This project is a Ride Management API developed using Django REST Framework.

The application provides authentication, profile management, driver and vehicle management, ride creation, ride acceptance, ride status management, and ride cancellation.

---

## Authentication

Implemented JWT-based authentication.

### APIs

- Register
- Login
- Change Password
- Logout

JWT access tokens are used to authenticate protected APIs.

---

## Profile Management

Implemented user profile management with:

- Create Profile
- View Profile
- Update Profile
- Delete Profile
- Restore Profile
- Admin Profile Listing

Profile deletion is handled using soft delete.

---

## Driver Management

Implemented driver management with:

- Create Driver
- List Drivers
- Driver Details
- Update Driver
- Driver Status Validation

Only active drivers can accept rides.

---

## Vehicle Management

Implemented vehicle management with:

- Create Vehicle
- List Vehicles
- Vehicle Details
- Update Vehicle
- Delete Vehicle

Vehicles are associated with drivers and vehicle types.

---

# Ride Management

## Ride Creation

Customers can create rides by providing:

- Pickup address
- Pickup latitude
- Pickup longitude
- Drop-off address
- Drop-off latitude
- Drop-off longitude
- Vehicle type
- Fare

New rides are created with:

```text
requested
````

status.

---

## Ride Details

Customers can:

* View their rides
* View individual ride details
* View ride status
* View assigned driver information

Users can access only their own rides.

---

## Ride Status Management

Ride statuses are managed through the ride status API.

Main statuses:

```text
requested
accepted
driver_arriving
started
completed
cancelled
```

---

# Task 6 – Accept Ride

Implemented driver ride acceptance.

### Endpoint

```text
POST /api/rides/{id}/accept/
```

### Rules

* User must be authenticated.
* User must be registered as a driver.
* Driver must be active.
* Ride must be in `requested` status.
* Driver cannot accept another ride while having an active ride.
* Ride is assigned to the driver after successful acceptance.

### Status Transition

```text
requested → accepted
```

### Concurrency Handling

`transaction.atomic()` and `select_for_update()` are used to prevent multiple drivers from accepting the same ride simultaneously.

---

# Task 7 – Cancel Ride

Implemented ride cancellation.

### Endpoint

```text
POST /api/rides/{id}/cancel/
```

### Cancellation Rules

A ride can be cancelled only when its current status is:

```text
requested
accepted
```

Allowed transitions:

```text
requested → cancelled
accepted  → cancelled
```

Cancellation is rejected for rides that are already:

```text
started
completed
cancelled
```

The API returns `400 Bad Request` for invalid cancellation attempts.

---

# Task 8 – End-to-End Testing

The complete ride lifecycle is tested using Postman.

## Successful Lifecycle

```text
Create Ride
     ↓
requested
     ↓
Accept Ride
     ↓
accepted
     ↓
Start Ride
     ↓
started
     ↓
Complete Ride
     ↓
completed
```

## Invalid Transition Testing

Invalid status transitions are also tested.

Examples:

```text
completed → started       ❌
completed → accepted      ❌
cancelled → started       ❌
cancelled → completed     ❌
```

Invalid transitions should return:

```text
400 Bad Request
```

---

# API Testing

All APIs are tested using Postman.

### Authentication

Bearer Token authentication is used for protected endpoints.

```text
Authorization
    ↓
Bearer Token
    ↓
Access Token
```

Customer access token is used for customer operations.

Driver access token is used for driver operations such as accepting rides.

---

# Error Handling

The API handles common errors such as:

* Authentication failure
* Unauthorized access
* Invalid ride ID
* Ride not found
* Invalid ride status
* Inactive driver
* Driver already having an active ride
* Missing ride status configuration
* Invalid UUID values

Appropriate HTTP status codes are returned for different errors.

---

# Database & ORM

Django ORM is used for database operations.

`select_related()` is used for optimizing related-object queries.

`transaction.atomic()` and `select_for_update()` are used where transactional consistency and concurrency protection are required.

---

# Development Server

Run the project using:

```bash
python manage.py runserver
```

Default development server:

```text
http://127.0.0.1:8000/
```

---

# Project Status

## Completed

* JWT Authentication
* User Profile Management
* Driver Management
* Vehicle Management
* Ride Creation
* Ride Listing
* Ride Details
* Ride Status Update
* Ride Acceptance
* Ride Cancellation
* Ride Lifecycle Testing
* Invalid Transition Testing

13/08/2026



# Ride Management – Development Documentation

**Date:** August 13, 2026
**Project:** Django Enterprise Project
**Module:** `accounts`
**Feature:** Ride Management

---

## 1. Objective

Implemented and tested the complete ride management flow in the Django REST Framework application.

The implementation covers:

* Ride creation
* Fare calculation
* Ride listing
* Ride details
* Ride status management
* Ride acceptance
* Ride cancellation
* Driver/vehicle information
* Ride lifecycle validation
* Duplicate ride acceptance protection
* Invalid state transition validation
* Unit testing
* Service-layer business logic
* Database transaction handling
* Git/README documentation

---

# 2. Ride Creation

Implemented `RideCreateSerializer` for creating rides.

### File

```text
accounts/serializers.py
```

### Main responsibilities

* Validate pickup address
* Validate dropoff address
* Validate latitude
* Validate longitude
* Validate pickup/dropoff are not the same
* Check whether rider already has an active ride
* Get `requested` ride status
* Calculate fare using `FareService`
* Create the ride with the authenticated user
* Automatically assign initial status as `requested`

### Initial ride status

```text
requested
```

The client does not manually control the initial ride status.

---

# 3. Fare Calculation

Implemented a dedicated fare service.

### File

```text
accounts/services/fare_service.py
```

### Service

```python
FareService
```

The service calculates:

```text
Distance
Base Fare
Distance Fare
Time Fare
Surge
Total Fare
```

### Distance calculation

Distance is calculated using the Haversine formula.

```text
Earth radius = 6371 km
```

The service calculates distance using:

```text
pickup latitude
pickup longitude
dropoff latitude
dropoff longitude
```

---

# 4. Fare Configuration

Fare configuration is maintained in:

```text
myproject/settings.py
```

Example configuration:

```python
RIDE_FARE_CONFIG = {

    "bike": {
        "base_fare": 30,
        "per_km": 10,
        "per_minute": 2,
    },

    "auto": {
        "base_fare": 40,
        "per_km": 15,
        "per_minute": 3,
    },

    "car": {
        "base_fare": 60,
        "per_km": 20,
        "per_minute": 4,
    },

    "suv": {
        "base_fare": 80,
        "per_km": 25,
        "per_minute": 5,
    },
}
```

Surge configuration:

```python
RIDE_SURGE_MULTIPLIER = 1.00
```

### Surge examples

```text
1.00 = No surge
1.25 = 25% surge
1.50 = 50% surge
2.00 = 100% surge
```

---

# 5. Fare Calculation Formula

The fare calculation follows:

```text
Distance Fare = Distance × Per KM Rate

Time Fare = Duration × Per Minute Rate

Subtotal =
    Base Fare
    + Distance Fare
    + Time Fare

Surge =
    Subtotal × (Surge Multiplier - 1)

Total =
    Subtotal + Surge
```

Fare values are rounded to two decimal places using:

```python
ROUND_HALF_UP
```

---

# 6. Vehicle-Based Pricing

Fare pricing is selected based on:

```python
vehicle_type.name
```

Supported vehicle types:

```text
Bike
Auto
Car
SUV
```

The service validates that pricing exists for the requested vehicle type.

If configuration is missing, an appropriate validation error is returned.

---

# 7. Ride Models

Ride status is represented by:

```text
RideStatus
```

Supported statuses:

```text
REQUESTED
ACCEPTED
DRIVER_ARRIVING
STARTED
COMPLETED
CANCELLED
```

The `Ride` model contains:

```text
rider
driver
vehicle_type
status
pickup_address
pickup_latitude
pickup_longitude
dropoff_address
dropoff_latitude
dropoff_longitude
fare
created_at
updated_at
```

---

# 8. Ride Lifecycle

The ride lifecycle was implemented using controlled status transitions.

### Lifecycle

```text
REQUESTED
    ↓
ACCEPTED
    ↓
DRIVER_ARRIVING
    ↓
STARTED
    ↓
COMPLETED
```

Cancellation is allowed from applicable active states.

```text
REQUESTED → CANCELLED

ACCEPTED → CANCELLED

DRIVER_ARRIVING → CANCELLED
```

Invalid transitions are rejected.

Example:

```text
COMPLETED → STARTED
```

is not allowed.

---

# 9. Ride Status Update

Implemented:

```text
RideStatusUpdateSerializer
```

### File

```text
accounts/serializers.py
```

The serializer validates whether a requested status transition is allowed.

Example transition mapping:

```python
allowed_transitions = {

    REQUESTED: [
        ACCEPTED,
        CANCELLED,
    ],

    ACCEPTED: [
        DRIVER_ARRIVING,
        CANCELLED,
    ],

    DRIVER_ARRIVING: [
        STARTED,
        CANCELLED,
    ],

    STARTED: [
        COMPLETED,
    ],
}
```

---

# 10. Ride Acceptance

Implemented driver ride acceptance.

Acceptance logic verifies:

* Ride exists
* Ride is in `requested` state
* Driver is eligible
* Ride has not already been accepted
* Driver is assigned safely
* Status changes to `accepted`

---

# 11. Concurrent Ride Acceptance

Concurrent ride acceptance was handled safely using database transactions.

The purpose is to prevent two drivers from accepting the same ride simultaneously.

The implementation uses transaction-based locking/atomic operations so that:

```text
Driver A → accepts ride
Driver B → attempts same ride
```

Only one driver can successfully obtain the ride.

The second request receives an appropriate failure response instead of assigning the ride twice.

---

# 12. Database Transactions

Database transaction handling was implemented for operations that modify multiple related records or require atomic state changes.

Transaction handling helps guarantee:

```text
All operations succeed
OR
All operations are rolled back
```

This prevents partially completed ride operations.

---

# 13. Ride Cancellation

Ride cancellation was implemented with state validation.

Cancellation is allowed only when the current ride state permits cancellation.

Invalid cancellation attempts return validation errors.

Example:

```text
COMPLETED → CANCELLED
```

is rejected.

---

# 14. Ride Listing

Implemented:

```python
RideListCreateView
```

### File

```text
accounts/views.py
```

The API supports:

```text
GET  → List rides
POST → Create ride
```

The queryset uses `select_related()` for related objects such as:

```text
rider
profile
status
driver
vehicle_type
```

This improves database query efficiency.

---

# 15. Ride Details

Implemented:

```python
RideDetailSerializer
```

The detail response provides:

```text
Passenger information
Driver information
Vehicle information
Pickup information
Dropoff information
Vehicle type
Ride status
Fare
Created time
Updated time
```

---

# 16. Driver Information

Implemented nested driver representation.

Driver response includes:

```text
Driver ID
Driver name
Vehicle
Vehicle type
Registration number
```

This allows ride detail APIs to return driver-related information without exposing unnecessary internal fields.

---

# 17. Vehicle Validation

Vehicle serializer validation was improved.

Registration numbers are normalized:

```python
value.strip().upper()
```

Validation uses:

```python
re.fullmatch()
```

Duplicate vehicle registration numbers are rejected.

Driver and vehicle type are also validated.

---

# 18. API Business Logic Separation

Business logic was separated from API views.

Instead of keeping fare calculation inside the view, the application uses:

```text
FareService
```

Architecture:

```text
API View
   ↓
Serializer
   ↓
Service Layer
   ↓
Models / Database
```

This makes the application easier to:

* Test
* Maintain
* Reuse
* Extend
* Debug

---

# 19. Tests Created

The following tests were created:

```text
accounts/tests/test_duplicate_acceptance.py
accounts/tests/test_fare.py
accounts/tests/test_invalid_state.py
accounts/tests/test_ride_acceptance.py
accounts/tests/test_ride_cancellation.py
accounts/tests/test_ride_creation.py
```

### Test coverage includes

* Ride creation
* Fare calculation
* Ride acceptance
* Duplicate acceptance
* Ride cancellation
* Invalid state transitions
* Ride lifecycle behavior

---

# 20. Ride Creation Test

Command used:

```powershell
python manage.py test accounts.tests.test_ride_creation
```

Final result:

```text
STATUS: 201
```

Test result:

```text
Ran 1 test
OK
```

Example successful response included:

```text
pickup_address: Guntur
dropoff_address: Vijayawada
status: requested
fare: 101.29
```

This confirms that:

```text
Request
   ↓
Validation
   ↓
Fare Calculation
   ↓
Ride Creation
   ↓
201 Created
```

works correctly.

---

# 21. Django System Check

Command:

```powershell
python manage.py check
```

Result:

```text
System check identified no issues (0 silenced).
```

This confirmed there were no Django configuration/system-check errors.

---

# 22. Exception Handling

A custom exception handler exists in:

```text
accounts/exceptions.py
```

It provides a consistent API error format.

Example:

```json
{
    "success": false,
    "error": "..."
}
```

This helps maintain consistent error responses across APIs.

---

# 23. README Documentation

Project documentation was updated in:

```text
README.md
```

The README includes the implemented features such as:

```text
JWT Authentication
User Profile Management
Driver Management
Vehicle Management
Ride Creation
Ride Listing
Ride Details
Ride Status Update
Ride Acceptance
Ride Cancellation
Ride Lifecycle Testing
Invalid Transition Testing
```

Git conflict markers were also cleaned from the README.

---

# 24. Git Workflow

Changes were integrated with the remote `main` branch using:

```powershell
git fetch origin
git pull --rebase origin main
```

README changes were committed using:

```powershell
git add README.md
git commit -m "Update README"
```

Finally pushed using:

```powershell
git push origin main
```

Latest verified commit:

```text
92d7869 Update README
```

Local branch and remote branch were synchronized:

```text
HEAD -> main
origin/main
```

---

# 25. Final Acceptance Criteria

| Acceptance Criteria                                | Status      |
| -------------------------------------------------- | ----------- |
| Service layer implemented                          | ✅ Completed |
| Fare calculation completed                         | ✅ Completed |
| Database transactions implemented                  | ✅ Completed |
| Concurrent ride acceptance handled safely          | ✅ Completed |
| Unit tests created                                 | ✅ Completed |
| Business logic separated from API views            | ✅ Completed |
| Code refactored according to Django best practices | ✅ Completed |

---

# 26. Final Project Flow

```text
                CLIENT
                   │
                   ▼
             Django API
                   │
                   ▼
              View Layer
                   │
                   ▼
           Serializer Layer
                   │
          ┌────────┴────────┐
          ▼                 ▼
    Validation         Service Layer
                            │
                            ▼
                      FareService
                            │
                            ▼
                       Database
                            │
                            ▼
                     Ride / Status
```

### Complete Ride Flow

```text
Create Ride
     ↓
Validate Location
     ↓
Check Active Ride
     ↓
Calculate Distance
     ↓
Calculate Fare
     ↓
Create REQUESTED Ride
     ↓
Driver Accepts
     ↓
ACCEPTED
     ↓
DRIVER_ARRIVING
     ↓
STARTED
     ↓
COMPLETED
```

Cancellation:

```text
REQUESTED
     ↓
CANCELLED
```

or

```text
ACCEPTED
     ↓
CANCELLED
```

or

```text
DRIVER_ARRIVING
     ↓
CANCELLED
```

---

## 27. Final Verification Commands

For future verification:

```powershell
python manage.py check
```

```powershell
python manage.py test accounts.tests.test_ride_creation
```

Full accounts tests:

```powershell
python manage.py test accounts
```

Git verification:

```powershell
git status
```

Remote verification:

```powershell
git log origin/main --oneline -5
```

14/08/2026



````markdown
# Ride Management API

A Django REST Framework based Ride Management API that provides authentication, user profiles, driver and vehicle management, ride lifecycle management, fare calculation, permissions, automated testing, and database query optimization.

---

## 1. Project Overview

This project is a backend REST API for managing a ride-booking system.

The application supports:

- User registration and authentication
- JWT login/logout
- User profile management
- Driver management
- Vehicle management
- Vehicle types
- Ride creation
- Ride acceptance
- Ride status management
- Ride cancellation
- Fare calculation
- Ride history
- Driver earnings
- Permissions and ownership validation
- Exception handling
- Automated tests
- Database query optimization

---

## 2. Technology Stack

### Backend

- Python
- Django
- Django REST Framework

### Authentication

- JWT Authentication
- `djangorestframework-simplejwt`

### Database

- Django ORM
- Relational database

### Testing

- Django Test Framework
- Django REST Framework APIClient

### API Testing

- Postman

---

## 3. Project Structure

```text
myproject/
│
├── accounts/
│   │
│   ├── migrations/
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── fare_service.py
│   │   └── ride.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_duplicate_acceptance.py
│   │   ├── test_fare.py
│   │   ├── test_invalid_state.py
│   │   ├── test_ride_acceptance.py
│   │   ├── test_ride_cancellation.py
│   │   └── test_ride_creation.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   └── responses.py
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
````

---

# 4. Installation

## Step 1 — Clone or download the project

Place the project in your desired directory.

Example:

```text
C:\Users\<username>\Desktop\django\myproject
```

---

## Step 2 — Create virtual environment

```powershell
python -m venv venv
```

---

## Step 3 — Activate virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

After activation:

```text
(venv)
```

should appear in the terminal.

---

## Step 4 — Install dependencies

```powershell
pip install -r requirements.txt
```

---

# 5. Database Setup

Run migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

# 6. Create Admin User

```powershell
python manage.py createsuperuser
```

Enter:

```text
Email
Password
```

The admin account can be used to manage drivers and other administrative data.

---

# 7. Run Development Server

```powershell
python manage.py runserver
```

The API will normally be available at:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# 8. Authentication

The API uses JWT authentication.

## Login

Example:

```http
POST /api/login/
```

Request:

```json
{
    "email": "user@example.com",
    "password": "password"
}
```

Successful response contains:

```json
{
    "user": {
        "id": "USER_ID",
        "email": "user@example.com"
    },
    "refresh": "REFRESH_TOKEN",
    "access": "ACCESS_TOKEN"
}
```

Use the access token for protected APIs.

Postman:

```text
Authorization
→ Bearer Token
→ ACCESS_TOKEN
```

---

# 9. Main API Features

## Authentication

```text
Register
Login
Logout
Change Password
```

---

## User Profile

```text
Get Profile
Create/Update Profile
Delete Profile
Restore Profile
Admin Profile List
```

---

## Driver

```text
Create Driver
List Drivers
Get Driver
Update Driver
```

Driver creation and management are restricted according to the configured permissions.

---

## Vehicle

```text
Create Vehicle
List Vehicles
Get Vehicle
Update Vehicle
Delete Vehicle
```

Drivers can manage their own vehicles.

Administrators can manage vehicles according to the configured permissions.

---

# 10. Ride Lifecycle

A ride follows a controlled lifecycle.

```text
REQUESTED
    ↓
ACCEPTED
    ↓
DRIVER_ARRIVING
    ↓
STARTED
    ↓
COMPLETED
```

A ride may also be cancelled when the current state allows cancellation.

Example:

```text
REQUESTED
    ↓
CANCELLED
```

Invalid state transitions are rejected by the application.

---

# 11. Create Ride

Example:

```http
POST /api/rides/
```

Request:

```json
{
    "pickup_address": "Guntur",
    "pickup_latitude": "16.306700",
    "pickup_longitude": "80.436500",
    "dropoff_address": "Vijayawada",
    "dropoff_latitude": "16.320000",
    "dropoff_longitude": "80.450000",
    "vehicle_type": "VEHICLE_TYPE_UUID"
}
```

Successful response:

```text
201 Created
```

The authenticated user is automatically associated with the ride as the rider.

---

# 12. Accept Ride

Driver authentication is required.

Example:

```http
POST /api/rides/{ride_id}/accept/
```

Successful response:

```json
{
    "success": true,
    "message": "Ride accepted successfully."
}
```

A ride that has already been accepted cannot be accepted again.

---

# 13. Update Ride Status

Example:

```http
PATCH /api/rides/{ride_id}/status/
```

Request:

```json
{
    "status": "started"
}
```

Later:

```json
{
    "status": "completed"
}
```

The service layer validates whether the requested state transition is allowed.

---

# 14. Cancel Ride

Example:

```http
POST /api/rides/{ride_id}/cancel/
```

Only the appropriate authenticated rider can cancel the ride according to the configured business rules.

---

# 15. Fare Calculation

Example:

```http
POST /api/rides/fare/
```

Request:

```json
{
    "vehicle_type": "VEHICLE_TYPE_UUID",
    "pickup_latitude": "16.306700",
    "pickup_longitude": "80.436500",
    "dropoff_latitude": "16.320000",
    "dropoff_longitude": "80.450000",
    "duration_minutes": 10
}
```

Response contains:

```json
{
    "success": true,
    "message": "Fare calculated successfully.",
    "data": {
        "base_fare": "...",
        "distance_fare": "...",
        "time_fare": "...",
        "surge": "...",
        "total": "..."
    }
}
```

Fare calculation is implemented in:

```text
accounts/services/fare_service.py
```

---

# 16. Ride History

The application provides APIs for:

```text
Active rides
Completed rides
Cancelled rides
Driver ride history
```

Additional statistics include:

```text
Daily ride count
Total completed rides
Driver total fare earned
```

---

# 17. Permissions

The API uses authentication and permission checks.

Examples:

### Unauthenticated user

Protected endpoints return:

```text
401 Unauthorized
```

### Authenticated user without required permission

Returns:

```text
403 Forbidden
```

### Admin-only functionality

Restricted using:

```python
IsAdminUser
```

### Driver ownership

Driver/vehicle resources are protected using ownership permissions.

---

# 18. Exception Handling

The project uses a custom DRF exception handler:

```text
accounts/utils/exceptions.py
```

The exception handler provides a consistent API response format.

Example:

```json
{
    "success": false,
    "message": "Request failed.",
    "error_code": "API_ERROR",
    "data": null
}
```

Internal server errors return:

```json
{
    "success": false,
    "message": "Internal server error.",
    "error_code": "INTERNAL_SERVER_ERROR",
    "data": null
}
```

Detailed exception information should be logged internally rather than exposed to API clients.

---

# 19. Standard Response Format

Successful responses generally follow:

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {}
}
```

Error responses generally follow:

```json
{
    "success": false,
    "message": "Request failed.",
    "error_code": "ERROR_CODE",
    "data": null
}
```

---

# 20. Automated Testing

Tests are located in:

```text
accounts/tests/
```

Current test areas include:

```text
Ride creation
Ride acceptance
Duplicate ride acceptance
Ride cancellation
Invalid ride states
Fare calculation
```

Run all accounts tests:

```powershell
python manage.py test accounts.tests
```

Run a specific test:

```powershell
python manage.py test accounts.tests.test_ride_creation
```

Example successful result:

```text
Found 1 test(s).
...
Ran 1 test
OK
```

---

# 21. Postman Regression Testing

The complete API should be tested using Postman.

Recommended execution order:

```text
1. Register
2. Login
3. Create Driver
4. Create Vehicle
5. Create Ride
6. Accept Ride
7. Start Ride
8. Complete Ride
9. Calculate Fare
10. Ride History
11. Permission Tests
12. Invalid Request Tests
```

Each request should be checked for:

```text
HTTP status code
Response body
success value
message
error_code
data
```

---

# 22. Database Query Optimization

The project includes optimized ride history queries using:

```python
select_related()
```

Example:

```python
Ride.objects.filter(
    rider=request.user
).select_related(
    "rider",
    "vehicle_type",
    "status",
)
```

This reduces unnecessary database queries when accessing related objects.

The project also contains a slow/optimized comparison for demonstrating query optimization.

---

# 23. Architecture

The project follows a layered architecture.

```text
                CLIENT
                  |
                  v
                POSTMAN
                  |
                  v
                URLS
                  |
                  v
                VIEWS
                  |
          +-------+-------+
          |               |
          v               v
     SERIALIZERS     PERMISSIONS
          |
          v
        SERVICES
       /         \
      v           v
RideService   FareService
      \           /
       \         /
          v
        MODELS
          |
          v
       DATABASE
```

### URLs

Routes incoming API requests to the appropriate view.

### Views

Handle HTTP requests and responses.

### Serializers

Validate request data and convert model data to API responses.

### Permissions

Control access to protected resources.

### Services

Contain business logic such as:

```text
Ride acceptance
Ride cancellation
Ride status transitions
Fare calculation
```

### Models

Define database entities and relationships.

### Database

Stores application data persistently.

---

# 24. Security

The application uses:

* JWT authentication
* Django password hashing
* DRF permissions
* Driver ownership checks
* Admin access controls
* Validation of incoming request data
* Custom exception handling

Production deployments should use:

```text
DEBUG = False
```

Sensitive configuration such as:

```text
SECRET_KEY
Database credentials
JWT configuration
```

should be stored securely using environment variables.

---

# 25. Code Quality

The project was reviewed for:

```text
Naming
Folder structure
Functions
Serializers
Views
Services
Models
Database queries
Exception handling
Security
```


---

# 26. Final Demonstration

The complete project can be demonstrated using the following flow:

```text
Login
  ↓
Create Driver
  ↓
Create Vehicle
  ↓
Create Ride
  ↓
Accept Ride
  ↓
Start Ride
  ↓
Complete Ride
  ↓
Calculate Fare
  ↓
Show Database Records
  ↓
Explain Architecture
```

---

# 27. Final Verification

Before final submission, run:

```powershell
python manage.py check
```

Then:

```powershell
python manage.py test accounts.tests
```

Then start the server:

```powershell
python manage.py runserver
```

Finally execute the complete Postman collection from beginning to end.

---

# 28. Expected Final Status

The project is considered ready for demonstration when:

```text
Django system check      → PASS
Automated tests          → PASS
Postman regression       → PASS
Authentication           → PASS
Driver management        → PASS
Vehicle management       → PASS
Ride lifecycle           → PASS
Fare calculation         → PASS
Permissions              → PASS
Invalid requests         → Proper errors
Database records         → Correct
Architecture             → Explainable
```

---

## Author

Ride Management API
Django REST Framework Project
 
 17/08/26
 
 
# Django Ride Management API

A Django REST Framework based Ride Management API with authentication,
driver management, vehicle management, ride management, ORM optimization,
filtering, indexing, pagination, and performance testing.

---

## Tech Stack

- Python 3.13
- Django 6.0.8
- Django REST Framework
- Django Filter
- Simple JWT
- SQLite / Database configured in project settings

---

# Project Features

## 1. Authentication

The project supports:

- User registration
- User login
- JWT access token
- JWT refresh token
- Logout
- Change password

Authentication is based on email instead of username.

---

## 2. Profile Management

Users can:

- Create profile
- View profile
- Update profile
- Upload profile image
- Soft delete profile
- Restore profile

Admin users can view profiles.

---

## 3. Driver Management

Admin users can:

- Create drivers
- List drivers
- View driver details
- Update drivers
- Search drivers
- Filter drivers by status
- Order drivers by different fields

Example ordering:

```text
?ordering=-created_at
````

---

## 4. Vehicle Management

Drivers can manage their vehicles.

Supported operations:

* Create vehicle
* List vehicles
* View vehicle
* Update vehicle
* Delete vehicle

Vehicles are related to:

* Driver
* Vehicle Type

`select_related()` is used to optimize related-object queries.

---

# Task 3 — ORM Aggregations

Ride statistics are calculated using Django ORM aggregation functions.

Implemented:

* Total rides
* Completed rides
* Cancelled rides
* Average fare
* Maximum fare
* Minimum fare
* Total driver earnings

ORM functions used:

```python
Count()
Sum()
Avg()
Min()
Max()
Q()
```

Example:

```python
Ride.objects.filter(
    rider=request.user
).aggregate(
    total_rides=Count("id"),
    average_fare=Avg("fare"),
    maximum_fare=Max("fare"),
    minimum_fare=Min("fare"),
)
```

---

# Task 4 — Optimize Relationships

The project contains both slow and optimized ride-history APIs.

## Slow API

The slow implementation accesses related objects inside a loop.

Example:

```python
for ride in rides:
    driver = ride.driver
    driver_user = driver.user
    status = ride.status
    vehicle_type = ride.vehicle_type
```

This can generate multiple database queries.

## Optimized API

The optimized implementation uses:

```python
select_related()
```

Example:

```python
Ride.objects.filter(
    rider=request.user
).select_related(
    "driver",
    "driver__user",
    "vehicle_type",
    "status",
)
```

This loads related ForeignKey / OneToOne objects together.

The API returns the query count so the slow and optimized implementations can be compared.

Example response:

```json
{
    "success": true,
    "optimization": "optimized",
    "query_count": 1,
    "count": 10,
    "results": []
}
```

---

# Task 5 — Database Indexing

Frequently searched and filtered fields were identified and indexed.

Important fields include:

```text
rider
driver
status
created_at
vehicle_type
```

Indexes were added using Django's `Meta.indexes`.

Example:

```python
class Meta:

    indexes = [
        models.Index(fields=["rider"]),
        models.Index(fields=["driver"]),
        models.Index(fields=["status"]),
        models.Index(fields=["created_at"]),
    ]
```

Composite indexes were also added for common queries:

```python
models.Index(
    fields=["rider", "created_at"]
)

models.Index(
    fields=["driver", "created_at"]
)

models.Index(
    fields=["status", "created_at"]
)
```

These indexes help improve filtering and ordering performance for large datasets.

After modifying indexes, run:

```powershell
python manage.py makemigrations
python manage.py migrate
```

---

# Task 6 — Advanced Filtering

Ride APIs support advanced filtering.

Implemented filters:

* Date filtering
* Status filtering
* Driver filtering
* Minimum fare
* Maximum fare
* Multiple filters together
* Ordering

Example query parameters:

```text
?status=completed
```

```text
?driver=<driver_uuid>
```

```text
?min_fare=100
```

```text
?max_fare=500
```

Multiple filters can be combined:

```text
?status=completed&driver=<driver_uuid>&min_fare=100&max_fare=500
```

Ordering examples:

```text
?ordering=created_at
```

```text
?ordering=-created_at
```

Descending ordering is represented using:

```text
- 
```

Example:

```text
?ordering=-created_at
```

---

# Task 7 — Large Dataset Testing

The API was tested with a large number of ride records.

The purpose of this task is to verify:

* API response performance
* Pagination
* Database query count
* ORM performance
* Index performance

Pagination is configured using:

```python
class CustomPagination(PageNumberPagination):

    page_size = 10

    page_size_query_param = "page_size"

    max_page_size = 50
```

Example:

```text
?page=1
```

Custom page size:

```text
?page=1&page_size=20
```

Maximum page size:

```text
50
```

This prevents the API from returning thousands of records in one response.

---

# Task 8 — Code Review

The ORM code was reviewed for unnecessary database operations.

The following problems were identified and optimized:

## Duplicate Queries

Repeated queries for the same related objects were reduced using:

```python
select_related()
```

---

## Queries Inside Loops

Avoid:

```python
for ride in rides:
    driver = ride.driver
    status = ride.status
```

when relationships can be loaded beforehand.

Use:

```python
rides = Ride.objects.select_related(
    "driver",
    "status",
    "vehicle_type",
)
```

---

## Unnecessary Database Calls

Avoid unnecessary calls such as:

```python
Ride.objects.get(id=id)
```

when the same object is already available.

Reuse the existing object whenever possible.

---

## Repeated Calculations

Repeated calculations were moved to ORM aggregation where appropriate.

Example:

```python
Ride.objects.aggregate(
    total=Sum("fare"),
    average=Avg("fare"),
)
```

instead of repeatedly calculating values in Python.

---

# ORM Optimization Summary

The project uses:

### select_related()

Used for ForeignKey and OneToOne relationships.

Example:

```python
Ride.objects.select_related(
    "driver",
    "driver__user",
    "status",
    "vehicle_type",
)
```

### prefetch_related()

Used when loading reverse relationships or many-to-many relationships.

Example:

```python
DriverProfile.objects.prefetch_related(
    "vehicles"
)
```

---

# Database Index Summary

Important indexes:

```text
Ride.rider
Ride.driver
Ride.status
Ride.created_at
Ride.vehicle_type
```

Composite indexes:

```text
rider + created_at
driver + created_at
status + created_at
```

---

# Pagination

API pagination uses:

```text
page_size = 10
max_page_size = 50
```

Example:

```text
GET /api/rides/?page=1
```

```text
GET /api/rides/?page=2
```

```text
GET /api/rides/?page=1&page_size=20
```

---

# Running the Project

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Run migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Run the development server:

```powershell
python manage.py runserver
```

Server:

```text
http://127.0.0.1:8000/
```

---

# Useful Django Commands

Check project:

```powershell
python manage.py check
```

Create migrations:

```powershell
python manage.py makemigrations
```

Apply migrations:

```powershell
python manage.py migrate
```

Open Django shell:

```powershell
python manage.py shell
```

Create admin user:

```powershell
python manage.py createsuperuser
```

Run server:

```powershell
python manage.py runserver
```

---

# Testing ORM Queries

Django shell can be used to inspect queries.

Example:

```python
from django.db import connection, reset_queries
from accounts.models import Ride

reset_queries()

rides = Ride.objects.select_related(
    "driver",
    "driver__user",
    "status",
    "vehicle_type",
)

list(rides)

print(len(connection.queries))
```

This can be used to compare slow and optimized queries.

---

# API Testing

The APIs can be tested using:

* Postman
* Browser
* Django REST Framework browsable API

For authenticated APIs, send the JWT access token:

```text
Authorization: Bearer <access_token>
```

---

# Project Goals

The main goal of this project is to demonstrate:

1. Django REST Framework API development
2. Authentication and authorization
3. Django ORM relationships
4. Query optimization
5. Database indexing
6. Advanced filtering
7. Pagination
8. Aggregations
9. Large dataset testing
10. Database performance improvement

---

# Tasks Completed

| Task   | Description                   | Status    |
| ------ | ----------------------------- | --------- |
| Task 1 | Basic Django / API setup      | Completed |
| Task 2 | ORM relationships and indexes | Completed |
| Task 3 | ORM aggregations              | Completed |
| Task 4 | Relationship optimization     | Completed |
| Task 5 | Database indexing             | Completed |
| Task 6 | Advanced filtering            | Completed |
| Task 7 | Large dataset testing         | Completed |
| Task 8 | ORM code review               | Completed |

---

# Important Note

This project uses Django's development server for development and testing only.

For production deployment, use a proper WSGI or ASGI server and production database configuration.

```
18/08/26

````markdown
# Driver Location & Nearby Driver API

## Overview

This module provides driver location tracking, driver availability management,
nearby-driver search, distance calculation, validation, and performance testing.

The system finds eligible drivers near a passenger's pickup location and
returns them sorted by distance.

---

## Features

- Driver location update
- Driver availability management
- Nearby driver search
- Distance calculation using Haversine formula
- Nearest driver sorting
- Location validation
- Active driver filtering
- Online driver filtering
- Busy/offline driver exclusion
- Large dataset performance testing

---

## Driver Availability

Drivers can have one of the following availability statuses:

```text
ONLINE
OFFLINE
BUSY
````

Only `ONLINE` drivers are eligible for new ride requests.

---

## Driver Location API

### Endpoint

```http
POST /api/drivers/location/
```

### Authentication

Requires a valid Bearer access token.

```http
Authorization: Bearer <ACCESS_TOKEN>
```

### Example Request

```json
{
    "latitude": 17.385,
    "longitude": 78.4867,
    "availability_status": "online"
}
```

### Example Response

```json
{
    "success": true,
    "message": "Driver location updated successfully.",
    "error_code": null,
    "data": {
        "driver_id": "d40f766b-1947-4eec-97ed-d01ffe0a6282",
        "latitude": 17.385,
        "longitude": 78.4867,
        "availability_status": "online"
    }
}
```

---

## Nearby Driver API

### Endpoint

```http
GET /api/drivers/nearby/
```

### Query Parameters

| Parameter | Required | Description         |
| --------- | -------- | ------------------- |
| latitude  | Yes      | Passenger latitude  |
| longitude | Yes      | Passenger longitude |
| radius    | Yes      | Search radius in KM |

### Example

```http
GET /api/drivers/nearby/?latitude=17.385&longitude=78.4867&radius=5
```

### Authentication

```http
Authorization: Bearer <ACCESS_TOKEN>
```

### Example Response

```json
{
    "success": true,
    "message": "Nearby drivers retrieved successfully.",
    "error_code": null,
    "data": {
        "latitude": 17.385,
        "longitude": 78.4867,
        "radius_km": 5.0,
        "count": 3,
        "drivers": [
            {
                "driver_id": "driver-b",
                "distance_km": 1.4,
                "availability_status": "online"
            },
            {
                "driver_id": "driver-c",
                "distance_km": 2.7,
                "availability_status": "online"
            },
            {
                "driver_id": "driver-a",
                "distance_km": 4.2,
                "availability_status": "online"
            }
        ]
    }
}
```

---

## Distance Calculation

Distance is calculated using the Haversine formula.

Earth radius:

```text
6371 KM
```

The calculated distance is used to:

1. Check whether the driver is within the requested radius.
2. Return `distance_km`.
3. Sort drivers from nearest to farthest.

Example:

```text
Driver B → 1.4 KM
Driver C → 2.7 KM
Driver A → 4.2 KM
```

The API returns Driver B first because it is the nearest driver.

---

## Driver Eligibility

A driver is returned only when:

```text
Driver status = ACTIVE
AND
Availability status = ONLINE
AND
Driver location is within requested radius
```

The following drivers are excluded:

```text
INACTIVE drivers
SUSPENDED drivers
OFFLINE drivers
BUSY drivers
Drivers outside the requested radius
```

---

## Location Validation

The API validates all location parameters.

### Missing coordinates

```json
{
    "success": false,
    "message": "latitude, longitude and radius are required.",
    "error_code": "MISSING_REQUIRED_FIELD",
    "data": null
}
```

### Invalid latitude

Latitude must be between:

```text
-90 and 90
```

Example:

```json
{
    "success": false,
    "message": "Invalid latitude.",
    "error_code": "INVALID_LATITUDE",
    "data": null
}
```

### Invalid longitude

Longitude must be between:

```text
-180 and 180
```

Example:

```json
{
    "success": false,
    "message": "Invalid longitude.",
    "error_code": "INVALID_LONGITUDE",
    "data": null
}
```

### Invalid radius

Radius must be greater than `0`.

Example:

```json
{
    "success": false,
    "message": "Radius must be greater than 0.",
    "error_code": "INVALID_RADIUS",
    "data": null
}
```

---

## Performance Testing

A large dataset was created for performance testing.

### Test Dataset

```text
Drivers created: 1000
```

Nearby-driver search was tested with:

```text
Latitude: 17.385
Longitude: 78.4867
Radius: 5 KM
```

Example result:

```text
HTTP Status: 200 OK
Nearby drivers found: 669
```

The API successfully handled the large test dataset and returned nearby
eligible drivers sorted by distance.

---

## Database Optimization

`DriverLocation` has an index on availability status:

```python
class Meta:
    indexes = [
        models.Index(
            fields=["availability_status"]
        ),
    ]
```

The query also uses:

```python
.select_related(
    "driver",
    "driver__user",
)
```

This reduces additional database queries when accessing driver and user
information.

---

## Acceptance Criteria

* [x] Driver location API completed
* [x] Nearby driver API completed
* [x] Distance calculated correctly
* [x] Driver availability integrated
* [x] Invalid coordinates rejected
* [x] Only eligible drivers returned
* [x] Location search tested with large datasets

---

## Task Status

```text
Task 4 - Distance Calculation       COMPLETED
Task 5 - Nearby Driver Sorting      COMPLETED
Task 6 - Driver Availability        COMPLETED
Task 7 - Location Validation        COMPLETED
Task 8 - Performance Testing        COMPLETED
```
19/08/26

Sure 👍 Nee current Jira story **Real-Time Communication Using Django Channels & WebSockets** ki suitable ga `README.md` first create cheddam.

Project root:

```text
C:\Users\BlackRoth\Desktop\django\myproject
```

### 1. `README.md` create cheyyi

VS Code lo project root folder meeda:

**Right Click → New File → `README.md`**

### 2. `README.md` lo idi complete ga paste cheyyi

````markdown
# Real-Time Communication Using Django Channels & WebSockets

## Overview

This project implements real-time communication for a ride-booking application using Django Channels and WebSockets.

The main objective is to allow mobile applications to receive real-time ride updates without repeatedly calling REST APIs.

## Technology Stack

- Python
- Django
- Django REST Framework
- Django Channels
- Daphne
- WebSockets
- Simple JWT
- SQLite

## REST API vs WebSocket

### REST API

```text
Mobile Application → Request → Backend
Mobile Application ← Response ← Backend
````

REST APIs are suitable for normal request-response operations.

### WebSocket

```text
Mobile Application ←→ WebSocket Server
        Real-time connection
```

WebSockets are useful when the application needs continuous real-time updates.

## WebSocket Use Cases

WebSockets are used for:

* Ride status updates
* Driver location updates
* Real-time ride communication
* Driver connection status
* Passenger connection status

## WebSocket Endpoints

### Ride WebSocket

```text
ws://127.0.0.1:8000/ws/ride/<ride_id>/?token=<access_token>
```

This WebSocket allows authorized users to connect to a specific ride.

### Driver Location WebSocket

```text
ws://127.0.0.1:8000/ws/driver/location/?token=<access_token>
```

This WebSocket is used for driver location communication.

## Authentication

WebSocket connections are protected using JWT access tokens.

The connection verifies:

1. JWT token
2. User identity
3. Ride existence
4. Ride ownership
5. Assigned driver authorization

Unauthorized users are rejected.

## Ride Authorization

A user can connect to a ride WebSocket only when:

* The user is the rider of the ride, or
* The user is the assigned driver of the ride.

Other users are rejected.

## Real-Time Ride Status Updates

Ride status updates are broadcast through the WebSocket channel group.

Example statuses:

* requested
* accepted
* driver_arriving
* started
* completed
* cancelled

## Driver Location Updates

Driver location information can be communicated through WebSockets so that connected clients can receive real-time location updates.

## Disconnect Handling

The WebSocket implementation handles:

* Mobile application closed
* Network disconnection
* Driver disconnection
* Passenger disconnection
* Invalid JWT token
* Unauthorized connection attempts

When a client disconnects, it is removed from the appropriate WebSocket channel group.

## Multiple Client Testing

The system is tested with multiple users:

* Passenger
* Driver
* Admin / unauthorized user

The tests verify that only authorized users receive ride-specific events.

## Unauthorized User Test

An unauthorized passenger attempting to connect to another user's ride is rejected.

Expected result:

```text
403 Access Denied
```

This prevents users from accessing another user's ride WebSocket.

## Database Models

Important models include:

* User
* Profile
* DriverProfile
* Vehicle
* VehicleType
* RideStatus
* Ride
* DriverLocation
* Notification

## Notification Handling

The notification system is designed to prevent duplicate notifications for the same event.

Notifications can be retrieved and marked as read.

## Running the Project

### Activate Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Check Django Configuration

```powershell
python manage.py check
```

### Start Development Server

```powershell
python manage.py runserver
```

The server runs at:

```text
http://127.0.0.1:8000/
```

## Testing

WebSocket connections can be tested using Postman WebSocket requests.

Example:

```text
ws://127.0.0.1:8000/ws/ride/<ride_id>/?token=<access_token>
```

Test cases include:

* Successful passenger connection
* Successful driver connection
* Invalid token
* Unauthorized user
* Ride ownership validation
* Driver authorization
* Ride status broadcast
* Driver location broadcast
* Disconnect
* Reconnect
* Multiple clients

## Security

The following security checks are implemented:

* JWT authentication
* User identity validation
* Ride ownership validation
* Driver authorization
* Unauthorized WebSocket rejection

### Important

Do not commit sensitive information such as:

* `.env`
* JWT access tokens
* Secret keys
* Passwords
* Database credentials

## Project Status

### Completed

* WebSocket server configuration
* Django Channels integration
* Daphne ASGI server
* JWT authentication
* Ride ownership validation
* Driver authorization
* Unauthorized user rejection
* WebSocket disconnect handling
* Multiple-client testing setup
* Notification model and migration

### Testing / Verification

* Ride status broadcast
* Driver location broadcast
* Passenger and driver simultaneous connections
* Disconnect/reconnect scenarios
* Duplicate notification prevention

## Acceptance Criteria

* [x] WebSocket server configured
* [x] Authenticated WebSocket connection implemented
* [x] Unauthorized users rejected
* [x] Disconnect handling implemented
* [ ] Ride status updates fully tested
* [ ] Driver location updates fully tested
* [ ] Multiple clients fully tested
* [ ] Disconnect/reconnect scenarios fully verified

## Author

Django Real-Time Communication Project

````

### 3. Save

```text
Ctrl + S
````

### 4. Check Git

PowerShell lo:

```powershell
git status
```
20/8/26



## 1. Project Overview

This module implements **asynchronous notification processing** for the ride-booking application.

The main objective is to process notification events in the background so that API requests can return quickly without waiting for notification processing to complete.

### Processing Flow

```text
Mobile App
    ↓
API Request
    ↓
Create Background Job
    ↓
Immediate API Response
    ↓
Background Worker
    ↓
Create Notification
    ↓
Mobile User Receives Notification
```

---

# 2. Features Implemented

* Notification model
* Notification REST APIs
* Pagination
* Background task processing
* Ride notification handling
* Driver assignment notification
* Ride completion notification
* Reminder notification
* Retry handling
* Duplicate notification prevention
* Notification retrieval
* Mark notification as read
* Read all notifications
* Testing

---

# 3. Notification Model

The `Notification` model contains the following fields:

| Field             | Description                                 |
| ----------------- | ------------------------------------------- |
| User              | User who receives the notification          |
| Ride              | Related ride                                |
| Notification Type | Type of notification                        |
| Message           | Notification message                        |
| Is Read           | Indicates whether the notification was read |
| Created At        | Notification creation time                  |

### Notification Types

Examples:

```text
JOB_SUCCESS
JOB_FAILED
JOB_RETRY
```

---

# 4. Notification APIs

### Get Notifications

```http
GET /api/notifications/
```

Returns notifications for the authenticated user.

Pagination is supported.

---

### Mark Notification as Read

```http
PATCH /api/notifications/{id}/read/
```

Marks a specific notification as read.

Example:

```text
is_read: false
        ↓
PATCH request
        ↓
is_read: true
```

---

### Mark All Notifications as Read

```http
POST /api/notifications/read-all/
```

Marks all notifications belonging to the authenticated user as read.

---

# 5. Background Processing

Background processing is used so notification creation does not block the main API request.

### Ride Notification

```text
Ride Event
    ↓
Background Task
    ↓
Create Notification
    ↓
Notify User
```

### Driver Assignment

```text
Driver Assigned
    ↓
Background Task
    ↓
Passenger Notification
```

### Ride Completion

```text
Ride Completed
    ↓
Background Task
    ↓
Passenger Notification
```

### Reminder

```text
Reminder Event
    ↓
Background Task
    ↓
Create Reminder Notification
```

---

# 6. Retry Handling

Failed background jobs are retried automatically.

### Retry Flow

```text
Attempt 1
   ↓
 Failed
   ↓
Retry
   ↓
Attempt 2
   ↓
 Failed
   ↓
Retry
   ↓
Attempt 3
   ↓
 Success
```

Retry handling prevents temporary failures from permanently stopping notification processing.

---

# 7. Duplicate Notification Prevention

Duplicate notifications are prevented using a unique constraint based on:

```text
User
+
Ride
+
Notification Type
```

The database constraint used is:

```text
unique_ride_notification
```

### Example

```text
First Event
    ↓
JOB_SUCCESS Notification
    ↓
Created Successfully
```

If the same event occurs again:

```text
Same User + Same Ride + Same Notification Type
                    ↓
              Duplicate Request
                    ↓
                Rejected
```

This ensures that the same ride event does not create multiple identical notifications.

---

# 8. Testing

The notification system was tested for the following scenarios.

## 8.1 Successful Job

A successful job notification was created successfully.

```text
JOB_SUCCESS
```

**Expected Result:** Notification is stored successfully.

**Result:** ✅ PASS

---

## 8.2 Failed Job

A failed job notification was created.

```text
JOB_FAILED
```

**Expected Result:** Failed notification is stored correctly.

**Result:** ✅ PASS

---

## 8.3 Retry

Retry handling was tested for failed jobs.

```text
Attempt 1 → Failed
Attempt 2 → Failed
Attempt 3 → Success
```

**Expected Result:** Failed jobs are retried according to the configured retry mechanism.

**Result:** ✅ PASS

---

## 8.4 Duplicate Prevention

The same `JOB_SUCCESS` notification was attempted twice for the same user and ride.

The second notification was rejected because of:

```text
unique_ride_notification
```

**Expected Result:** Only one notification exists for the same event.

**Result:** ✅ PASS

---

## 8.5 Notification Retrieval

The following API was tested:

```http
GET /api/notifications/
```

**Expected Result:**

* Authenticated user can retrieve notifications.
* Notifications are returned with pagination.
* User receives only their own notifications.

**Result:** ✅ PASS

---

## 8.6 Mark as Read

The following API was tested:

```http
PATCH /api/notifications/{id}/read/
```

### Before

```json
{
    "is_read": false
}
```

### After

```json
{
    "is_read": true
}
```

**Expected Result:** Notification is successfully marked as read.

**Result:** ✅ PASS

---

# 9. Test Summary

| Test Case              | Result |
| ---------------------- | ------ |
| Successful Job         | ✅ PASS |
| Failed Job             | ✅ PASS |
| Retry                  | ✅ PASS |
| Duplicate Prevention   | ✅ PASS |
| Notification Retrieval | ✅ PASS |
| Mark as Read           | ✅ PASS |

---

# 10. Acceptance Criteria

| Acceptance Criteria                | Status      |
| ---------------------------------- | ----------- |
| Notification module completed      | ✅ Completed |
| Background worker configured       | ✅ Completed |
| Redis integration completed        | ✅ Completed |
| Asynchronous notifications working | ✅ Completed |
| Retry mechanism implemented        | ✅ Completed |
| Duplicate notifications prevented  | ✅ Completed |
| Notification APIs tested           | ✅ Completed |

---

# 11. Final Status

```text
Notifications & Background Processing
                ↓
             COMPLETED
```

21/8/26


# 21-Aug-2026 — Friday

# Jira Story: Caching, API Performance & Advanced Backend Testing

## Objective

Combine the concepts learned during the week to improve backend performance,
reliability, security, and code quality.

---

# Task 1 — Understand Caching

## Definition

Caching is a technique used to temporarily store frequently requested data
in a fast storage system such as Redis.

Instead of requesting the same data from PostgreSQL every time, the application
can retrieve it from the cache.

## Flow

Database
    ↓
Cache
    ↓
API

## Cache Benefits

- Reduces database queries
- Improves API response time
- Reduces database load
- Improves application performance

## Example

Frequently requested data such as driver locations can be stored in Redis
and reused for a short period of time.

---

# Task 2 — Configure Redis Cache

## Definition

Redis is an in-memory data store that can be used as a caching system.

It stores frequently accessed data in memory, making data retrieval much
faster than querying the database repeatedly.

## Suitable APIs for Caching

- Nearby drivers
- Vehicle types
- Ride configuration
- Frequently accessed profile information

## Cache Configuration

The Django application was configured to use Redis as the cache backend.

## Example

```python
from django.core.cache import cache

cache.set("example_key", data, 300)

data = cache.get("example_key")
````

The value is stored for 300 seconds.

---

# Task 3 — Cache Nearby Drivers

## Definition

Nearby driver information can be requested frequently by passengers.
Caching this information reduces repeated database queries.

## Cache Strategy

```text
Nearby Drivers API
        ↓
Check Cache
        ↓
   Cache exists?
    /       \
  Yes        No
   ↓          ↓
Cache Hit   Database
              ↓
        Calculate Distance
              ↓
          Store in Cache
              ↓
           Response
```

## Cache Hit

A cache hit occurs when the requested data already exists in Redis.

```text
API Request
    ↓
Redis
    ↓
Data Found
    ↓
Cache HIT
    ↓
Response
```

## Cache Miss

A cache miss occurs when the requested data is not available in Redis.

```text
API Request
    ↓
Redis
    ↓
Data Not Found
    ↓
Cache MISS
    ↓
Database
    ↓
Store Data in Cache
    ↓
Response
```

## Cache Expiration

Cache expiration defines how long cached data remains valid.

Example:

```python
cache.set(cache_key, nearby_drivers, 60)
```

The cached nearby driver data expires after 60 seconds.

---

# Task 4 — Cache Invalidation

## Definition

Cache invalidation is the process of removing or updating outdated data
from the cache.

This is important when the underlying database data changes.

## Driver Location Update

```text
Driver Location Update
        ↓
Invalidate Old Cache
        ↓
Create / Refresh New Cache
        ↓
Updated Driver Information
```

## Why Cache Invalidation Is Required

Without invalidation, the API may return old driver locations or outdated
availability information.

## Example

When a driver's location changes:

```python
cache.delete(cache_key)
```

The next API request will fetch fresh information from the database and
store the updated result in Redis.

---

# Task 5 — API Performance Benchmark

## Definition

API performance benchmarking is the process of measuring and comparing
API performance before and after optimization.

## Comparison

```text
Without Cache
      vs
With Cache
```

## Metrics

The following metrics are measured:

* Response time
* Database query count
* Cache hits
* Cache misses

## Without Cache

```text
API
 ↓
PostgreSQL
 ↓
Response
```

Every request may require database queries.

## With Cache

```text
API
 ↓
Redis
 ↓
Response
```

When the cache contains the required data, the database query can be avoided.

## Expected Result

With caching:

* Response time should decrease
* Database queries should decrease
* Cache hits should increase
* Database load should decrease

---

# Task 6 — Complete Backend Test Suite

## Definition

A backend test suite is a collection of automated tests used to verify
that different parts of the application work correctly.

## Areas Tested

```text
Authentication
Profiles
Drivers
Vehicles
Rides
Fare
Location
Notifications
WebSockets
Permissions
```

## Positive Tests

Positive tests verify that valid requests produce the expected result.

Example:

```text
Valid JWT
    ↓
Authenticated API Request
    ↓
200 OK
```

## Negative Tests

Negative tests verify that invalid or unauthorized requests are handled
correctly.

Example:

```text
Invalid JWT
    ↓
401 Unauthorized
```

Another example:

```text
User A tries to access User B's ride
    ↓
403 Forbidden
```

## Testing Goals

* Verify correct functionality
* Detect bugs
* Verify error handling
* Verify permissions
* Prevent regressions

---

# Task 7 — Security Testing

## Definition

Security testing verifies that APIs and WebSocket connections cannot be
accessed or manipulated by unauthorized users.

## Security Tests

### Unauthorized API Access

Verify that protected APIs cannot be accessed without authentication.

```text
No JWT
    ↓
API Request
    ↓
401 Unauthorized
```

### Invalid JWT

Verify that invalid or expired JWT tokens are rejected.

```text
Invalid JWT
    ↓
API Request
    ↓
401 Unauthorized
```

### User Accessing Another User's Ride

Verify that users can access only their own rides.

```text
User A
  ↓
User B's Ride
  ↓
Access Denied
```

### Driver Accessing Another Driver's Data

Verify that drivers cannot access or modify another driver's information.

### Invalid WebSocket Connection

Verify that invalid WebSocket authentication or unauthorized connections
are rejected.

### Invalid Request Payloads

Test missing, invalid, or incorrect request values.

Example:

```text
Invalid Latitude
Invalid Longitude
Missing Required Field
Invalid Ride Status
```

### Excessive API Requests

Test whether APIs can handle excessive requests safely and determine
whether rate limiting or throttling is required.

## Security Goal

Every discovered security issue should be fixed and tested again.

---

# Task 8 — Final Weekly Code Review

## Definition

A final code review is the process of reviewing the complete backend
application to ensure that the code is clean, secure, maintainable,
and follows good development practices.

## Review Areas

### Architecture

Check whether the application structure is organized correctly and whether
business logic is separated from API views where appropriate.

### Naming

Check that classes, functions, variables, models, and files use clear
and meaningful names.

### Database Queries

Check for:

* Unnecessary queries
* N+1 query problems
* Missing select_related()
* Missing prefetch_related()
* Unnecessary database access

### API Responses

Check that APIs return consistent:

* Status codes
* Response formats
* Success messages
* Error messages

### Error Handling

Verify that expected errors are handled properly without exposing
unnecessary internal information.

### Security

Review:

* Authentication
* Authorization
* JWT validation
* Object-level permissions
* WebSocket authentication
* Input validation

### Logging

Verify that important application events and errors can be tracked
through appropriate logging.

### Tests

Check that important functionality has both positive and negative tests.

### Documentation

Verify that important APIs, architecture decisions, setup instructions,
and configuration details are documented.

### Git Commits

Review Git history to ensure commits are meaningful and changes are
properly tracked.

## Architectural Decision Review

Each major architectural decision should have a clear reason.

Examples:

### Redis

Redis was selected for caching because it provides fast in-memory data
access and helps reduce repeated database queries.

### Cache Expiration

A short cache expiration time is used for frequently changing driver
location data to reduce the chance of serving stale information.

### Database Optimization

`select_related()` is used where appropriate to reduce unnecessary
database queries for related objects.

### Background Processing

Background tasks are used for operations that do not need to block the
main API response.

---

# Acceptance Criteria

* Redis caching implemented
* Cache invalidation handled
* API performance benchmark completed
* Complete backend test suite created
* Positive and negative tests implemented
* Security testing completed
* Bugs identified and fixed
* Code reviewed and refactored
* Architecture documentation updated
* Git changes committed and pushed

---

# Key Concepts

| Concept            | Definition                                                      |
| ------------------ | --------------------------------------------------------------- |
| Cache              | Temporary storage for frequently accessed data                  |
| Redis              | In-memory data store commonly used for caching                  |
| Cache Hit          | Requested data is found in the cache                            |
| Cache Miss         | Requested data is not found in the cache                        |
| Cache Expiration   | Time after which cached data becomes invalid                    |
| Cache Invalidation | Removing or updating outdated cached data                       |
| Benchmark          | Measuring and comparing system performance                      |
| Positive Test      | Test using valid input and expected behavior                    |
| Negative Test      | Test using invalid input or unauthorized behavior               |
| Security Testing   | Testing the system for security vulnerabilities                 |
| Code Review        | Reviewing code for quality, security, and maintainability       |
| API Performance    | Measuring how quickly and efficiently an API responds           |
| N+1 Query          | Problem where one query causes many additional database queries |

---

# Final Outcome

The backend was reviewed and improved for:

* Performance
* Reliability
* Security
* Scalability
* Maintainability
* Testing
* Documentation
* Code quality

```
```




