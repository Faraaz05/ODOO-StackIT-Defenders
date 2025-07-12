from django.db import models
from django.conf import settings

class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()  # Will store HTML from rich text editor
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200)  # Comma-separated tags for simplicity

    def __str__(self):
        return self.title