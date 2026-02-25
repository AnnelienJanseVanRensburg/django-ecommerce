from django.contrib import admin
from .models import UserProfile, ResetToken

admin.site.register(UserProfile)
admin.site.register(ResetToken)
