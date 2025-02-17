import json
machine_file = "Fibonacci_machine.json"
# Abrir y leer el archivo JSON
with open(machine_file, "r", encoding="utf-8") as file:
    data = json.load(file)  # Carga el contenido del archivo como un diccionario

Q = data["states"] #Estados
sigma = data["alphabet"] #Alfabeto de entrada
gamma = data["tapeAlphabet"] #Alfabeto de cinta
q0 = data["initialState"] #Estado inicial
F = data["finalState"] #Estado final
Blanc = data["Blanc"] #Símbolo blanco
delta = data["delta"] #Lista de transiciones //'estado, lectura': [transicion, input, movimiento]
tapeInput = data["tapeInput"] #Input inicial en cadena

# Función para encontrar los cambios en la cinta de la máquina
def delta_transitions(state, char_input):
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

# FUNCIONAMIENTO DE MÁQUINA
tape = [Blanc, Blanc]

using_fibonacci = machine_file == "Fibonacci_machine.json"
if using_fibonacci:
    print("Hemos reconocido que estas ejecutando la máquina de fibonacci.")
    print("Ingresa el valor n (cantidad de veces que se ejecutará la secuencia):")
    n = int(input("n = "))
    ejecucion = "A" * n
    tape.extend(list(ejecucion))
    
tape.extend(list(tapeInput))
tape.extend([Blanc, Blanc])

print("\nEjecutando máquina...\n")
state = q0
index = 2 #punto de inicio de la cinta
char_tape = tape[index] #caracter leido actualmente en la cinta

while not (state == F and char_tape == Blanc):
    changes = delta_transitions(state, char_tape)
    state = changes[0]
    tape[index] = changes[1]
    index += int(changes[2])
    if index == len(tape) - 1:
        tape.extend([Blanc])
    char_tape = tape[index]

tape_result = "".join(tape)
result = tape_result.replace(Blanc, "")

print(f"Resultado en la cinta: {result}\n")

if using_fibonacci:
    valores = result.split("X")[:-1]  # Ignorar el último elemento vacío
    print("Secuencia Fibonacci: " + " ".join(str(valor.count("1")) for valor in valores))


