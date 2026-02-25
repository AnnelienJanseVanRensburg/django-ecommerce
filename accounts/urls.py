from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password",
    ),
    path(
        "reset-password/<str:token>/",
        views.reset_password,
        name="reset_password",
    ),
]
