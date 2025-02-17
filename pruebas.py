import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# [Código a ejecutar]
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# [Pruebas a realizar]
def measure_time(func, input_size):
    # Crear array aleatorio
    arr = np.random.randint(0, 1000, size=input_size)
    
    # Medir tiempo de ejecución
    start_time = time.time()
    func(arr.copy())  # Usamos copy para no modificar el array original
    end_time = time.time()
    
    return end_time - start_time

# Tamaños de entrada para pruebas
input_sizes = np.linspace(100, 2000, 20, dtype=int)
execution_times = []

# Realizar mediciones
for size in input_sizes:
    time_taken = measure_time(bubble_sort, size)
    execution_times.append(time_taken)

# [Análisis]
# Convertir a arrays de numpy para el análisis
X = input_sizes.reshape(-1, 1)
y = np.array(execution_times)

# Crear el modelo de regresión polinomial
degrees = [1, 2, 3]  # Probaremos diferentes grados
best_degree = 1
best_r2 = 0

for degree in degrees:
    poly_features = PolynomialFeatures(degree=degree)
    X_poly = poly_features.fit_transform(X)
    
    model = LinearRegression()
    model.fit(X_poly, y)
    
    y_pred = model.predict(X_poly)
    r2 = r2_score(y, y_pred)
    
    if r2 > best_r2:
        best_degree = degree
        best_r2 = r2
        best_model = model
        best_poly_features = poly_features

# [Diagrama de dispersión y regresión]
plt.figure(figsize=(10, 6))
plt.scatter(input_sizes, execution_times, color='blue', label='Datos medidos')

# Generar puntos para la línea de regresión
X_continuous = np.linspace(min(input_sizes), max(input_sizes), 100).reshape(-1, 1)
X_continuous_poly = best_poly_features.transform(X_continuous)
y_continuous = best_model.predict(X_continuous_poly)

plt.plot(X_continuous, y_continuous, color='red', 
         label=f'Regresión polinomial (grado {best_degree})')

plt.xlabel('Tamaño de entrada (n)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.title('Análisis de Complejidad: Bubble Sort')
plt.legend()
plt.grid(True)

# Guardar el gráfico
plt.savefig('./complexity_analysis.png')

# Imprimir resultados del análisis
print(f"\nResultados del análisis:")
print(f"Mejor grado polinomial: {best_degree}")
print(f"R² Score: {best_r2:.4f}")

if best_degree == 2:
    print("El análisis sugiere una complejidad O(n²)")
elif best_degree == 3:
    print("El análisis sugiere una complejidad O(n³)")
else:
    print(f"El análisis sugiere una complejidad O(n^{best_degree})")