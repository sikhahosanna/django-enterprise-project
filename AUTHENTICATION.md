# Authentication Documentation

## Overview

This project implements JWT Authentication using Django REST Framework and Simple JWT.

## Authentication Features

- User Registration API
- User Login API
- JWT Access Token and Refresh Token
- Protected Profile API
- Change Password API
- Logout API with Token Blacklist

## API Endpoints

## 1. Register API

Method:
POST

Endpoint:

/api/register/

Request:

```json
{
    "email": "siri@gmail.com",
    "password": "Siri@12345"
}
2. Login API

Method:
POST

Endpoint:

/api/login/

Login response contains:

Access Token
Refresh Token
3. Profile API

Method:
GET

Endpoint:

/api/profile/

Authorization:

Bearer <access_token>
4. Change Password API

Method:
POST

Endpoint:

/api/change-password/

Request:

{
    "current_password": "OldPassword",
    "new_password": "NewPassword"
}
5. Logout API

Method:
POST

Endpoint:

/api/logout/

Request:

{
    "refresh": "refresh_token"
}

After logout, the refresh token will be blacklisted and cannot be reused.

JWT Authentication Flow
User registers using Register API.
User logs in and receives JWT tokens.
Access token is used for protected APIs.
Logout API blacklists the refresh token.

Tarvata save chesi:

```powershell
git add AUTHENTICATION.md
git commit -m "Updated authentication documentation"
git push origin main