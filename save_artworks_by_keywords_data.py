import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
collection = "renoir"
# Información inicial
data = {
    "title": collection,
    "total": 636,
    "objectIDs": [
438815, 438011, 437432, 438014, 437430, 459110, 459112, 459111, 438012, 438013, 438010, 437436, 437426, 437437, 437429, 437425, 441104, 437433, 437424, 437135, 264858, 201585, 436965, 490026, 459967, 459971, 459970, 459968, 459969, 459113, 459109, 437438, 459966, 437439, 437428, 437431, 437427, 358923, 437434, 339677, 339674, 437435, 358770, 358926, 358922, 358927, 339678, 364095, 358929, 191807, 358765, 722444, 436703, 336671, 488710, 284452, 285444, 333817, 19294, 364093, 436132, 436706, 436947, 437317, 437299, 437133, 10915, 19335, 436534, 437680, 844492, 436958, 436840, 436175, 436960, 435868, 437301, 337576, 438005, 438820, 437313, 436945, 438823, 437136, 436123, 437989, 482061, 437847, 495585, 437686, 437118, 437310, 437993, 439361, 436964, 438002, 437117, 436952, 438003, 437124, 436121, 439631, 436525, 489996, 438551, 436944, 436530, 336046, 436162, 436004, 436144, 436322, 436948, 436002, 436950, 436545, 436001, 437160, 435962, 436176, 437111, 437384, 486845, 436159, 436155, 437926, 435879, 437115, 436946, 438144, 437130, 437105, 437108, 435626, 482386, 339751, 438136, 337620, 337405, 337413, 435867, 441374, 438435, 435875, 436548, 334373, 487806, 489551, 436127, 437942, 334652, 437052     
    ]
}

# URL base de la API
base_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

# Función para obtener los datos de un objeto individual
def fetch_object_data(object_id):
    try:
        response = requests.get(f"{base_url}/{object_id}")
        response.raise_for_status()  # Verifica si hubo errores en la solicitud
        object_data = response.json()

        # Verifica si ambos URLs de imágenes están presentes
        if object_data.get("primaryImage") and object_data.get("primaryImageSmall"):
            return object_data
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el objeto {object_id}: {e}")
    return None

# Lista para almacenar los datos completos de los objetos
objects_data = []

# Usar multihilos para cargar los datos en paralelo
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_id = {executor.submit(fetch_object_data, obj_id): obj_id for obj_id in data["objectIDs"]}

    for future in as_completed(future_to_id):
        object_data = future.result()
        if object_data:
            objects_data.append(object_data)

# Guardar todos los datos en un archivo JSON
with open( collection + ".json", "w") as f:
    json.dump({"title": data["title"], "total": len(objects_data), "objects": objects_data}, f, indent=4)

print("Datos guardados en " + collection + ".json")
