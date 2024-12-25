from django.db import models
from django.contrib.auth.models import User
class GeneratedText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_texts')
    url = models.URLField(max_length=200)
    text = models.TextField()
    title = models.CharField(max_length=200, default="Untitled")  # Set a default value here

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Generated Text for {self.user.username} on {self.url}"

