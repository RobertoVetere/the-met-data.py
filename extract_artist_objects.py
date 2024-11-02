import json
import sys

def extract_artist_objects(input_file, artist_name, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Filtrar objetos que contengan el nombre del artista
    artist_objects = [
        obj for obj in data.get("objects", [])
        if obj.get("constituents") and any(
            constituent.get("name") == artist_name or constituent.get("artistDisplayName") == artist_name
            for constituent in (obj.get("constituents") or [])
        )
    ]

    # Guardar los objetos filtrados en el archivo de salida
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(artist_objects, file, indent=4, ensure_ascii=False)
    
    print(f"Archivo '{output_file}' creado con {len(artist_objects)} objetos de {artist_name}.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python extract_artist_objects.py <input_file> <artist_name> <output_file>")
    else:
        input_file = sys.argv[1]
        artist_name = sys.argv[2]
        output_file = sys.argv[3]
        extract_artist_objects(input_file, artist_name, output_file)
