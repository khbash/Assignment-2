import requests
from pyexpat import features

response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson")

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

data=response.json()

import json
with open('earthquake.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, indent=5, ensure_ascii=False)

PARAMS = {
    "Place" :
    "Magnitude" :
    "Time" :
    "Depth" :
}