

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

<<<<<<< HEAD
=======



>>>>>>> bdcf3c9 (Complete ride management tasks)
