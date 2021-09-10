import json

all_invaders = json.load(open("all_invaders/all_invaders.json", ))
all_invaders_and_geoloc = json.load(open("invaders_and_geoloc/all_invaders_and_geoloc.json", ))

map_all_invaders_and_geoloc = {}
for pa_name in all_invaders_and_geoloc:
    map_all_invaders_and_geoloc[pa_name] = all_invaders_and_geoloc[pa_name]


def should_print_no_geoloc(inv):
    if inv["invader_name"] not in map_all_invaders_and_geoloc:
        return False
    invader = map_all_invaders_and_geoloc[inv["invader_name"]]
    if "invisible" in invader and invader["invisible"] is not None:
        return False

    if "longitude" not in invader:
        return True


for inv in all_invaders:
    if "banlieue" in str(inv["arrondissement"]) or inv["destroyed"]:
        continue
    if should_print_no_geoloc(inv):
        print("We don't have geoloc for ", inv)
