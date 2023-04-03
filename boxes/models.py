from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Box(models.Model):
    length = models.DecimalField(max_digits=10, decimal_places=2)
    breadth = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(
        max_digits=10, decimal_places=2)
    created_by = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Box ({self.length} x {self.breadth} x {self.height})"
