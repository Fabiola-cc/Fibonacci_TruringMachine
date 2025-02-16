import json
import Machine as m

print("Bienveido al simulador de máquina de turing")

print("\nLeyendo información de la máquina")
# Abrir y leer el archivo JSON
with open("another_machine.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Carga el contenido del archivo como un diccionario

Q = data["states"] #Estados
sigma = data["alphabet"] #Alfabeto de entrada
gamma = data["tapeAlphabet"] #Alfabeto de cinta
q0 = data["initialState"] #Estado inicial
F = data["finalState"] #Estado final
Blanc = data["Blanc"] #Símbolo blanco
delta = data["delta"] #Lista de transiciones //'estado, lectura': [transicion, input, movimiento]
tapeInput = data["tapeInput"] #Input inicial en cadena

tape = m.tape_initialization(Blanc, tapeInput)
result = m.derivation(Blanc, q0, F, delta, tape)
print(f"Resultado en la cinta: {result}")