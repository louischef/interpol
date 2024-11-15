import concurrent.futures
import pycountry
from module.interpol_scrapping import getData, getDetails
from module.json_manipulation import loadJsonData
from module.text_manipulation import empty_file
import time
# Fonction pour traiter chaque URL
def process_url(url, index):
    try:
        details = getDetails(url)
        print(f"Details for URL {index}: {details}")
        loadJsonData(details)
        print(f"Processed URL {index}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Error processing URL {index}: {e}")

# Fonction pour traiter chaque pays
def process_country(country):
    try:
        getData(country)
        print(f"Processed country: {country.name}")
        time.sleep(0.5)  # Attendre 50 milliseconde pour éviter de surcharger le serveur
    except Exception as e:
        print(f"Error processing country {country.name}: {e}")

def main():
    # Nettoyer les fichiers au lancement du programme
    empty_file(r"C:\Users\louis\Downloads\Python intermédiaire\projetInterpole\links.txt")
    empty_file(r"C:\Users\louis\Downloads\Python intermédiaire\projetInterpole\clean_links.txt")

    # Utilisation de ThreadPoolExecutor pour les appels à getData pour chaque pays
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Soumet chaque pays à un thread
        futures = [executor.submit(process_country, country) for country in pycountry.countries]

        # Attendre la fin de tous les threads et gérer les exceptions
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Vérifie s'il y a des exceptions
            except Exception as e:
                print(f"Exception in process_country: {e}")

    # Lire les URLs nettoyées et les traiter avec multithreading
    with open("clean_links.txt", "r") as file:
        lines = file.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        [executor.submit(process_url, line.strip(), i+1) for i, line in enumerate(lines)]

if __name__ == "__main__":
    main()
