from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, NoteSerializer, ChordSerializer
from .models import Note, Chord
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination

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
