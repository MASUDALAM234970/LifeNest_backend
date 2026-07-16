LifeNest — Auth Module (Flutter / GetX)
This module implements the Sign In and Sign Up flow for the LifeNest
app, wired against the Django backend defined in `schema.yaml`
(`/api/users/*` endpoints). It uses GetX for state management and the
`http` package for networking — no `dio`.
Built for both backend and frontend devs to plug in without reverse-engineering
the code, so read this before touching auth.
---
Folder structure
```
lib/
├── data/
│   ├── models/
│   │   └── auth_models.dart      # request/response models (matches schema.yaml)
│   └── services/
│       ├── api_client.dart       # low-level HTTP client, token storage, 401 refresh
│       └── auth_service.dart     # one method per /api/users/* endpoint
└── app/
    └── controllers/
        └── auth_controller.dart  # GetX controller used by the UI screens
```
How the pieces fit together
```
UI (Sign In / Sign Up screens)
        │  calls
        ▼
AuthController (GetX)            — form state, validation, loading/error
        │  calls
        ▼
AuthService                      — one function per endpoint, builds request bodies
        │  calls
        ▼
ApiClient                        — adds JWT header, base URL, retries on 401
        │
        ▼
Django backend (/api/users/...)
```
---
For backend developers
Every request/response shape in `auth_models.dart` maps 1:1 to
`schema.yaml`. If the backend changes a field name, response shape, or
adds/removes a required field on any `/api/users/*` endpoint, update the
matching model in `auth_models.dart` — that's the single source of truth
on the app side.
Token flow assumed: `POST /users/login/` and `POST /users/signup/` return
`{ "access": "...", "refresh": "..." }`. `POST /users/token/refresh/`
takes `{ "refresh": "..." }` and returns a new `access` token. If the
actual response wraps this differently (e.g. nested under `"data"`),
update `TokenModel.fromJson` in `auth_models.dart`.
Errors are expected in DRF's default shape: `{"field": ["message"]}` or
`{"detail": "message"}`. `ApiException.message` in `api_client.dart`
parses this — if the backend uses a different error envelope, that's the
only place to change.
`date_of_birth` is sent as `"YYYY-MM-DD"` on signup.
For frontend developers
`AuthController.to` gives you the controller anywhere without manually
calling `Get.put()` — it self-registers on first use.
Fields already exposed and ready to bind to widgets:
Sign In: `loginEmailCtrl`, `loginPasswordCtrl`, `loginFormKey`,
`obscureLoginPassword`, `rememberMe`
Sign Up: `signupNameCtrl`, `signupEmailCtrl`, `signupPasswordCtrl`,
`signupConfirmPasswordCtrl`, `signupFormKey`, `dateOfBirth`,
`obscureSignupPassword`, `obscureConfirmPassword`, `agreeToTerms`
Shared: `isLoading`, `errorMessage`
Actions to call from buttons: `login()`, `signup()`,
`continueWithFirebase(token)`, `requestPasswordReset(email)`,
`verifyPasswordResetOtp(email, otp)`,
`confirmPasswordReset(email, password, confirmPassword)`, `logout()`.
All of the above are `Future<void>` or `Future<bool>` — `await` them and
read `isLoading`/`errorMessage` (both `Rx`, so wrap in `Obx`) to drive
the UI.
On success, `login()` / `signup()` / `continueWithFirebase()` already
navigate to `RoutesName.home` via `Get.offAllNamed`. On failure they show
a `Get.snackbar` automatically — you don't need to handle that yourself.
---
Setup checklist
Add to `pubspec.yaml`:
```yaml
   dependencies:
     http: ^1.2.0
     get_storage: ^2.1.1
     get: ^4.6.6
   ```
In `api_client.dart`, replace the placeholder:
```dart
   static const String baseUrl = 'https://api.lifenest.app/api';
   ```
with the real backend URL.
In `auth_controller.dart`, fix the import path for `RoutesName` to match
this project's actual routes file:
```dart
   import '../routes/routes_name.dart';
   ```
Make sure `GetStorage.init()` is called once in `main()` before
`runApp()`, since both `ApiClient` and `AuthController` read/write to it.
Known assumptions / things to confirm
[ ] Confirm the `TokenModel` shape (`access` / `refresh`) matches the real
login/signup response.
[ ] Confirm the error response shape backend actually returns.
[ ] `RoutesName.home` and `RoutesName.login` must exist in the project's
route table.
[ ] Firebase token retrieval (Google/Apple sign-in) is not included
here — only the backend call after you already have a Firebase ID
token. Wire up `firebase_auth` / `google_sign_in` / `sign_in_with_apple`
separately and pass the resulting token into
`AuthController.continueWithFirebase(token)`.
