from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

class Chord(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    is_public = models.BooleanField(default=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Null pour les morceaux publics
    created_at = models.DateTimeField(auto_now_add=True)
    

# Create your models here.
