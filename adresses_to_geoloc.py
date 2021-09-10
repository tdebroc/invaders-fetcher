import json
import os
from time import sleep

import requests
from geopy import Nominatim

all_invaders_and_address = json.load(open("invaders_and_address/all_invaders_and_address.json", ))

invaders_and_geoloc = json.load(open("invaders_and_geoloc/all_invaders_and_geoloc.json", ))

locator = Nominatim(user_agent='myGeocoder641')


def build_invaders_to_zip_code():
    all_invaders = json.load(open("all_invaders/all_invaders.json", ))
    pa_name_to_arr = {}
    for inv in all_invaders:
        arr = inv["arrondissement"]
        is_digit = isinstance(arr, int) or arr.isdigit()
        if is_digit and int(arr) < 10:
            arr = "7500" + str(arr)
        elif is_digit and int(arr) >= 10:
            arr = "750" + str(arr)
        elif "banlieue" in arr:
            arr = arr.split(" ")[1]
        else:
            raise Exception("Can't convert arr to code postal")
        pa_name_to_arr[inv["invader_name"]] = arr
    return pa_name_to_arr


def save_invader(invaders_and_geoloc):
    file1 = open("invaders_and_geoloc/all_invaders_and_geoloc.json", "w")
    file1.write(json.dumps(invaders_and_geoloc))
    file1.close()
    sleep(1)


scan = True


def convert_address_to_geoloc():
    global scan
    invader_to_zip_code = build_invaders_to_zip_code()
    for inv in all_invaders_and_address:
        print(inv)
        pa_name = inv["pa_name"]
        if pa_name == "PA_0173":
            scan = False
        if not scan:
            continue

        zip_code = invader_to_zip_code[pa_name]

        if pa_name not in invaders_and_geoloc:
            invaders_and_geoloc[pa_name] = {}
        invaders_and_geoloc[pa_name]["pa_name"] = pa_name
        invaders_and_geoloc[pa_name]["zip_code"] = zip_code
        invaders_and_geoloc[pa_name]["address"] = inv["address"] if "address" in inv else None
        invaders_and_geoloc[pa_name]["invisible"] = inv["invisible"] if "invisible" in inv else None

        if not zip_code.startswith("75"):
            continue

        if "geoloc_forced" in inv:
            geo_parts = inv["geoloc_forced"].split(",")
            invaders_and_geoloc[pa_name]["pa_name"] = pa_name
            invaders_and_geoloc[pa_name]["latitude"] = geo_parts[0].replace(" ", "")
            invaders_and_geoloc[pa_name]["longitude"] = geo_parts[1].replace(" ", "")

        elif inv["address"] is not None:
            full_address = inv["address"].replace(",", "") + "," + zip_code + ", Paris, France"
            print("Locating " + full_address)

            resp = requests.get(url="https://maps.googleapis.com/maps/api/geocode/json",
                                params={
                                    "address": full_address,
                                    "key": os.environ["GOOGLE_MAP_KEY"]
                                }).json()

            if len(resp["results"]) > 0:
                location = resp["results"][0]["geometry"]["location"]
                invaders_and_geoloc[pa_name]["pa_name"] = pa_name
                invaders_and_geoloc[pa_name]["latitude"] = location["lat"]
                invaders_and_geoloc[pa_name]["longitude"] = location["lng"]
                print(pa_name + " found here: " + str(location["lat"]) + ", " + str(location["lng"]))
                if location["lat"] < 48.53118738378756 or location["lng"] < 1.798749922324435 \
                        or location["lat"] > 49.0530719135176 or location["lng"] > 2.8729098208012553:
                    print("Strange location retrieved ! Out of Paris ")
            else:
                print("We can't find geoloc for " + pa_name + "," + full_address)
                inv["location"] = None
        save_invader(invaders_and_geoloc)
    save_invader(invaders_and_geoloc)


convert_address_to_geoloc()
