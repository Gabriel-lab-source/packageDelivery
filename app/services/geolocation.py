import requests
import math


def get_coordinates(address):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json"
    }

    headers = {
        "User-Agent": "delivery-app"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return None, None

    data = response.json()

    if not data:
        return None, None

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    return lat, lon


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # raio da Terra em km

    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def estimate_time(distance_km, speed_kmh=30):
    if not distance_km:
        return 0

    hours = distance_km / speed_kmh
    minutes = hours * 60

    return round(minutes)
