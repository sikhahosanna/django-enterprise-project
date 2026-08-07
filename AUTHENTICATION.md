
```markdown
# Authentication Documentation

## Overview

This project implements a secure JWT-based authentication system using Django REST Framework and Simple JWT.

The authentication module provides secure user registration, login, authorization, password management, and logout functionality.

---

# Authentication Features

The system supports the following features:

- User Registration API
- Email Based Login API
- JWT Access Token Generation
- JWT Refresh Token Generation
- Protected API Authentication
- Change Password API
- Logout API with Token Blacklist
- API Testing and Documentation

---

# API Endpoints

## 1. Register API

### Method

POST


### Endpoint

```

/api/register/

````


### Purpose

Creates a new user account in the application.


### Request Body

```json
{
    "email": "siri@gmail.com",
    "password": "Siri@12345"
}
````

### Response Example

```json
{
    "message": "User registered successfully"
}
```

### Validation

The API validates:

* Email format
* Required fields
* Duplicate email
* Password strength

---

# 2. Login API

### Method

POST

### Endpoint

```
/api/login/
```

### Purpose

Authenticates users using email and password.

### Request Body

```json
{
    "email": "siri@gmail.com",
    "password": "Siri@12345"
}
```

### Response Contains

* User details
* Access Token
* Refresh Token

### Response Example

```json
{
    "user": {
        "email": "siri@gmail.com"
    },
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
}
```

---

# 3. Profile API

### Method

GET

### Endpoint

```
/api/profile/
```

### Purpose

Retrieves authenticated user profile information.

### Authorization Header

```
Authorization: Bearer <access_token>
```

### Security

Only authenticated users with valid JWT tokens can access this API.

---

# 4. Change Password API

### Method

POST

### Endpoint

```
/api/change-password/
```

### Purpose

Allows authenticated users to securely update their password.

### Request Body

```json
{
    "current_password": "OldPassword",
    "new_password": "NewPassword"
}
```

### Validation

The API verifies:

* Current password correctness
* New password strength
* Secure password hashing

---

# 5. Logout API

### Method

POST

### Endpoint

```
/api/logout/
```

### Purpose

Securely logs out users by invalidating refresh tokens.

### Request Body

```json
{
    "refresh": "refresh_token"
}
```

### Logout Process

```
User Logout

     |

Refresh Token

     |

Token Blacklist

     |

Token Cannot Be Used Again
```

After logout, the refresh token is blacklisted and cannot be reused.

---

# JWT Authentication Flow

```
User Registration

        |

        v

User Account Created

        |

        v

User Login

        |

        v

JWT Access + Refresh Token Generated

        |

        v

Access Protected APIs

        |

        v

Password Change / Logout

        |

        v

Secure User Session Management
```

---

# Security Implementation

Implemented security practices:

* JWT Token Authentication
* Password Hashing
* Password Validation
* Token Blacklisting
* Protected API Access
* Secure User Session Handling

---

# Testing Completed

Verified:

* Successful registration
* Duplicate email validation
* Invalid credentials handling
* JWT token generation
* Protected API access
* Password update validation
* Logout token blacklist functionality

---

# Documentation Status

Completed:

✅ Authentication APIs
✅ JWT Configuration
✅ API Request Examples
✅ API Response Examples
✅ Security Flow Documentation
✅ Testing Documentation

---

# Git Commit

Save authentication documentation:

```bash
git add AUTHENTICATION.md

git commit -m "Updated authentication documentation"

git push origin main
```

```

