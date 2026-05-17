from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, UserPayment


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "pk",
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


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "payment_date",
        "payment_course",
        "payment_lesson",
        "payment",
        "payment_method",
    )
    search_fields = (
        "user",
        "payment",
    )
    list_filter = ("payment",)


