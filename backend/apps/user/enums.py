from django.db import models


class AuthStatusChoices(models.TextChoices):
    NEW = "new", "new"
    CODE_VERIFIED = "code_verified", "code_verified"
    DONE = "done", "done"


class UserRolesChoices(models.TextChoices):
    CLIENT = "client", "client"
    ADMIN = "admin", "admin"
