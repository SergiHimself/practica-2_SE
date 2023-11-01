import json
import sys
import copy
import tkinter as tk
from tkinter import simpledialog, messagebox

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

def hacer_pregunta(i):
    if i < num_preguntas:
        pregunta = preguntas["preguntas"][i]
        propiedad_buscar = pregunta["propiedad"]

        label_pregunta.config(text=pregunta['pregunta'] + " (s/n): ")
        respuesta_usuario.set("")  # Reiniciar la respuesta del usuario
        
        def continuar():
            respuesta_i = respuesta_usuario.get().strip().lower()
            if respuesta_i not in ('s', 'n'):
                messagebox.showwarning("Respuesta no válida", "Por favor, ingrese 's' para Sí o 'n' para No.")
            else:
                take_chance(respuesta_i, propiedad_buscar)
                nuevo_personaje["propiedades"][pregunta["propiedad"]] = respuesta_i == 's'
                hacer_pregunta(i + 1)
        
        button_continuar.config(command=continuar)
    else:
        finalizar_adivinador()

def finalizar_adivinador():
    if len(personajes["personajes"]) == 1:
        resultado = f"Tu personaje es {personajes['personajes'][0]['nombre']}"
    else:
        nueva_respuesta = tk.simpledialog.askstring("Adivinador", "No se ha encontrado un personaje que coincida con las respuestas proporcionadas. ¿En quién estabas pensando?")
        if nueva_respuesta and nueva_respuesta.lower() != 'saltar':
            nuevo_personaje["nombre"] = nueva_respuesta
            seguridad["personajes"].append(nuevo_personaje)
            guardar_base_de_datos('akinator_base_de_datos.json', seguridad)
            resultado = f'Gracias, aprendí un nuevo personaje: {nueva_respuesta}'
        else:
            resultado = "Adiós"
    label_resultado.config(text=resultado)

def reiniciar_juego():
    global personajes
    personajes = cargar_base_de_datos('akinator_base_de_datos.json')
    label_resultado.config(text="")
    hacer_pregunta(0)

if __name__ == '__main__':
    preguntas = cargar_base_de_datos('akinator_preguntas.json')
    personajes = cargar_base_de_datos('akinator_base_de_datos.json')
    seguridad = copy.deepcopy(personajes)
    num_preguntas = len(preguntas["preguntas"])
    nuevo_personaje = {"nombre": None, "propiedades": {}}

    root = tk.Tk()
    root.title("Adivinador")
    
    label_pregunta = tk.Label(root, text="Adivino: Lucha Libre")
    label_pregunta.pack()

    label_pregunta = tk.Label(root, text="")
    label_pregunta.pack()
    
    label_resultado = tk.Label(root, text="")
    label_resultado.pack()

    respuesta_usuario = tk.StringVar()
    entry_respuesta = tk.Entry(root, textvariable=respuesta_usuario)
    entry_respuesta.pack()
    
    button_continuar = tk.Button(root, text="Continuar")
    button_continuar.pack()

    button_reiniciar = tk.Button(root, text="Reiniciar Juego", command=reiniciar_juego)
    button_reiniciar.pack()

    hacer_pregunta(0)

    root.mainloop()