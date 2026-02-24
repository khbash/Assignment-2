import requests
import json
import pandas as pd
import numpy as np

from pyexpat import features

response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson")
data = response.json()

URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

with open('earthquake.json', 'w', encoding="utf-8") as file:
    json.dump(data, file, indent=5, ensure_ascii=False)

features = data['features']

data_list = []
for eq in features:
    data_list.append({
        'Place': eq['properties']['place'],
        'Magnitude': eq['properties']['mag'],
        'Time': eq['properties']['time'],
        'Depth': eq['geometry']['coordinates'][2]
    })

df = pd.DataFrame(data_list)

df = df.dropna()
df = df[df['Magnitude'] > 3.0]
df['Time'] = pd.to_datetime(df['Time'], unit='ms')

print(f"Середня магнітуда: {df['Magnitude'].mean():.2f}")
print(f"Медіана магнітуди: {df['Magnitude'].median():.2f}")
print(f"Максимальна магнітуда: {df['Magnitude'].max():.2f}")

print("\nТоп-5 найсильніших землетрусів:")
print(df.nlargest(5, 'Magnitude')[['Place', 'Time', 'Magnitude']])

correlation = df['Magnitude'].corr(df['Depth'])
print(f"\nКореляція між магнітудою та глибиною: {correlation:.2f}")