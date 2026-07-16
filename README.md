# Users & Authentication API

A REST API for user authentication and account management — built with **Django REST Framework** (based on `drf-spectacular` schema generation) and **JWT** authentication (via `djangorestframework-simplejwt`).

This document explains all available endpoints, request/response shapes, and auth rules so both backend and frontend developers can work independently without confusion.

---

## Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Endpoints Summary](#endpoints-summary)
- [Endpoint Details](#endpoint-details)
  - [Signup](#1-signup)
  - [Login](#2-login)
  - [Firebase Auth (Google/Apple)](#3-firebase-auth-googleapple-login)
  - [Logout](#4-logout)
  - [Token Refresh](#5-token-refresh)
  - [Token Verify](#6-token-verify)
  - [Profile (Get / Update)](#7-profile-get--update)
  - [Password Change](#8-password-change)
  - [Password Reset Request](#9-password-reset-request)
  - [Password Reset OTP Verify](#10-password-reset-otp-verify)
  - [Password Reset Confirm](#11-password-reset-confirm)
  - [Resend OTP](#12-resend-otp)
  - [Verify OTP](#13-verify-otp-signup-verification)
  - [Account Delete](#14-account-delete)
  - [Schema](#15-api-schema)
- [Data Models (Schemas)](#data-models-schemas)
- [Notes for Frontend Developers](#notes-for-frontend-developers)
- [Notes for Backend Developers](#notes-for-backend-developers)

---

## Overview

This API handles:
- 📝 User registration (signup) with OTP email verification
- 🔐 Login with email + password
- 🔥 Social login via Firebase (Google / Apple)
- 🔄 JWT access/refresh token management
- 👤 User profile retrieval and update
- 🔑 Password change & password reset (OTP-based)
- ❌ Account deletion

## Base URL

```
/api/
```

All routes below are relative to this base (e.g. `/api/users/login/`).

## Authentication

This API uses **JWT (JSON Web Token)** authentication.

| Security Scheme | Type | How it's sent |
|---|---|---|
| `jwtAuth` | Bearer Token | `Authorization: Bearer <access_token>` header |
| `cookieAuth` | Session Cookie | `sessionid` cookie (used mainly for the schema endpoint) |
| `basicAuth` | HTTP Basic | Username/password (used mainly for the schema endpoint) |

**Flow:**
1. User signs up or logs in → receives `access` and `refresh` tokens.
2. Send `access` token in the `Authorization` header for protected routes.
3. When `access` token expires, use the `refresh` token to get a new one via `/api/users/token/refresh/`.
4. On logout, the `refresh` token is blacklisted server-side.

🔓 **Public endpoints** (no token required): signup, login, firebase-auth, password reset flow, resend-otp, verify-otp, schema.

🔒 **Protected endpoints** (JWT required): profile, password-change, logout, account-delete.

---

## Endpoints Summary

| # | Method | Endpoint | Auth Required | Description |
|---|--------|----------|:---:|---|
| 1 | POST | `/api/users/signup/` | ❌ | Register a new user |
| 2 | POST | `/api/users/login/` | ❌ | Login with email & password |
| 3 | POST | `/api/users/firebase-auth/` | ❌ | Login/signup via Firebase (Google/Apple) |
| 4 | POST | `/api/users/logout/` | ✅ | Logout & blacklist refresh token |
| 5 | POST | `/api/users/token/refresh/` | ❌ | Get a new access token |
| 6 | POST | `/api/users/token/verify/` | ❌ | Verify a token's validity |
| 7 | GET/PUT/PATCH | `/api/users/profile/` | ✅ | View / update profile |
| 8 | POST | `/api/users/password-change/` | ✅ | Change password (logged-in user) |
| 9 | POST | `/api/users/password-reset/` | ❌ | Request password reset OTP |
| 10 | POST | `/api/users/password-reset-otp-verify/` | ❌ | Verify OTP for password reset |
| 11 | POST | `/api/users/password-reset-confirm/` | ❌ | Set new password after OTP verification |
| 12 | POST | `/api/users/resend-otp/` | ❌ | Resend OTP code |
| 13 | POST | `/api/users/verify-otp/` | ❌ | Verify OTP (e.g. after signup) |
| 14 | DELETE | `/api/users/account-delete/` | ✅ | Permanently delete account |
| 15 | GET | `/api/schema/` | Public | Raw OpenAPI schema (JSON/YAML) |

---

## Endpoint Details

### 1. Signup
Register a new user account.

```
POST /api/users/signup/
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "date_of_birth": "2000-05-14",
  "password": "StrongPass1!",
  "confirm_password": "StrongPass1!"
}
```

| Field | Type | Required | Notes |
|---|---|:---:|---|
| `name` | string | ✅ | Max 150 chars |
| `email` | string (email) | ✅ | Used for login, max 255 chars |
| `date_of_birth` | string (date, `YYYY-MM-DD`) | ✅ | Nullable |
| `password` | string | ✅ | Min 8 chars, must include uppercase, lowercase, number & special char |
| `confirm_password` | string | ✅ | Must match `password` |

**Response `200`:** Returns the created user object (password fields are write-only, never returned).

> ℹ️ Likely triggers an OTP email — pair with [Verify OTP](#13-verify-otp-signup-verification).

---

### 2. Login
Authenticate with email and password.

```
POST /api/users/login/
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "StrongPass1!"
}
```

**Response `200`:** User/token data (exact shape defined by your `UserLogin` serializer output — typically includes `access` and `refresh` tokens).

---

### 3. Firebase Auth (Google/Apple login)
Authenticate using a Firebase ID token (social login).

```
POST /api/users/firebase-auth/
```

**Request Body:**
```json
{
  "firebase_token": "<firebase_id_token>",
  "name": "John Doe",
  "date_of_birth": "2000-05-14"
}
```

| Field | Type | Required | Notes |
|---|---|:---:|---|
| `firebase_token` | string | ✅ | ID token from Firebase client SDK |
| `name` | string | ❌ | Optional — falls back to Firebase profile data |
| `date_of_birth` | string (date) | ❌ | Optional |

**Response `200`:** Authenticated user data + tokens.

---

### 4. Logout
Logs the user out by blacklisting their refresh token.

```
POST /api/users/logout/
Authorization: Bearer <access_token>
```

**Response `200`:** No response body.

---

### 5. Token Refresh
Exchange a valid `refresh` token for a new `access` token.

```
POST /api/users/token/refresh/
```

**Request Body:**
```json
{ "refresh": "<refresh_token>" }
```

**Response `200`:**
```json
{ "access": "<new_access_token>" }
```

---

### 6. Token Verify
Check whether a token is still valid.

```
POST /api/users/token/verify/
```

**Request Body:**
```json
{ "token": "<access_or_refresh_token>" }
```

**Response `200`:** Empty object if valid; `401` if invalid/expired.

---

### 7. Profile (Get / Update)
Retrieve or update the authenticated user's profile.

```
GET   /api/users/profile/     — Get profile
PUT   /api/users/profile/     — Full update
PATCH /api/users/profile/     — Partial update
Authorization: Bearer <access_token>
```

**Response `200`:** No body schema defined in the source spec — confirm the actual returned fields (likely `name`, `email`, `date_of_birth`, etc.) with the backend team.

---

### 8. Password Change
Change password while logged in.

```
POST /api/users/password-change/
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "old_password": "OldPass1!",
  "new_password": "NewPass1!",
  "confirm_password": "NewPass1!"
}
```

All three fields are **required**.

---

### 9. Password Reset Request
Start the "forgot password" flow — sends an OTP to the user's email.

```
POST /api/users/password-reset/
```

**Request Body:**
```json
{ "email": "john@example.com" }
```

---

### 10. Password Reset OTP Verify
Verify the OTP sent for password reset.

```
POST /api/users/password-reset-otp-verify/
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

`otp` — max length 6.

---

### 11. Password Reset Confirm
Set a new password after OTP has been verified.

```
POST /api/users/password-reset-confirm/
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "NewPass1!",
  "confirm_password": "NewPass1!"
}
```

---

### 12. Resend OTP
Resend an OTP code (e.g. if the user didn't receive it).

```
POST /api/users/resend-otp/
```

**Request Body:**
```json
{ "email": "john@example.com" }
```

---

### 13. Verify OTP (signup verification)
Verify an OTP code, typically used to confirm signup / email ownership.

```
POST /api/users/verify-otp/
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "otp": "123456"
}
```

---

### 14. Account Delete
Permanently delete the authenticated user's account.

```
DELETE /api/users/account-delete/
Authorization: Bearer <access_token>
```

**Response `204`:** No response body. ⚠️ This action is irreversible.

---

### 15. API Schema
Raw OpenAPI schema for this API, useful for generating clients (Swagger, Postman, etc.).

```
GET /api/schema/?format=json|yaml&lang=<language_code>
```

Supports content negotiation for `application/json`, `application/yaml`, `application/vnd.oai.openapi`, and `application/vnd.oai.openapi+json`. Also supports an optional `lang` query param for localized schema descriptions (many language codes supported, e.g. `en`, `bn` is not listed — see raw schema for the full list).

---

## Data Models (Schemas)

| Model | Key Fields |
|---|---|
| `UserRegistration` | `name`, `email`, `date_of_birth`, `password`*, `confirm_password`* |
| `UserLogin` | `email`, `password`* |
| `FirebaseAuth` | `firebase_token`*, `name`, `date_of_birth` |
| `PasswordChange` | `old_password`*, `new_password`*, `confirm_password`* |
| `PasswordResetRequest` | `email` |
| `PasswordResetOTPVerify` | `email`, `otp` |
| `PasswordResetConfirm` | `email`, `password`*, `confirm_password`* |
| `ResendOTP` | `email` |
| `VerifyOTP` | `email`, `otp` |
| `TokenRefresh` | `access` (read-only), `refresh` |
| `TokenVerify` | `token`* |

`*` = write-only field (never returned in API responses, only accepted as input).

---

## Notes for Frontend Developers

- Store `access` and `refresh` tokens securely (e.g. httpOnly cookie or secure storage — avoid plain `localStorage` for sensitive apps).
- Attach `Authorization: Bearer <access_token>` to every protected request.
- When you get a `401`, try `/api/users/token/refresh/` once; if that also fails, redirect to login.
- Password field must satisfy: **min 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character.**
- OTP fields are always 6 characters or fewer.
- The `/api/users/profile/` response body isn't fully documented in the schema — coordinate with backend to confirm exact field names before building the profile UI.

## Notes for Backend Developers

- Several endpoints (`profile`, `resend-otp`, `verify-otp`, `password-reset-otp-verify`) are missing `description` fields or full response schemas in the OpenAPI spec — consider adding `drf-spectacular` docstrings/annotations so this README (and any auto-generated client) stays accurate.
- `TokenRefresh.access` is `readOnly`, confirming it's only ever a response field, not input.
- Consider adding explicit response schemas for `profile` GET/PUT/PATCH so frontend doesn't have to guess field names.

---

*This README was generated from the project's OpenAPI (`schema.yaml`) specification. Keep it in sync by regenerating whenever the schema changes.*
