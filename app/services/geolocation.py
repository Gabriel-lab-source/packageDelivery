import requests


def get_route(lat1, lon1, lat2, lon2):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    headers = {
        "Authorization": "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjQ3NmZjMWRmMTgyYjRmYjM4YTg0NjM3MjNmNDI5YjU3IiwiaCI6Im11cm11cjY0In0=",
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [lon1, lat1],
            [lon2, lat2]
        ]
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    summary = data["features"][0]["properties"]["summary"]

    distance = summary["distance"] / 1000
    duration = summary["duration"] / 60
    geometry = data["features"][0]["geometry"]

    return {
        "distance": round(distance, 2),
        "duration": round(duration, 2),
        "geometry": geometry
    }


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
