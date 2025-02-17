# Importación de librerías necesarias
import json  # Para cargar datos JSON
import time  # Para medir tiempos de ejecución
import numpy as np  # Para operaciones numéricas
import matplotlib.pyplot as plt

def delta_transitions(state, char_input, delta):
    """
    Calcula la transición de estado según la función delta de la máquina de Turing
    
    Args:
        state: Estado actual de la máquina
        char_input: Carácter actual en la cinta
        delta: Diccionario de transiciones
    
    Returns:
        Lista con el nuevo estado, símbolo a escribir y dirección del movimiento
    """
    key_value = f"{state}, {char_input}"
    changes = delta.get(key_value, []).copy()
    
    if len(changes) == 0:
        return changes

    # Convierte las direcciones simbólicas (S,R,L) a valores numéricos (0,1,-1)
    if changes[2] == "S":
        changes[2] = "0"  # Stay (no moverse)
    elif changes[2] == "R":
        changes[2] = "1"  # Right (mover derecha)
    elif changes[2] == "L":
        changes[2] = "-1"  # Left (mover izquierda)
    
    return changes

def run_fibonacci_machine(n, machine_data):
    """
    Ejecuta la máquina de Turing que genera la secuencia de Fibonacci
    
    Args:
        n: Número de términos de Fibonacci a generar
        machine_data: Diccionario con la configuración de la máquina
    
    Returns:
        Lista con la secuencia de Fibonacci generada
    """
    # Extracción de los componentes de la máquina
    Q = machine_data["states"]  # Conjunto de estados
    sigma = machine_data["alphabet"]  # Alfabeto de entrada
    gamma = machine_data["tapeAlphabet"]  # Alfabeto de la cinta
    q0 = machine_data["initialState"]  # Estado inicial
    F = machine_data["finalState"]  # Estado final
    Blanc = machine_data["Blanc"]  # Símbolo blanco
    delta = machine_data["delta"]  # Función de transición
    tapeInput = machine_data["tapeInput"]  # Entrada inicial en la cinta

    # Inicialización de la cinta
    tape = [Blanc, Blanc]
    ejecucion = "A" * n  # Genera la cadena de entrada según n
    tape.extend(list(ejecucion))
    tape.extend(list(tapeInput))
    tape.extend([Blanc, Blanc])

    # Configuración inicial
    state = q0
    index = 2  # Posición inicial del cabezal
    char_tape = tape[index]

    # Bucle principal de ejecución
    while not (state == F and char_tape == Blanc):
        changes = delta_transitions(state, char_tape, delta)
        if not changes:  # Si no hay transición definida, terminar
            break
        # Actualizar estado y cinta
        state = changes[0]
        tape[index] = changes[1]
        index += int(changes[2])
        # Extender la cinta si es necesario
        if index == len(tape) - 1:
            tape.extend([Blanc])
        char_tape = tape[index]

    # Procesar resultado
    tape_result = "".join(tape)
    result = tape_result.replace(Blanc, "")
    valores = result.split("X")[:-1]
    fibonacci_sequence = [valor.count("1") for valor in valores]
    return fibonacci_sequence

def measure_execution_time(n, machine_data):
    """
    Mide el tiempo de ejecución de la máquina de Fibonacci
    
    Args:
        n: Número de términos a generar
        machine_data: Configuración de la máquina
    
    Returns:
        Tupla con (tiempo_ejecución, secuencia_fibonacci)
    """
    start_time = time.time()
    fibonacci_sequence = run_fibonacci_machine(n, machine_data)
    end_time = time.time()
    return end_time - start_time, fibonacci_sequence

# Bloque principal de ejecución
# Cargar la configuración de la máquina desde archivo JSON
with open("Fibonacci_machine.json", "r", encoding="utf-8") as file:
    machine_data = json.load(file)

# Configuración de pruebas
input_sizes = np.arange(1,18)  # Probar con n del 1 al 10
execution_times = []
fibonacci_results = []

print("Realizando mediciones iniciales...")
# Ejecutar pruebas para diferentes valores de n
for n in input_sizes:
    time_taken, fib_sequence = measure_execution_time(n, machine_data)
    execution_times.append(time_taken)
    fibonacci_results.append(fib_sequence)
    print(f"n = {n}: {time_taken:.4f} segundos, Fibonacci: {fib_sequence}")


# [Análisis y Visualización]
plt.figure(figsize=(12, 6))

# Gráfico de dispersión
plt.subplot(1, 2, 1)
plt.scatter(input_sizes, execution_times, color='blue', label='Tiempos medidos')

# Ajuste polinomial
degrees = [1, 2, 3]  # Probar diferentes grados
best_r2 = -1
best_degree = 1
best_coeffs = None

for degree in degrees:
    coeffs = np.polyfit(input_sizes, execution_times, degree)
    poly = np.poly1d(coeffs)
    y_pred = poly(input_sizes)
    r2 = 1 - (np.sum((execution_times - y_pred) ** 2) / 
              np.sum((execution_times - np.mean(execution_times)) ** 2))
    
    if r2 > best_r2:
        best_r2 = r2
        best_degree = degree
        best_coeffs = coeffs

# Graficar mejor ajuste
x_continuous = np.linspace(min(input_sizes), max(input_sizes), 100)
best_poly = np.poly1d(best_coeffs)
plt.plot(x_continuous, best_poly(x_continuous), color='red', 
         label=f'Ajuste polinomial (grado {best_degree})')

plt.xlabel('Tamaño de entrada (n)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.title('Análisis de Tiempo de Ejecución')
plt.legend()
plt.grid(True)

# Gráfico de valores Fibonacci generados
plt.subplot(1, 2, 2)
for i, sequence in enumerate(fibonacci_results):
    plt.plot(range(len(sequence)), sequence, marker='o', 
             label=f'n={i+1}', alpha=0.7)
plt.xlabel('Índice en la secuencia')
plt.ylabel('Valor de Fibonacci')
plt.title('Secuencias de Fibonacci Generadas')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

plt.tight_layout()
plt.savefig('gráfica_mejor_regresión.png', bbox_inches='tight')

print("\nResultados del análisis:")
print(f"Mejor grado polinomial: {best_degree}")
print(f"R² Score: {best_r2:.4f}")
print(f"Coeficientes del polinomio: {best_coeffs}")

# Determinar complejidad aproximada
if best_degree == 3:
    print("El análisis sugiere una complejidad O(n³)")
elif best_degree == 2:
    print("El análisis sugiere una complejidad O(n²)")
else:
    print("El análisis sugiere una complejidad O(n)")

# [Análisis y Visualización]
plt.figure(figsize=(12, 6))

# Gráfico de dispersión y regresiones
plt.subplot(1, 2, 1)
plt.scatter(input_sizes, execution_times, color='blue', label='Tiempos medidos')

# Definir colores para cada grado
colors = ['red', 'green', 'purple']
degrees = [1, 2, 3]

# Calcular y graficar todas las regresiones
r2_scores = []
for degree, color in zip(degrees, colors):
    # Calcular coeficientes del polinomio
    coeffs = np.polyfit(input_sizes, execution_times, degree)
    poly = np.poly1d(coeffs)
    
    # Calcular R²
    y_pred = poly(input_sizes)
    r2 = 1 - (np.sum((execution_times - y_pred) ** 2) / 
              np.sum((execution_times - np.mean(execution_times)) ** 2))
    r2_scores.append(r2)
    
    # Graficar regresión
    x_continuous = np.linspace(min(input_sizes), max(input_sizes), 100)
    plt.plot(x_continuous, poly(x_continuous), color=color, 
             label=f'Grado {degree} (R² = {r2:.4f})')

plt.xlabel('Tamaño de entrada (n)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.title('Análisis de Tiempo de Ejecución')
plt.legend()
plt.grid(True)

# Gráfico de valores Fibonacci generados
plt.subplot(1, 2, 2)
for i, sequence in enumerate(fibonacci_results):
    plt.plot(range(len(sequence)), sequence, marker='o', 
             label=f'n={i+1}', alpha=0.7)
plt.xlabel('Índice en la secuencia')
plt.ylabel('Valor de Fibonacci')
plt.title('Secuencias de Fibonacci Generadas')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)

plt.tight_layout()
plt.savefig('gráfica_con_todas_regresiones.png', bbox_inches='tight')
