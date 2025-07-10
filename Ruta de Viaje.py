import requests
import urllib.parse

# =================================
# CONFIGURACIÓN
# =================================
api_key = "d242aefe-259c-4221-90ba-a14a854a060a"  # <-- pon aquí tu clave de Graphhopper
route_url = "https://graphhopper.com/api/1/route?"

def geocoding(location):
    url = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(location)}&limit=1&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and len(data["hits"]) != 0:
        point = data["hits"][0]["point"]
        lat, lng = point["lat"], point["lng"]
        name = data["hits"][0].get("name", location)
        return lat, lng, name
    else:
        print(f"⚠️ No se pudo encontrar {location}")
        return None, None, location

while True:
    vehicle = input("Tipo de vehículo (car, bike, foot): ")
    if vehicle in ["s", "quit"]:
        break

    origen = input("Ciudad origen en Chile: ")
    if origen in ["s", "quit"]:
        break
    lat_o, lng_o, name_o = geocoding(origen)

    destino = input("Ciudad destino en Argentina: ")
    if destino in ["s", "quit"]:
        break
    lat_d, lng_d, name_d = geocoding(destino)

    if lat_o and lat_d:
        points = f"&point={lat_o}%2C{lng_o}&point={lat_d}%2C{lng_d}"
        final_url = f"{route_url}vehicle={vehicle}&key={api_key}{points}"

        response = requests.get(final_url)
        data = response.json()

        if response.status_code == 200:
            path = data["paths"][0]
            km = path["distance"] / 1000
            miles = km / 1.61
            t_sec = path["time"] / 1000
            h = int(t_sec // 3600)
            m = int((t_sec % 3600) // 60)
            s = int(t_sec % 60)
            print("=======================================")
            print(f"De {name_o} a {name_d} con {vehicle}")
            print(f"Distancia: {km:.1f} km / {miles:.1f} mi")
            print(f"Duración: {h}h {m}m {s}s")
            print("Narrador:")
            for step in path["instructions"]:
                print(f"- {step['text']} ({step['distance']/1000:.1f} km)")
            print("=======================================")
        else:
            print("⚠️ No se pudo calcular la ruta.")
    else:
        print("⚠️ Datos inválidos, vuelve a intentar.")

    seguir = input("¿Quieres calcular otra ruta? (Enter para sí, s para salir): ")
    if seguir.lower() in ["s", "quit"]:
        break

# =================================
# STOP para Windows / Notepad++
# =================================
input("Presiona Enter para cerrar...")
