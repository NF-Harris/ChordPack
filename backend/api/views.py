from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, NoteSerializer, ChordSerializer
from .models import Note, Chord
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from pgvector.django import CosineDistance 
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_song_embedding
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from django.utils.decorators import classonlymethod
from asgiref.sync import sync_to_async,async_to_sync
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .models import Chord
from .utils import clean_chordpro_format

from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Charge le fichier .env qui se trouve à la racine de ton projet backend
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Create your views here.

class CreateUserViews(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes ={IsAuthenticated}

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author = user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author = self.request.user)
        else:
            print(serializer.errors)

class NoteDelete(generics.DestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author = user)
    

class PublicChordList(generics.ListAPIView):
    """Affiche la liste de toutes les chansons publiques scrapées."""
    queryset = Chord.objects.filter(is_public=True, user__isnull=True)
    serializer_class = ChordSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20


class PublicChordDetail(generics.RetrieveAPIView):
    """Affiche le détail d'une chanson publique spécifique."""
    queryset = Chord.objects.filter(is_public=True, user__isnull=True)
    serializer_class = ChordSerializer
    permission_classes = [AllowAny]


# =======================================================
#  2. CARNET PRIVÉ (CRUD : Lecture, Création, Modification, Suppression)
# =======================================================

class UserChordListCreate(generics.ListCreateAPIView):
    """
    - GET : Affiche uniquement les chansons créées par l'utilisateur connecté.
    - POST : Permet à l'utilisateur connecté de créer une nouvelle chanson.
    """
    serializer_class = ChordSerializer
    permission_classes = [IsAuthenticated] # Exige un Token JWT valide
    filterset_class = ProductFilter
    

    def get_queryset(self):
        # L'utilisateur ne voit QUE ses propres chansons dans son carnet
        return Chord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_public=False)


class UserChordDetailUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    - GET : Voir le détail d'une de ses chansons privées.
    - PUT / PATCH : Modifier sa chanson (titre, accords...).
    - DELETE : Supprimer sa chanson.
    """
    serializer_class = ChordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Chord.objects.filter(user=self.request.user)




class VectorSearchChordView(APIView):
    """
    Endpoint appelé par n8n envoyant une chaîne de caractères brute 'query_text'.
    """

    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # 1. Sécurité : Vérification de la clé API
        token = request.headers.get('X_API_KEY')
        if token != os.environ.get('X_API_KEY'):
            print(f"DEBUG AUTH - Token reçu: '{token}' | Attendu: '{os.environ.get('X_API_KEY')}'", flush=True)
            raise AuthenticationFailed("Accès non autorisé.")

        # 2. Récupération du texte de recherche envoyé par n8n
        query_text = request.data.get('query_text')
        if not query_text:
            return Response({"error": "Le champ 'query_text' est requis."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 3. Génération de l'embedding de la question de l'utilisateur
        try:
            query_embedding = generate_song_embedding(query_text)
        except Exception as e:
            return Response({"error": f"Erreur lors de la génération de l'embedding OpenAI : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 4. Recherche par similarité cosinus avec pgvector
        # On ne prend que les morceaux qui ont un embedding et on garde les 5 plus proches
        results = Chord.objects.filter(embedding__isnull=False).annotate(
            distance=CosineDistance('embedding', query_embedding)
        ).order_by('distance')[:5]
        
        # 5. Structuration de la réponse JSON pour n8n
        data = []
        for chord in results:
            data.append({
                "id": chord.id,
                "title": chord.title,
                "artist": chord.artist or "Artiste inconnu",
                "content": chord.content, # Ton format ChordPro
                "score": round(1 - chord.distance, 4) # Plus proche de 1 = meilleure correspondance
            })
            
        return Response(data, status=status.HTTP_200_OK)


# =======================================================
# 3. Helpers pour l'accès asynchrone à la base de données
# =======================================================
# Django requiert que les opérations ORM soient exécutées dans un thread synchrone
@sync_to_async
def get_chord_or_none(pk):
    """Récupère l'accord en base de données de manière sécurisée."""
    try:
        # On s'assure que l'accord appartient bien à l'utilisateur connecté
        return Chord.objects.get(pk=pk)
    except Chord.DoesNotExist:
        return None

@sync_to_async
def save_chord_content(chord, new_content):
    """Sauvegarde le nouveau contenu nettoyé de l'accord."""
    chord.content = new_content
    chord.verified = True
    chord.save()
    return chord


# =======================================================
# 4. Vue Asynchrone pour la rectification
# =======================================================
class RectifyChordView(APIView):
    """
    Vue synchrone classique exécutant le nettoyage de manière sécurisée.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk, *args, **kwargs):
        # 1. Récupération du morceau
        chord = get_object_or_404(Chord, pk=pk)
        
        raw_content = chord.content
        if not raw_content:
            return Response(
                {"error": "Le contenu de la chanson est vide."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 2. Appel synchrone direct, plus de conflits de boucles !
            cleaned_content = clean_chordpro_format(raw_content)
        except Exception as e:
            return Response(
                {"error": f"Erreur lors du traitement par l'IA : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
                
        if not cleaned_content:
            return Response(
                {"error": "Le nettoyage a échoué. L'IA n'a retourné aucun contenu ou le quota est dépassé."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        if cleaned_content.strip() == raw_content.strip():
            chord.verified = True
            chord.save()
            return Response(ChordSerializer(chord).data, status=status.HTTP_200_OK)
        
        # 3. Sauvegarde
        chord.content = cleaned_content
        chord.verified = True
        chord.save()
        
        return Response(ChordSerializer(chord).data, status=status.HTTP_200_OK)