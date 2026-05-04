from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "avatar",
        "is_staff",
        "is_active",
        "date_joined",
        "is_superuser",
        "phone_number",
        "city",
    )
    search_fields = (
        "username",
        "email",
        "phone_number",
    )
    list_filter = ("email",)
    search_fields = (
        "username",
        "email",
    )
