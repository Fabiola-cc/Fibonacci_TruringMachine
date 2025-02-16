import json

# FUNCIONES PARA UTILIZAR MÁQUINA
def tape_initialization(blanc, input_string):
    tape = [blanc, blanc]
    tape.extend(list(input_string))
    tape.extend([blanc, blanc])
    return tape

def derivation(blanc, initial_state, acceptance_state, delta, tape):
    print("Ejecutando secuencia...")
    delta = delta #transiciones de la máquina
    state = initial_state
    index = 2 #punto de inicio de la cinta
    char_tape = tape[index] #caracter leido actualmente en la cinta

    while not (state == acceptance_state and char_tape == blanc):
        changes = delta_transitions(state, char_tape, delta)
        state = changes[0]
        tape[index] = changes[1]
        index += int(changes[2])
        char_tape = tape[index]
    
    tape_result = "".join(tape)
    return tape_result.replace(blanc, "")

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

tape = tape_initialization(Blanc, tapeInput)
result = derivation(Blanc, q0, F, delta, tape)
print(f"Resultado en la cinta: {result}")