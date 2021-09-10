import json
import re

from bs4 import BeautifulSoup
import os

def extract_arrondissement(content):
    if "Paris - 1er arrondissement" in content:
        return 1

    title_search = re.search('Paris - (\d{1,2})ème arrondissement', content, re.IGNORECASE)
    if title_search:
        return title_search.group(1)

    title_search = re.search('Paris - banlieue (\d{1,2})', content, re.IGNORECASE)
    if title_search:
        return "banlieue " + title_search.group(1)
    print("arr Not found in " + content)
    return None


path = 'invaders_spotter_free_html_pages/'
files = os.listdir(path)
invaders = []
invaders_list = ""
for filename in files:
    f = open(path + filename, "r")
    page_text = f.read()
    soup = BeautifulSoup(page_text, 'html.parser')

    table = soup.find('table')
    results = table.find_all('tr', attrs={'class': 'haut'})
    print('Number of results', len(results))

    for res in results:
        content = str(res)
        destroyed = "Détruit" in content
        invader_name = re.findall(r"PA_\d\d\d\d", content)[0]
        arr = extract_arrondissement(content)
        print(invader_name, arr, destroyed)
        invaders.append({
            "invader_name": invader_name,
            "arrondissement": arr,
            "destroyed": destroyed
        })
        if not destroyed:
            invaders_list = invaders_list + invader_name + "\n"

file1 = open("all_invaders/all_invaders.json", "w")
file1.write(json.dumps(invaders))
file1.close()
file2 = open("all_invaders/all_invaders.list", "w")
file2.write(invaders_list)
file2.close()
