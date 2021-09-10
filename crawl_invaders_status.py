from time import sleep

import requests


for page_num in range(1, 31):
    sleep(2)
    url = 'http://invader.spotter.free.fr/listing.php'
    myobj = {'ville': 'PA', "mode": "liste", "page": page_num, "arrondissement": "00"}
    x = requests.post(url, data=myobj)

    file1 = open("invaders_spotter_free_html_pages/invaders_page_" + str(page_num) + ".html", "w")
    file1.write(x.text)
    file1.close()
