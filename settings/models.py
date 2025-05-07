from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:30]}...'

class Settings(models.Model):
    site_name = models.CharField(max_length=100, default="My Site")
    site_description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name_plural = "Settings"
