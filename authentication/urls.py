from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("register/", RegistrationView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("validate-username/",  csrf_exempt(UserNameValidationView.as_view()), name='validate-username'),
    path("validate-email/",  csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
    path("activate/<uidb64>/<token>", VerificationView.as_view(), name='activate'),
    path("request-reset-link/", RequestPasswordResetEmail.as_view(), name='request-password'),
    path('set-new-password/<uidb64>/<token>', ComplatePasswordReset.as_view(), name='reset-user-password')
]