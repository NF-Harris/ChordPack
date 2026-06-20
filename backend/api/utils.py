import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Charge le fichier .env qui se trouve à la racine de ton projet backend
load_dotenv(os.path.join(BASE_DIR, '.env'))


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_song_embedding(text):
    """Génère un vecteur d'embedding à partir d'un texte."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding