# Autores: Angel Sanabria, Pablo Vásquez
# CC2016 - Algoritmos y Estructura de Datos
# Hoja de Trabajo No. 10 - Implementación de Grafos y Algoritmo de Floyd

import numpy as np

# Variables globales
vertices = []  # Lista de vértices (ciudades)
adj_matrix = None  # Matriz de adyacencia
path_matrix = None  # Matriz de caminos para Floyd-Warshall
weather_weights = {}  # Diccionario para almacenar pesos según condiciones climáticas

def read_graph(filename):
    """
    Lee el grafo desde un archivo y inicializa la matriz de adyacencia.

    @param filename Nombre del archivo de texto que contiene los datos del grafo.
    @throws FileNotFoundError Si el archivo especificado no existe.
    @throws Exception Si ocurre un error al leer el archivo.
    """
    global vertices, adj_matrix, weather_weights
    try:
        with open(filename, 'r') as file:
            for line in file:
                city1, city2, normal, rain, snow, storm = line.strip().split()
                if city1 not in vertices:
                    vertices.append(city1)
                if city2 not in vertices:
                    vertices.append(city2)
                weather_weights[(city1, city2)] = {
                    'normal': float(normal),
                    'rain': float(rain),
                    'snow': float(snow),
                    'storm': float(storm)
                }
        
        n = len(vertices)
        adj_matrix = np.full((n, n), float('inf'))
        np.fill_diagonal(adj_matrix, 0)
        
        # Inicializa la matriz con pesos de clima normal
        for (city1, city2), weights in weather_weights.items():
            i = vertices.index(city1)
            j = vertices.index(city2)
            adj_matrix[i][j] = weights['normal']
            
    except FileNotFoundError:
        print("Archivo no encontrado. Asegúrese de que el archivo exista.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def floyd_warshall():
    """
    Implementa el algoritmo de Floyd-Warshall para encontrar los caminos más cortos entre todos los pares de vértices.

    @return Matriz de distancias más cortas entre todos los pares de vértices.
    """
    global path_matrix
    n = len(vertices)
    path_matrix = np.full((n, n), -1, dtype=int)
    dist = adj_matrix.copy()

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    path_matrix[i][j] = k

    return dist

def reconstruct_path(i, j, path):
    """
    Reconstruye el camino más corto entre dos vértices usando la matriz de caminos.

    @param i Índice del vértice inicial.
    @param j Índice del vértice final.
    @param path Lista para almacenar los índices de los vértices en el camino.
    """
    if path_matrix[i][j] == -1:
        if i != j:
            path.append(j)
        return
    reconstruct_path(i, path_matrix[i][j], path)
    reconstruct_path(path_matrix[i][j], j, path)

def get_path(start, end):
    """
    Obtiene el camino más corto entre dos ciudades.

    @param start Nombre de la ciudad de origen.
    @param end Nombre de la ciudad de destino.
    @return Tupla con la lista de ciudades en el camino más corto y la distancia total.
            Retorna (None, None) si las ciudades no existen, o (None, inf) si no hay camino.
    """
    if start not in vertices or end not in vertices:
        return None, None
    
    i = vertices.index(start)
    j = vertices.index(end)
    dist = floyd_warshall()
    
    if dist[i][j] == float('inf'):
        return None, float('inf')
        
    path = [i]
    reconstruct_path(i, j, path)
    path = [vertices[i] for i in path]
    return path, dist[i][j]

def find_center():
    """
    Encuentra el centro del grafo, el vértice con mínima excentricidad.

    @return Tupla con el nombre del vértice central y su excentricidad.
    """
    dist = floyd_warshall()
    eccentricities = np.max(dist, axis=1)
    min_eccentricity = np.min(eccentricities[np.isfinite(eccentricities)])
    center_idx = np.where(eccentricities == min_eccentricity)[0][0]
    return vertices[center_idx], min_eccentricity

def update_weather(city1, city2, weather):
    """
    Actualiza el peso de una arista según la condición climática especificada.

    @param city1 Nombre de la primera ciudad.
    @param city2 Nombre de la segunda ciudad.
    @param weather Condición climática ('normal', 'rain', 'snow', 'storm').
    """
    global adj_matrix
    if (city1, city2) in weather_weights and weather in weather_weights[(city1, city2)]:
        i = vertices.index(city1)
        j = vertices.index(city2)
        adj_matrix[i][j] = weather_weights[(city1, city2)][weather]
    else:
        print("Par de ciudades o condición climática inválida.")

def add_edge(city1, city2, normal, rain, snow, storm):
    """
    Agrega una nueva arista al grafo con pesos para todas las condiciones climáticas.

    @param city1 Nombre de la primera ciudad.
    @param city2 Nombre de la segunda ciudad.
    @param normal Tiempo en horas para clima normal.
    @param rain Tiempo en horas para lluvia.
    @param snow Tiempo en horas para nieve.
    @param storm Tiempo en horas para tormenta.
    """
    global adj_matrix, weather_weights
    if city1 not in vertices:
        vertices.append(city1)
        n = len(vertices)
        new_matrix = np.full((n, n), float('inf'))
        np.fill_diagonal(new_matrix, 0)
        new_matrix[:-1, :-1] = adj_matrix
        adj_matrix = new_matrix
    if city2 not in vertices:
        vertices.append(city2)
        n = len(vertices)
        new_matrix = np.full((n, n), float('inf'))
        np.fill_diagonal(new_matrix, 0)
        new_matrix[:-1, :-1] = adj_matrix
        adj_matrix = new_matrix
    
    i = vertices.index(city1)
    j = vertices.index(city2)
    adj_matrix[i][j] = float(normal)
    weather_weights[(city1, city2)] = {
        'normal': float(normal),
        'rain': float(rain),
        'snow': float(snow),
        'storm': float(storm)
    }

def remove_edge(city1, city2):
    """
    Elimina una arista del grafo.

    @param city1 Nombre de la primera ciudad.
    @param city2 Nombre de la segunda ciudad.
    """
    global adj_matrix
    if city1 in vertices and city2 in vertices:
        i = vertices.index(city1)
        j = vertices.index(city2)
        adj_matrix[i][j] = float('inf')
        weather_weights.pop((city1, city2), None)
    else:
        print("Par de ciudades inválido.")

def print_adjacency_matrix():
    """
    Imprime la matriz de adyacencia del grafo.
    """
    print("\nMatriz de Adyacencia:")
    print(" " * 10, end="")
    for city in vertices:
        print(f"{city:>10}", end="")
    print()
    for i, row in enumerate(adj_matrix):
        print(f"{vertices[i]:>10}", end="")
        for val in row:
            if val == float('inf'):
                print(f"{'inf':>10}", end="")
            else:
                print(f"{val:>10.1f}", end="")
        print()

def main():
    """
    Bucle principal del programa que maneja la interacción con el usuario.
    """
    filename = "logistica.txt"
    read_graph(filename)
    
    while True:
        print("\n=== Sistema de Rutas Logísticas ===")
        print("1. Encontrar el camino más corto entre dos ciudades")
        print("2. Encontrar el centro del grafo")
        print("3. Modificar el grafo")
        print("4. Salir")
        print("5. Mostrar matriz de adyacencia")
        choice = input("Ingrese su opción (1-5): ")
        
        if choice == '1':
            city1 = input("Ingrese la ciudad de origen: ")
            city2 = input("Ingrese la ciudad de destino: ")
            path, distance = get_path(city1, city2)
            if path:
                print(f"Camino más corto: {' -> '.join(path)}")
                print(f"Distancia: {distance:.1f} horas")
            else:
                print("No existe un camino entre estas ciudades.")
                
        elif choice == '2':
            center, eccentricity = find_center()
            print(f"El centro del grafo es: {center} con excentricidad {eccentricity:.1f}")
                
        elif choice == '3':
            print("\nOpciones de modificación:")
            print("a. Interrumpir tráfico entre dos ciudades")
            print("b. Establecer nueva conexión entre dos ciudades")
            print("c. Cambiar condición climática")
            mod_choice = input("Seleccione una opción (a-c): ")
            
            if mod_choice == 'a':
                city1 = input("Ciudad 1: ")
                city2 = input("Ciudad 2: ")
                remove_edge(city1, city2)
                print("Arista eliminada.")
                
            elif mod_choice == 'b':
                city1 = input("Ciudad 1: ")
                city2 = input("Ciudad 2: ")
                normal = input("Tiempo normal (horas): ")
                rain = input("Tiempo con lluvia (horas): ")
                snow = input("Tiempo con nieve (horas): ")
                storm = input("Tiempo con tormenta (horas): ")
                add_edge(city1, city2, normal, rain, snow, storm)
                print("Arista agregada.")
                
            elif mod_choice == 'c':
                city1 = input("Ciudad 1: ")
                city2 = input("Ciudad 2: ")
                weather = input("Condición climática (normal, rain, snow, storm): ")
                update_weather(city1, city2, weather)
                print("Peso actualizado.")
                
        elif choice == '4':
            print("Saliendo del programa...")
            break
            
        elif choice == '5':
            print_adjacency_matrix()
            
        else:
            print("Opción inválida. Intente de nuevo.")

# Ejecutar el programa directamente
if __name__ == "__main__":
    main()