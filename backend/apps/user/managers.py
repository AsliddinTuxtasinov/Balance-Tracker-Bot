import re

from django.contrib.auth.base_user import BaseUserManager

from apps.user.enums import UserRolesChoices


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError('The phone_number must be set')

        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number=phone_number, password=password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_roles', UserRolesChoices.ADMIN)
        return self._create_user(phone_number=phone_number, password=password, **extra_fields)

    @classmethod
    def normalize_phone_number(cls, phone_number):
        """
        Normalize a phone number by removing all non-numeric characters.

        This method ensures that only digits remain in the phone number,
        making it easier to store, compare, or validate. It does not
        add a country code, enforce length, or check compliance with
        the E.164 format — it only strips non-digit characters.

        Args:
            phone_number (str | None):
                The raw phone number string, which may contain spaces,
                dashes, parentheses, or other non-numeric characters.
                If None is provided, it will be treated as an empty string.

        Returns:
            str:
                The normalized phone number containing digits only.

        Example:
            "(90) 123-45-67" -> "901234567"; "+998 90 123 45 67" -> "998901234567"; None -> ""
        """
        phone_number = phone_number or ""
        # Remove non-numeric characters
        phone_number = re.sub(r"\D", "", phone_number)
        return phone_number
