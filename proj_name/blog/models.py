from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 'cascade' <- if user is deleted, we want to delete their posts as well

    f""" Note
    For DateTimeField arguments:
        - auto_now      (bool) = allows to get current time on EVERY UPDATE
        - auto_now_add  (bool) = allows to get current time on CREATE but DISABLES modification
    """

    def __str__(self) -> str:
        return self.title