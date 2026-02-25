from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Store additional profile information for each user."""
    ACCOUNT_TYPES = [
        ("vendor", "Vendor"),
        ("buyer", "Buyer"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPES,
    )

    def __str__(self):
        """Return a string representation of the UserProfile."""
        return f"{self.user.username} - {self.account_type}"


class ResetToken(models.Model):
    """Store password reset tokens with expiry times."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        """Return a string representation of the ResetToken."""
        return f"Reset token for {self.user.username}"

    def is_expired(self):
        """Return True if the token has passed its expiry date."""
        from django.utils import timezone

        return timezone.now() > self.expiry_date
