import json

all_invaders_and_geoloc = json.load(open("invaders_and_geoloc/all_invaders_and_geoloc.json", ))

invaders_by_arr = {}

for pa_name in sorted(all_invaders_and_geoloc.keys()):
    print(pa_name  + " => " + all_invaders_and_geoloc[pa_name]["zip_code"])


for pa_name in all_invaders_and_geoloc:
    inv = all_invaders_and_geoloc[pa_name]
    zip_code = inv["zip_code"]
    if zip_code not in invaders_by_arr:
        invaders_by_arr[zip_code] = []
    invaders_by_arr[zip_code].append(inv["pa_name"])


'''
for arr in sorted(invaders_by_arr.keys()):
    print("\nArr " + arr)
    print(sorted(invaders_by_arr[arr]))
'''