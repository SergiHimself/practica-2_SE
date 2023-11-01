import sys
import json
import copy

def cargar_base_de_datos(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def guardar_base_de_datos(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def take_chance(respuesta, propiedad):
    if respuesta == "s":
        res = True
    else:
        res = False

    to_remove = []
    for p in personajes["personajes"]:
        if p["propiedades"][propiedad] != res:
            to_remove.append(p)

    for p in to_remove:
        personajes["personajes"].remove(p)

preguntas: dict = cargar_base_de_datos('akinator_preguntas.json')
personajes: dict = cargar_base_de_datos('akinator_base_de_datos.json')
seguridad = copy.deepcopy(personajes)

num_preguntas = len(preguntas["preguntas"])

nuevo_personaje = {"nombre": None, "propiedades": {}}

print("Adivino: Lucha Libre")
for i in range(0, num_preguntas):
    pregunta = preguntas["preguntas"][i]
    propiedad_buscar = pregunta["propiedad"]
    respuesta = input(f"{pregunta['pregunta']} (s/n): ")
    take_chance(respuesta, propiedad_buscar)
    nuevo_personaje["propiedades"][pregunta["propiedad"]] = respuesta.lower() == 's'
    
if len(personajes["personajes"]) == 1:
    print("\nTu luchador es " + personajes["personajes"][0]["nombre"])
    sys.exit()
else:
    nueva_respuesta: str = input("No se ha encontrado un luchador que coincida con las respuestas proporcionadas. ¿En quién estabas pensando? ")

    if nueva_respuesta.lower() != 'saltar':
        # Agrega el nombre del nuevo personaje
        nuevo_personaje["nombre"] = nueva_respuesta
    
        # Agrega el nuevo personaje a la lista de personajes
        seguridad["personajes"].append(nuevo_personaje)
        guardar_base_de_datos('akinator_base_de_datos.json', seguridad)
        print(f'Gracias, aprendí un nuevo luchador: {nueva_respuesta}')