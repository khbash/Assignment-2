import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

df['Region'] = df['Place'].str.split(',').str[-1].str.strip()
top_regions = df['Region'].value_counts().head(5)
print("\nТоп-5 регіонів за кількістю подій:")
print(top_regions)

plt.subplot(1, 3, 1)
plt.hist(df['Magnitude'], bins=15, color='skyblue', edgecolor='black')
plt.title('Розподіл магнітуд')
plt.xlabel('Магнітуда')

plt.subplot(1, 3, 2)
plt.scatter(df['Depth'], df['Magnitude'], alpha=0.5, color='salmon')
plt.title('Глибина vs Магнітуда')
plt.xlabel('Глибина (км)')
plt.ylabel('Магнітуда')

plt.subplot(1, 3, 3)
top_regions.plot(kind='bar', color='lightgreen')
plt.title('Топ-5 регіонів')
plt.ylabel('Кількість')

plt.show()