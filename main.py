import concurrent.futures
import time
from module.interpol_scrapping import getData, loadJsonData, getDetails

# Fonction à exécuter en parallèle pour chaque URL
def process_url(url, index):
    try:
        details = getDetails(url)
        print(f"Details for URL {index}: {details}")
        loadJsonData(details)
        print(f"Processed URL {index}")
    except Exception as e:
        print(f"Error processing URL {index}: {e}")

def main():
    with open("clean_links.txt", "r") as file:
        lines = file.readlines()

    # On définit le nombre de threads (ici 10 par exemple)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # On crée un iterable de tuples (url, index) pour les passer à la fonction `process_url`
        futures = [executor.submit(process_url, line.strip(), i+1) for i, line in enumerate(lines)]
        
        # On attend que tous les threads terminent
        for future in concurrent.futures.as_completed(futures):
            # On peut récupérer des résultats ou simplement gérer les exceptions ici
            pass

if __name__ == "__main__":
    main()
