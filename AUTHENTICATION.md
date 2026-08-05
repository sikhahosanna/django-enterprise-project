# Authentication Documentation

## Overview
This project implements JWT Authentication using Django REST Framework and Simple JWT.

## Features
- User Registration API
- User Login API
- JWT Authentication
- Profile API
- Change Password API
- Logout API with Token Blacklist

## API Endpoints

### Register
POST /api/register/

### Login
POST /api/login/

### Profile
GET /api/profile/

### Change Password
POST /api/change-password/

### Logout
POST /api/logout/

## JWT Authentication

Login API returns:

- Access Token
- Refresh Token

Protected APIs require:

Authorization:
Bearer <access_token>

## Logout

Logout blacklists the refresh token so it cannot be reused.