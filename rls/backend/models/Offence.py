import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Offence(models.Model):

    offence_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    commited_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(null = False, blank = False, max_length = 100)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "penalties")
