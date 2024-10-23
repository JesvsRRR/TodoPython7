import time
import os
from pathlib import Path
import ast  # Para evaluar de manera segura las listas en formato string

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def counting_sort(arr):
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    count = [0] * range_val
    output = [0] * len(arr)
    
    for i in arr:
        count[i - min_val] += 1
    
    for i in range(1, len(count)):
        count[i] += count[i-1]
    
    for i in range(len(arr)-1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return output

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    
    if l < n and arr[l] > arr[largest]:
        largest = l
    
    if r < n and arr[r] > arr[largest]:
        largest = r
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)
    
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    
    return arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
        
        merge_sort(L)
        merge_sort(R)
        
        i = j = k = 0
        
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr)//2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def read_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read().strip()
        # Usar ast.literal_eval para evaluar de manera segura la lista
        return ast.literal_eval(content)

def measure_sorting_time(sort_func, arr):
    arr_copy = arr.copy()
    start_time = time.time()
    sort_func(arr_copy)
    end_time = time.time()
    return end_time - start_time

def main():
    # Solicitar la ruta de la carpeta al usuario
    folder_path = input("Ingrese la ruta de la carpeta con los archivos: ").strip()
    
    # Si no se ingresa una ruta, usar la carpeta actual
    if not folder_path:
        folder_path = "."
    
    # Convertir la ruta a objeto Path
    folder_path = Path(folder_path)
    
    # Verificar si la carpeta existe
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"Error: La carpeta {folder_path} no existe o no es una carpeta válida")
        return
    
    sizes = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 
             10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
    
    algorithms = {
        'Bubble Sort': bubble_sort,
        'Counting Sort': counting_sort,
        'Heap Sort': heap_sort,
        'Insertion Sort': insertion_sort,
        'Merge Sort': merge_sort,
        'Quick Sort': quick_sort,
        'Selection Sort': selection_sort
    }
    
    results = {algo_name: [] for algo_name in algorithms}
    
    # Crear una lista para almacenar los tamaños encontrados
    found_sizes = []
    
    for size in sizes:
        filename = f'file_{size}.txt'
        filepath = folder_path / filename
        
        if not filepath.exists():
            print(f"Archivo {filename} no encontrado en {folder_path}")
            continue
            
        found_sizes.append(size)
        print(f"Procesando {filename}...")
        
        try:
            arr = read_file(filepath)
            if len(arr) != size:
                print(f"Advertencia: {filename} contiene {len(arr)} elementos, se esperaban {size}")
            
            for algo_name, algo_func in algorithms.items():
                time_taken = measure_sorting_time(algo_func, arr)
                results[algo_name].append(time_taken)
                print(f"  {algo_name}: {time_taken:.4f}s")
                
        except Exception as e:
            print(f"Error al procesar {filename}: {str(e)}")
            continue
    
    print("\nResultados finales:")
    print("Tamaños procesados:", " ".join(map(str, found_sizes)))
    print("-" * 80)
    
    # Imprimir resultados
    for algo_name, times in results.items():
        print(f"{algo_name}: {' '.join([f'{t:.4f}s' for t in times])}")
    
    # Guardar resultados en un archivo
    try:
        with open('resultados_ordenamiento.txt', 'w') as f:
            f.write("Resultados del análisis de algoritmos de ordenamiento\n")
            f.write("=" * 50 + "\n\n")
            f.write("Tamaños procesados: " + " ".join(map(str, found_sizes)) + "\n\n")
            for algo_name, times in results.items():
                f.write(f"{algo_name}: {' '.join([f'{t:.4f}s' for t in times])}\n")
        print("\nLos resultados han sido guardados en 'resultados_ordenamiento.txt'")
    except Exception as e:
        print(f"\nError al guardar los resultados en archivo: {str(e)}")

if __name__ == "__main__":
    main()
