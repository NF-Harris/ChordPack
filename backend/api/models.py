from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField
from .utils import generate_song_embedding

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
    verified = models.BooleanField(default=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Null pour les morceaux publics
    created_at = models.DateTimeField(auto_now_add=True)
    embedding = VectorField(dimensions=768, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     # 1. On vérifie si c'est une création ou si un champ textuel a changé
    #     must_generate_embedding = False
        
    #     if self.pk is None:
    #         # C'est un nouveau morceau
    #         must_generate_embedding = True
    #     else:
    #         # Le morceau existe déjà, on compare avec la version en base de données
    #         orig = Chord.objects.get(pk=self.pk)
    #         if orig.title != self.title or orig.artist != self.artist or orig.content != self.content or orig.embedding is None:
    #             must_generate_embedding = True

    #     # 2. On génère l'embedding uniquement si nécessaire
    #     if must_generate_embedding:
    #         text_to_embed = f"Title: {self.title}. Artist: {self.artist}. Content: {self.content}"
    #         try:
    #             self.embedding = generate_song_embedding(text_to_embed)
    #         except Exception as e:
    #             print(f"Erreur lors de la génération de l'embedding: {e}")
                
    #     super().save(*args, **kwargs)
    

# Create your models here.
