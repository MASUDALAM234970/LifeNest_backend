from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    FirebaseAuthView,
    VerifyOTPView,
    ResendOTPView,
    PasswordResetRequestView,
    PasswordResetOTPVerifyView,
    PasswordResetConfirmView,  # Add this import
    PasswordChangeView,
    UserProfileView,
    AccountDeleteView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
)

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('firebase-auth/', FirebaseAuthView.as_view(), name='firebase-auth'),
    
    # Token management
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token-verify'),
    
    # OTP verification
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    
    # Password management
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-otp-verify/', PasswordResetOTPVerifyView.as_view(), name='password-reset-otp-verify'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    
    # Profile management
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('account-delete/', AccountDeleteView.as_view(), name='account-delete'),
]