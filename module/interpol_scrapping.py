import requests
import json
import pycountry
import time
import deepl
from babel import Locale
from babel.dates import format_date
from datetime import datetime

auth_key = "9fe3620b-df95-484d-9113-73ed10776b5b:fx"
translator = deepl.Translator(auth_key)
# Initialisation de la locale en français
locale_fr = Locale('fr')

# afficher le total, si le total est supérieur à 160 alors
# segmenter par age
payload = {}
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-encoding': 'gzip, deflate, br, zstd',
  'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
  'cache-control': 'max-age=0',
  'priority': 'u=0, i',
  'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8"," "Chromium";v="129":',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36:'
}

# translator.translate_text("Hello, World!", target_lang="FR")


def getData(country, ageMin=0, ageMax=120, gender=None, forename=None, payload=payload, headers=headers) -> list:
    if gender is None:
        url = f"https://ws-public.interpol.int/notices/v1/red?nationality={country.alpha_2}&ageMax={ageMax}&ageMin={ageMin}&resultPerPage=160"
    else:
        url = f"https://ws-public.interpol.int/notices/v1/red?nationality={country.alpha_2}&ageMax={ageMax}&ageMin={ageMin}&sexId={gender}&resultPerPage=160"
    if forename:
        url += f"&forename={forename}"
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code != 200:
        print(f"Erreur lors de la requête: {response.status_code}")
        return {"total": 0, "notices": []}
    json_object = json.loads(response.text)
    total = json_object["total"]
    if total > 160:
        new_age = (ageMin + ageMax) // 2  # diviser l'âge à chaque fois par deux pour affiner
        if ageMin == ageMax:
            getData(country, ageMin, new_age, gender="F")
            if country.alpha_2 == 'RU' and gender == "M":
                getData(country, ageMin, new_age, gender, forename="islam")
            else:
                getData(country, ageMin, new_age, gender="M")
            return json_object
        getData(country, ageMin, new_age, gender)  # donc à chaque fois qu'il y a trop de requêtes, il affinera avec le nouvel âge
        getData(country, new_age + 1, ageMax, gender)
    print(f"Total: {total}")
    persons = json_object["_embedded"]["notices"]
    for person in persons:
        link = person["_links"]["self"]["href"]
        with open('links.txt', 'a') as f:
            f.write(link + "\n")
    remove_duplicate('links.txt')
    
proxies_list = {'http': 'http://pkg-private2-country-any:8apd175kpstbkf7v@private-eu.vital-proxies.com:8603'}

def getDetails(link):
    response = requests.request("GET", link, headers=headers, data=payload, proxies=proxies_list)
    if response.status_code == 200:
        resultat = transformer_donnees(response.json())
        return resultat
    else:
        response.raise_for_status()


def loadJsonData(data):
    try:
        # Charger les données existantes dans data.json, s'il y en a
        try:
            with open('1data.json', 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except json.JSONDecodeError:
            json_data = []  # Fichier vide ou non initialisé, commencer avec une liste vide

        # Ajouter les nouvelles données
        json_data.append(data)

        # Écrire le tout dans le fichier, en remplaçant le contenu existant
        with open('1data.json', 'a', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    except json.JSONDecodeError:
        print("Erreur lors de la conversion en JSON.")


def remove_duplicate(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(f'clean_{filename}', 'w') as f:
        f.writelines(set(lines))

def get_country_name(alpha_2):
    try:
        if alpha_2:
            country = pycountry.countries.get(alpha_2=alpha_2)
            if country:
                return locale_fr.territories.get(alpha_2, "inconnu")
    except Exception as e:
        print(f"Erreur lors de la récupération du pays : {e}")
    return "inconnu"

def format_date_fr(date_str):
    if date_str and len(date_str.split('/')) == 3:
        try:
            date_obj = datetime.strptime(date_str, "%Y/%m/%d")
            return format_date(date_obj, format="short", locale="fr")
        except ValueError:
            return date_str
    return date_str

def translate_text(text, lang="FR"):
    # Vérifie si le texte est valide et non vide avant de le traduire
    if text and isinstance(text, str):
        try:
            return translator.translate_text(text, target_lang=lang).text.replace('"', "'")
        except Exception as e:
            print(f"Erreur de traduction : {e}")
            return text.replace('"', "'")
    return "inconnu"

couleurs_cheveux_fr = {
    "BLA": "noir",      # Black
    "BRO": "brun",      # Brown
    "BLD": "blond",     # Blonde
    "RED": "roux",      # Red
    "GRY": "gris",      # Gray
    "WHT": "blanc",     # White
    "BAL": "chauve",    # Bald
    "AUB": "auburn",    # Auburn
    "CHA": "châtain",   # Chestnut
    "DYE": "teint",     # Dyed
    "GRE": "gris",      # Grey
    "LIG": "clair",     # Light
}

couleurs_yeux_fr = {
    "BLA": "noir",      # Black
    "BRO": "marron",    # Brown
    "BLU": "bleu",      # Blue
    "GRN": "vert",      # Green
    "HAZ": "noisette",  # Hazel
    "GRY": "gris",      # Gray
    "AMB": "ambre",     # Amber
    "VLT": "violet",    # Violet
    "YEL": "jaune",     # Yellow
    "GOL": "doré",      # Golden
    "LIG": "clair",     # Light
}

def get_hair_colors(hair_codes):
    if hair_codes:
        return [couleurs_cheveux_fr.get(code.upper(), "inconnu") for code in hair_codes]
    return ["inconnu"]

def get_eye_colors(eye_codes):
    if eye_codes:
        return [couleurs_yeux_fr.get(code.upper(), "inconnu") for code in eye_codes]
    return ["inconnu"]




def transformer_donnees(data):
    def get_country_name(alpha_2):
        # Vérifie si le code est valide
        if alpha_2:
            country = pycountry.countries.get(alpha_2=alpha_2)
            return locale_fr.territories.get(alpha_2) if country else "inconnu"
        return "inconnu"

    # Création du dictionnaire des informations sur la personne
    personne_recherchee = {
        "nom": data.get("name") or "inconnu",
        "prenom": data.get("forename") or "inconnu",
        "date_naissance": format_date_fr(data.get("date_of_birth")) if data.get("date_of_birth") else "inconnu",
        "taille": data.get("height") or "inconnu",
        "poids": data.get("weight") or "inconnu",
        "sexe": data.get("sex_id") or "inconnu",
        "motif_recherche": (data.get("arrest_warrants", [{}])[0].get("charge")),
        "signes_distinctifs": (data.get("distinguishing_marks"))
    }
    
    # Générer les entrées indexées pour les couleurs des yeux, nationalités, couleurs de cheveux et langues parlées
    # avec une logique de numérotation
    personne_recherchee.update({
        f"couleur_yeux{i + 1}": color
        for i, color in enumerate(get_eye_colors(data.get("eyes_colors_id", [])))
    })
    
    personne_recherchee.update({
        f"nationalite{i + 1}": nationality
        for i, nationality in enumerate([get_country_name(n) for n in data.get("nationalities", [])])
    })
    
    personne_recherchee.update({
        f"couleur_cheveux{i + 1}": hair_color
        for i, hair_color in enumerate(get_hair_colors(data.get("hairs_id", [])))
    })
    
    personne_recherchee.update({
        f"langue_parlee{i + 1}": language
        for i, language in enumerate(data.get("languages_spoken_ids", []))
    })

    return personne_recherchee
