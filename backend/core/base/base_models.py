# Base model class that provides common fields and functionalities for other models to inherit from
import uuid
from django.utils.translation import gettext_lazy as _

from django.db import models


class BaseModel(models.Model):
    # Unique identifier for each instance of the model
    id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, primary_key=True)

    # DateTimeField that automatically stores the creation time of an instance when
    # it is first saved to the database
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created_at"))

    # DateTimeField that automatically updates with the current time whenever
    # the instance is saved or updated in the database
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated_at"))

    class Meta:
        # Specifies that this model is abstract, meaning it won't be created as a separate table in the database
        abstract = True
