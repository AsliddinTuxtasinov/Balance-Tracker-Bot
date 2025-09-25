import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.user.enums import UserRolesChoices, AuthStatusChoices
from apps.user.managers import CustomUserManager
from core.base.base_models import BaseModel


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)

    user_roles = models.CharField(max_length=35, choices=UserRolesChoices.choices, default=UserRolesChoices.CLIENT)
    auth_status = models.CharField(max_length=35, choices=AuthStatusChoices.choices, default=AuthStatusChoices.NEW)

    telegram_id = models.BigIntegerField(unique=True, db_index=True, null=True, blank=True)

    is_staff = models.BooleanField(
        _("staff status"), default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"), default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    def check_pass(self):
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    def clean(self):
        self.check_pass()
        self.hashing_password()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number

    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
