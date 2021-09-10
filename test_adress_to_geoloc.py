import os

import requests

resp = requests.get(url="https://maps.googleapis.com/maps/api/geocode/json",
                    params={
                        "address": "église Saint-Eustache, 75001,France",
                        "key": os.environ["GOOGLE_MAP_KEY"]
                    }).json()

location = resp["results"][0]["geometry"]["location"]
print(location)
