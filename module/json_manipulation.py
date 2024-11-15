import json


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
