import json

# Función para encontrar los cambios en la cinta de la máquina
def delta_transitions(state, char_input, delta):
    key_value = f"{state}, {char_input}"
    changes = delta.get(key_value, []).copy()
    
    if len(changes) == 0:
        return changes

    # Reemplazar dirección por valor de suma
    if changes[2] == "S":
        changes[2] = "0"
    elif changes[2] == "R":
        changes[2] = "1"
    elif changes[2] == "L":
        changes[2] = "-1"
    
    return changes

# EJECUCION PRINCIPAL
print("Bienvenido al simulador de máquina de turing")

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

# FUNCIONAMIENTO DE MÁQUINA
tape = [Blanc, Blanc]
tape.extend(list(tapeInput))
tape.extend([Blanc, Blanc])

print("\nEjecutando máquina...\n")
state = q0
index = 2 #punto de inicio de la cinta
char_tape = tape[index] #caracter leido actualmente en la cinta

while not (state == F and char_tape == Blanc):
    changes = delta_transitions(state, char_tape, delta)
    state = changes[0]
    tape[index] = changes[1]
    index += int(changes[2])
    char_tape = tape[index]

tape_result = "".join(tape)
result = tape_result.replace(Blanc, "")

print(f"Resultado en la cinta: {result}\n")