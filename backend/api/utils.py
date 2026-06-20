import os
from dotenv import load_dotenv
from pathlib import Path
import google.generativeai as genai

load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Charge le fichier .env qui se trouve à la racine de ton projet backend
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Configuration de l'API Gemini (Gratuite via Google AI Studio)
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def generate_song_embedding(text):
    """
    Génère un vecteur d'embedding de 768 dimensions gratuitement
    avec le modèle text-embedding-004 de Google.
    """
    if not api_key:
        raise ValueError("La variable d'environnement GEMINI_API_KEY n'est pas configurée.")
    
    # Appel au modèle d'embedding gratuit de Google
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"
    )
    
    # Retourne la liste de 768 nombres
    return response['embedding']