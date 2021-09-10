import json

invaders_and_geoloc = json.load(open("invaders_and_geoloc/all_invaders_and_geoloc.json", ))

for i in range(1, 21):
    if i < 10:
        i = "0" + str(i)
    zip_code = "750" + str(i)

    kml = open("build_kml/begin_kml.txt", "r").read()
    for pa_name in invaders_and_geoloc:
        invader = invaders_and_geoloc[pa_name]
        if invader["zip_code"] != zip_code:
            continue
        if "latitude" in invader:
            kml = kml + "<Placemark><name>" + pa_name + "</name>" + \
                  "<styleUrl>#icon-1899-F9A825-nodesc</styleUrl>" + \
                  "<Point>" + \
                  "<coordinates>" + \
                  str(invader["longitude"]) + "," + str(invader["latitude"]) + ",0" + \
                  "</coordinates></Point></Placemark>"

    kml = kml + "</Folder></Document></kml>"

    file1 = open("final_kml/map_for_" + zip_code + ".kml", "w")
    file1.write(kml)
    file1.close()


