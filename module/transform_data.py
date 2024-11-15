import pycountry
import deepl
from babel import Locale
from babel.dates import format_date
from datetime import datetime

locale_fr = Locale('fr')

auth_key = "9fe3620b-df95-484d-9113-73ed10776b5b:fx"
translator = deepl.Translator(auth_key)

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