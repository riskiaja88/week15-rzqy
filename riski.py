from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pymongo import MongoClient
import certifi
import requests
from math import radians, cos, sin, asin, sqrt

password = 'riskipipo'
cxn_str = f'mongodb://riskiwe0:{password}@ac-arj6m9i-shard-00-00.fca6kp0.mongodb.net:27017,ac-arj6m9i-shard-00-01.fca6kp0.mongodb.net:27017,ac-arj6m9i-shard-00-02.fca6kp0.mongodb.net:27017/?ssl=true&replicaSet=atlas-106k85-shard-0&authSource=admin&retryWrites=true&w=majority'
client = MongoClient(cxn_str)
db = client.dbsparta_plus_week3

# Fungsi untuk menghitung jarak antara dua titik geografis
def distance(lat1, lat2, lon1, lon2):
     
    # Modul matematika bermuat fungsi bernama
    # radian yang mengonversi dari derajat ke radian.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # formula Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius bumi dalam kilometer. Gunakan 3956 untuk mil
    r = 6371
      
    # kalkulasikan hasil
    return(c * r)

# Fungsi untuk mengkonversi km ke mil
def km_to_mil(km):
    return km * 0.621371

# Endpoint API SpaceX untuk mendapatkan daftar peluncuran
launches_url = "https://api.spacexdata.com/v4/launches"
response = requests.get(launches_url)
launches = response.json()[-20:]  # Ambil 20 peluncuran terakhir

# Loop melalui setiap peluncuran
for launch in launches:
    launchpad_id = launch["launchpad"]
    
    # Endpoint API SpaceX untuk mendapatkan nama lengkap launchpad
    launchpad_url = f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}"
    response = requests.get(launchpad_url)
    launchpad = response.json()
    launchpad_name = launchpad["full_name"]
    launchpad_lat, launchpad_lon = launchpad["latitude"], launchpad["longitude"]
    
    # Endpoint API geocoding Mapbox untuk mendapatkan koordinat geografis launchpad
    mapbox_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    access_token = 'pk.eyJ1IjoiYXZlcmFnZXN0dWRlbnQiLCJhIjoiY2xmNWoxZGk0MTNidTNzbzRoMnRtNnh3byJ9.deUPDd5iBomdXP3nxvYebg'
    response = requests.get(f"{mapbox_url}{launchpad_name}.json?access_token={access_token}")
    mapbox_data = response.json()
    if len(mapbox_data["features"]) == 0:
        print(f"Koordinat tidak ditemukan untuk {launchpad_name}")
        continue
    mapbox_lon, mapbox_lat = mapbox_data["features"][0]["center"]
    
    # Perbedaan dalam km antara hasil geocoding Mapbox dan posisi SpaceX resmi untuk launchpad
    distance_km = distance(mapbox_lat, launchpad_lat, mapbox_lon, launchpad_lon)
    distance_mil = km_to_mil(distance_km)
    
    # Cetak hasil
    print(launch['date_local'], launchpad_name, launchpad_name, f"{distance_km:.2f}\n")