import json
import os
import re


def find_address(pa_name, page_text):
    title_search = re.search(r'<div class="txt">Space Invader ' + pa_name + '(.*)</div>', page_text, re.IGNORECASE)
    if title_search:
        address_found = title_search.group(1)
        return address_found
    else:
        print("No adress found for " + pa_name)
        return None


def find_district(pa_name, page_text):
    title_search = re.search(r'<div class="sub t4">Dans la zone <a href=".*">(.*)</a></div>', page_text, re.IGNORECASE)
    if title_search:
        address_found = title_search.group(1)
        return address_found
    else:
        print("No district found for " + pa_name)
        return None


def find_all():
    path = 'battleparis/'
    files = os.listdir(path)
    invaders = []
    for filename in files:
        f = open(path + filename, "r")
        pa_name = filename.replace("invader_", "").replace(".html", "")
        page_text = f.read()
        address = find_address(pa_name, page_text)
        district = find_district(pa_name, page_text)
        print(pa_name, "is here: ", address , ",", district , ", Paris")
        invaders.append({
            "pa_name": pa_name,
            "address": address,
            "district": district
        })
    print("invaders count is: " + str(len(invaders)))
    file1 = open("invaders_and_address/all_invaders_and_address.json", "w")
    file1.write(json.dumps(invaders))
    file1.close()


find_all()
