from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password", "telegram_id")}),
        (
            _("User Information"),
            {
                "fields": ("user_roles", "full_name", "auth_status")
            },
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (
            _("Important dates"),
            {
                "fields": ("last_login",)
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )
    list_display = ["phone_number", "user_roles", "full_name", "telegram_id", "is_active", "is_staff"]
    search_fields = ["full_name", "phone_number"]
    list_filter = ("user_roles", "is_active", "groups")
    readonly_fields = ["telegram_id"]
    ordering = ["-created_at"]
