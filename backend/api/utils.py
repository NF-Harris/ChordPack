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


# =======================================================
# 1. Configuration Initiale (Variables d'environnement)
# =======================================================
# Clé API Google pour Gemini (Gratuit via AI Studio)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialisation du module Google si la clé est présente
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


# =======================================================
# 2. Fonction de Rectification Directe via Gemini (Python)
# =======================================================
def clean_chordpro_format(bad_chordpro_text):
    """
    Version SYNCHRONE avec la syntaxe google-generativeai classique.
    """
    
    # 2. Initialisation du modèle
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = (
    r"Tu es un outil de nettoyage de notation musicale ChordPro. Ton rôle unique est de vérifier et corriger les accords entre crochets [ ] :"
    r"\n1. Un crochet de sustain ou de liaison au milieu des paroles est valide s'il contient uniquement des vrais noms d'accords reliés par des symboles de rythme (ex valides : [F#m....], [G-Am7-------------G/B])."
    r"\n2. RÈGLE DES DIAGRAMMES ET DICTIONNAIRES D'ACCORDS : Si un crochet contient des diagrammes de positions de doigts ou des tablatures numériques (comme [x32310], [133111]), ou des en-têtes (comme [Capo:], [C7:]), tu dois sortir tout cela des crochets. De plus, si plusieurs définitions d'accords sont écrasées ou mal formatées, sépare-les proprement pour qu'on ait chaque accord avec sa tablature associée de manière lisible (ex: 'C7: x32310' et 'Fm: 133111' séparés par un espace ou un retour à la ligne)."
    r"\nPar exemple : '[C7:]Fm: [x32310]133111' doit être corrigé proprement en : 'C7: x32310 \nFm: 133111' (ou séparé par un espace clair)."
    r"\n3. Si du texte de parole ou une tablature est coincé dans ou juste après un crochet au milieu du chant, sépare-le proprement."
    r"\n4. RÈGLE DES LIGNES INSTRUMENTALES (Solo, Intro, Sioka, etc.) : Si une ligne ou une section ne contient pas de paroles mais uniquement des noms d'accords ou des symboles (ex: |, ||, -), enlève tous les crochets de cette ligne. Ne rajoute jamais de crochets là où il n'y en a pas."
    r"\nNe touche pas aux lignes de texte avec paroles chantées où les accords sont bien positionnés."
    r"\nRenvoie UNIQUEMENT le texte corrigé, sans commentaires, sans bloc de code markdown."
    r"\n\nTexte à corriger :\n" + bad_chordpro_text
)
    
    try:
        # 3. Appel synchrone classique
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erreur lors de l'appel Gemini direct synchrone : {e}")
        return None
    

