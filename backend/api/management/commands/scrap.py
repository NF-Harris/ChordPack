from django.core.management.base import BaseCommand
from api.models import Chord
from bs4 import BeautifulSoup
import requests
import re

acousticGasyurl = "https://acousticgasy.com/mpihira/"

def GetMpihira(mpihiraUrl):
    response = requests.get(mpihiraUrl)
    soup = BeautifulSoup(response.text, "html.parser")

    divs = soup.find_all("div", class_="entry-content" )

    singer_link = []

    for div in divs:
        links = div.find_all("a", href=True)
        for link in links:
            if "https://acousticgasy.com/mpihira/" in link["href"] and not("share" in link["href"]):
                singer_link.append(link["href"])

    return singer_link

def GetSongUrl(singer_link):

    songs_link = []
    for link in singer_link:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.find_all("div", class_="entry-content" )

        for div in divs:
            links = div.find_all("a", href=True)
            for link in links:
                if not"https://acousticgasy.com/mpihira/" in link["href"]:
                    songs_link.append(link["href"])

    return songs_link



def acousticGasySerializer(soup):

    bloc = soup.find('pre')

    if bloc:
        # 0. ETAPE CRUCIALE : On trouve tous les <br/> et on les remplace par "\n"
        for br in bloc.find_all("br"):
            br.replace_with("\n")

        # 1. On sépare le texte ligne par ligne en gardant tout brut
        lignes = bloc.get_text(strip=False).replace("\xa0", " ").split('\n')
        
        # Nettoyage des lignes vides au début ou à la fin
        lignes = [l for l in lignes if l.strip() or l == ""]

        chanson_chordpro = []
        
        # 2. On parcourt les lignes deux par deux (Ligne d'accords, puis Ligne de paroles)
        i = 0
        while i < len(lignes):
            ligne_actuelle = lignes[i]

            ignore = False
            ignoreList = ["Chorus","Verse","Intro", "Tondrompeon","Tonony","Fiverenana","Key","Tonalite"]
            for ing in ignoreList:
                if ing in ligne_actuelle:
                    ignore = True
                    break
            
            # S'il s'agit d'une ligne vide ou d'un titre de section (ex: "Chorus #1")
            if not ligne_actuelle.strip() or ignore:
                chanson_chordpro.append(ligne_actuelle.strip())
                i += 1
                continue
                
            # On vérifie si la ligne suivante existe
            if i + 1 < len(lignes):
                ligne_suivante = lignes[i + 1]
                
                # Détection : Si la ligne actuelle contient des accords (beaucoup d'espaces)
                # et la suivante ressemble à des paroles
                if len(re.findall(r'[A-G][#b]?[m0-9]?[^\s]*', ligne_actuelle)) > 0:
                    
                    # --- ALGORITHME DE FUSION EN CHORDPRO ---
                    accords_trouves = []
                    # On trouve chaque accord et sa position exacte (index de début)
                    for match in re.finditer(r'\S+', ligne_actuelle):
                        accord = match.group()
                        index = match.start()
                        accords_trouves.append((index, accord))
                    
                    # On trie les accords du plus grand index au plus petit (très important pour ne pas décaler la chaîne en insérant)
                    accords_trouves.sort(key=lambda x: x[0], reverse=True)
                    
                    # On transforme la ligne de paroles en liste pour pouvoir insérer facilement
                    paroles_liste = list(ligne_suivante)
                    
                    for index, accord in accords_trouves:
                        # Si l'accord est positionné plus loin que la longueur du texte, 
                        # on agrandit le texte avec des espaces
                        if index > len(paroles_liste):
                            paroles_liste.extend([' '] * (index - len(paroles_liste)))
                        
                        # On insère l'accord au format ChordPro [Accord]
                        paroles_liste.insert(index, f"[{accord}]")
                    
                    # On rassemble la ligne fusionnée
                    ligne_fusionnee = "".join(paroles_liste)
                    chanson_chordpro.append(ligne_fusionnee.strip())
                    
                    # On avance de 2 lignes puisqu'on a traité accords + paroles
                    i += 2
                else:
                    # C'est une ligne de texte normale sans accord au-dessus
                    chanson_chordpro.append(ligne_actuelle.strip())
                    i += 1
            else:
                chanson_chordpro.append(ligne_actuelle.strip())
                i += 1

        # 3. Résultat final prêt pour la Base de Données
        texte_final_chordpro = "\n".join(chanson_chordpro)
        return texte_final_chordpro
    
def GetSongs(songs_link):
    songsChord = []

    for link in songs_link:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("h1", class_="entry-title")

        if title:
            texte_propre = title.get_text(strip=False).replace("\xa0", " ").replace("–", "-")  # Remplacer le tiret moyen (en-dash).replace("—", "-")  # Remplacer le tiret long au cas où (em-dash)
    
    
            # 2. On découpe selon la parenthèse
            ligne = texte_propre.split("(")
            if len(ligne) <2:
                ligne = texte_propre.split("-")
            
            # 3. On nettoie les espaces au début/fin de chaque élément, et on vire la parenthèse fermante ')'
            ligne = [l.replace(")", "").strip() for l in ligne if l.strip()]
        else :
            print("dafuq", link)
        
        print(ligne)

        divs = soup.find_all("div", class_="entry-content" )

        for div in divs:
            song = acousticGasySerializer(div)
            songsChord.append({"artist":ligne[1],"title":ligne[0],"content":song, "is_public": True})

    return songsChord
    
# print(GetSongs(GetSongUrl(GetMpihira(acousticGasyurl))))

class Command(BaseCommand):
    help = "Scrape acousticgasy et remplit la base SQLite"

    def handle(self, *args, **options):

        chanson_list = GetSongs(GetSongUrl(GetMpihira(acousticGasyurl)))
        for chanson_dict in chanson_list:
            song_obj, created = Chord.objects.update_or_create(
                title=chanson_dict["title"],
                artist=chanson_dict["artist"],
                defaults={
                    "content": chanson_dict["content"],
                    "is_public": chanson_dict["is_public"],
                    "user": None  # Les morceaux publics n'appartiennent à aucun utilisateur spécifique
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f" [Créé] {song_obj.artist} - {song_obj.title} ajouté en BDD !"))
            else:
                self.stdout.write(self.style.SUCCESS(f" [Mis à jour] {song_obj.artist} - {song_obj.title} mis à jour !"))

            self.stdout.write(self.style.SUCCESS("=== Fin du processus avec succès ==="))
