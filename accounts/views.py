from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
import hashlib
import secrets
import datetime
from .models import UserProfile, ResetToken


def register_user(request):
    """Handle user registration for both vendors and buyers."""
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        account_type = request.POST.get("account_type")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "accounts/register.html")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        UserProfile.objects.create(
            user=user,
            account_type=account_type,
        )

        group = Group.objects.get(name=account_type)
        user.groups.add(group)

        login(request, user)
        return redirect("store_list")

    return render(request, "accounts/register.html")


def login_user(request):
    """Handle user login and session creation."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("store_list")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "accounts/login.html")

    return render(request, "accounts/login.html")


def logout_user(request):
    """Log out the current user and redirect to login page."""
    logout(request)
    return redirect("login")


def forgot_password(request):
    """Handle forgotten password requests by sending a reset email."""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email")
            return render(request, "accounts/forgot_password.html")

        raw_token = secrets.token_urlsafe(32)
        hashed_token = hashlib.sha1(raw_token.encode()).hexdigest()

        expiry = timezone.now() + datetime.timedelta(minutes=5)

        ResetToken.objects.create(
            user=user,
            token=hashed_token,
            expiry_date=expiry,
        )

        reset_url = (
            f"http://localhost:8000/accounts/reset-password/{raw_token}/"
        )

        email_message = EmailMessage(
            subject="Password Reset Request",
            body=f"Click the link to reset your password: {reset_url}",
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email_message.send()

        messages.success(request, "Password reset link sent to your email")
        return redirect("login")

    return render(request, "accounts/forgot_password.html")


def reset_password(request, token):
    """Validate a reset token and allow the user to set a new password."""
    hashed_token = hashlib.sha1(token.encode()).hexdigest()

    try:
        reset_token = ResetToken.objects.get(
            token=hashed_token,
            used=False,
        )
    except ResetToken.DoesNotExist:
        messages.error(request, "Invalid or expired link")
        return redirect("login")

    if reset_token.is_expired():
        reset_token.delete()
        messages.error(request, "Reset link has expired")
        return redirect("forgot_password")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(
                request,
                "accounts/reset_password.html",
                {"token": token},
            )

        reset_token.user.set_password(password)
        reset_token.user.save()
        reset_token.delete()

        messages.success(request, "Password reset successful, please log in")
        return redirect("login")

    return render(
        request,
        "accounts/reset_password.html",
        {"token": token},
    )
