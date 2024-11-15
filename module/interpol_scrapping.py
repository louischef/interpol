import requests
import json
from module.transform_data import transformer_donnees
from module.json_manipulation import remove_duplicate
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
    

def getDetails(link):
    response = requests.request("GET", link, headers=headers, data=payload, proxies={'http': 'http://pkg-private2-country-any:8apd175kpstbkf7v@private-eu.vital-proxies.com:8603'})
    if response.status_code == 200:
        resultat = transformer_donnees(response.json())
        return resultat
    else:
        response.raise_for_status()