import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "profile")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)