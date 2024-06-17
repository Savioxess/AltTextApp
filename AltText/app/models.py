from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class SavedTexts(models.Model):
    text_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.text_id} - {self.filename}'