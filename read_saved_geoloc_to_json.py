import json

all_lines = open("save_some_geoloc.txt", "r").readlines()

invaders = {}
for line in all_lines:
    print(line)
    parts = line.split(" ")
    if "is here" in line:
        invaders[parts[0]] = {
            "pa_name": parts[0],
            "latitude": parts[3].replace(",", ""),
            "longitude": parts[4].replace("\n", "")
        }
    if "We can't find geoloc for" in line:
        pa_name = parts[5].replace(",", "")
        invaders[pa_name] = {
            "pa_name": pa_name
        }

file1 = open("invaders_and_geoloc/all_invaders_and_geoloc.json", "w")
file1.write(json.dumps(invaders))
file1.close()
