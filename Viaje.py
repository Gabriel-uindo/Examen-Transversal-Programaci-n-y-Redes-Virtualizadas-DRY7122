import requests
import urllib.parse


api_key = "b5d44e4b-88b2-4ca1-b4c4-901f086ff2e3"  
route_url = "https://graphhopper.com/api/1/route?"


def geocoding(location, api_key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    params = {"q": location, "limit": "1", "key": api_key}
    url = geocode_url + urllib.parse.urlencode(params)

    response = requests.get(url)
    json_data = response.json()
    status_code = response.status_code

    if status_code == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lon = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        state = json_data["hits"][0].get("state", "")
        country = json_data["hits"][0].get("country", "")
        if state and country:
            full_name = f"{name}, {state}, {country}"
        elif state:
            full_name = f"{name}, {state}"
        else:
            full_name = name
        return 200, lat, lon, full_name
    else:
        print(f"Error geocoding: {status_code} - {json_data.get('message', '')}")
        return status_code, None, None, location


print("============================================")
print("       EXAMEN DRY7122 - ÍTEM 2")
print(" Obtener viaje entre ciudad de Chile y Argentina")
print("============================================")

origin_city = input("Ingrese ciudad de origen en Chile: ")
origin_data = geocoding(origin_city, api_key)

dest_city = input("Ingrese ciudad de destino en Argentina: ")
dest_data = geocoding(dest_city, api_key)

if origin_data[0] == 200 and dest_data[0] == 200:

    origin_point = "&point=" + str(origin_data[1]) + "%2C" + str(origin_data[2])
    dest_point = "&point=" + str(dest_data[1]) + "%2C" + str(dest_data[2])

    params = {"key": api_key, "vehicle": "car"}
    final_url = route_url + urllib.parse.urlencode(params) + origin_point + dest_point

    route_response = requests.get(final_url)
    route_status = route_response.status_code
    route_data = route_response.json()

    print("============================================")
    print(f"Dirección desde {origin_data[3]} hasta {dest_data[3]}")
    print("Usando vehículo: car")
    print("============================================")

    if route_status == 200:
        km = route_data["paths"][0]["distance"] / 1000
        miles = km / 1.61
        total_sec = route_data["paths"][0]["time"] / 1000
        hr = int(total_sec // 3600)
        min = int((total_sec % 3600) // 60)
        sec = int(total_sec % 60)

        print(f"Distancia total: {km:.1f} km / {miles:.1f} millas")
        print(f"Duración estimada: {hr}h {min}m {sec}s")
        print("============================================")
        print("Narrador del viaje (paso a paso):")
        for step in route_data["paths"][0]["instructions"]:
            text = step["text"]
            step_dist_km = step["distance"] / 1000
            print(f"- {text} ({step_dist_km:.1f} km)")
        print("============================================")
    else:
        print(f"Error al calcular ruta: {route_status} - {route_data.get('message', '')}")
else:
    print("No se pudo obtener coordenadas de origen o destino.")
