from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """What fields show in the admin list"""
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff"
        )
    fieldsets = UserAdmin.fieldsets + (
        ("Role Info", {"fields": ("role",)}),
    )
