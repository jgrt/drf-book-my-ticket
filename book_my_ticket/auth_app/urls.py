from django.urls import path, include

urlpatterns = [
    path("auth/rest-auth/", include("rest_auth.urls")),
    path("sign-up/rest-auth/registration/", include("rest_auth.registration.urls")),
]
