import tkinter as tk
import time

# Función para resolver el laberinto utilizando recursión y programación dinámica (memoización)
def resolver_laberinto(laberinto, x, y, solucion, memo, canvas, cell_size, delay=500):
    # Verificamos si estamos fuera de los límites del laberinto
    if x < 0 or y < 0 or x >= len(laberinto) or y >= len(laberinto[0]):
        return False  # Si estamos fuera de los límites, no es una solución válida

    # Si llegamos a la salida
    if laberinto[x][y] == 2:
        solucion[x][y] = 2  # Marcamos la celda de salida en la solución
        dibujar_celda(canvas, x, y, "green", cell_size)  # Mostramos la salida
        canvas.update()
        time.sleep(delay / 1000)  # Pausa para visualización paso a paso
        return True  # Indicamos que hemos encontrado la salida

    
    # Comprobamos si ya conocemos la solución desde esta celda (Memoización)
    if memo[x][y] != -1:
        return memo[x][y]  # Si ya lo hemos calculado, devolvemos el resultado almacenado

    # Comprobamos si es un camino válido
    if es_camino_valido(laberinto, x, y):
        solucion[x][y] = 1  # Marcamos la celda actual como parte del camino
        dibujar_celda(canvas, x, y, "yellow", cell_size)  # Mostramos el camino en amarillo
        canvas.update()
        time.sleep(delay / 1000)  # Pausa para visualización paso a paso

        # Verificamos si estamos en una celda de teletransportación
        if laberinto[x][y] == 3 or laberinto[x][y] == 4:
            nueva_pos = teletransportar(laberinto, laberinto[x][y])
            # Actualizamos las coordenadas a la nueva posición y seguimos
            x, y = nueva_pos[0], nueva_pos[1]
            solucion[x][y] = 1  # Marcamos la nueva celda teletransportada como parte del camino
            dibujar_celda(canvas, x, y, "yellow", cell_size)
            canvas.update()
            time.sleep(delay / 1000)

        # Movemos hacia la derecha
        if resolver_laberinto(laberinto, x, y + 1, solucion, memo, canvas, cell_size, delay):
            memo[x][y] = True  # Guardamos el resultado para futuras referencias
            return True

        # Movemos hacia abajo
        if resolver_laberinto(laberinto, x + 1, y, solucion, memo, canvas, cell_size, delay):
            memo[x][y] = True  # Guardamos el resultado
            return True

        # Movemos hacia la izquierda
        if resolver_laberinto(laberinto, x, y - 1, solucion, memo, canvas, cell_size, delay):
            memo[x][y] = True  # Guardamos el resultado
            return True

        # Movemos hacia arriba
        if resolver_laberinto(laberinto, x - 1, y, solucion, memo, canvas, cell_size, delay):
            memo[x][y] = True  # Guardamos el resultado
            return True

        # Si ninguna dirección es válida, retrocedemos
        solucion[x][y] = 0  # Marcamos la celda como no parte del camino
        dibujar_celda(canvas, x, y, "white", cell_size)  # Borramos el camino si retrocedemos
        canvas.update()
        time.sleep(delay / 1000)  # Pausa para visualización paso a paso
        memo[x][y] = False  # Guardamos que no hay solución desde esta celda
        return False

    memo[x][y] = False  # Guardamos que no es válido continuar desde esta celda
    return False

# Función que comprueba si una celda es válida
def es_camino_valido(laberinto, x, y):
    if x >= 0 and y >= 0 and x < len(laberinto) and y < len(laberinto[0]):  # Verifica si está dentro de los límites
        if laberinto[x][y] == 111:  # Trivia
            return trivia()  # Si responde correctamente, puede continuar
        elif laberinto[x][y] == 3 or laberinto[x][y] == 4:  # Celdas de teletransportación
            return True  # Permitimos continuar si es una celda de teletransportación
        elif laberinto[x][y] == 0 or laberinto[x][y] == 2:  # Camino válido o salida
            return True  # Las celdas con 0 (camino) o 2 (salida) son válidas
    return False  # Si no es válida, no podemos avanzar

# Función de teletransportación
def teletransportar(laberinto, valor_actual):
    destino = 4 if valor_actual == 3 else 3
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == destino:
                return (i, j)

# Dibujar una celda en la GUI
def dibujar_celda(canvas, x, y, color, cell_size):
    canvas.create_rectangle(y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, fill=color)

# Función para manejar trivia en celdas especiales
def trivia():
    return True  # Para simplificar, asumimos que la trivia siempre es correcta

# Función principal para ejecutar la resolución del laberinto con visualización
def ejecutar_laberinto_visual():
    # Dimensiones y tamaño de las celdas
    cell_size = 50
    delay = 500  # Delay en milisegundos entre pasos
    laberinto = [
        [0, 1, 0, 0, 0, 1],
        [111, 1, 1, 0, 1, 1],
        [3, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 1, 0],
        [1, 0, 1, 0, 4, 0],
        [1, 0, 0, 0, 0, 2]
    ]
    solucion = [[0 for _ in range(len(laberinto[0]))] for _ in range(len(laberinto))]
    memo = [[-1 for _ in range(len(laberinto[0]))] for _ in range(len(laberinto))]

    # Crear la ventana y el canvas
    root = tk.Tk()
    root.title("Visualización del Laberinto - Paso a Paso")
    canvas = tk.Canvas(root, width=len(laberinto[0]) * cell_size, height=len(laberinto) * cell_size)
    canvas.pack()

    # Dibujar el laberinto inicial
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == 1:  # Pared
                dibujar_celda(canvas, i, j, "black", cell_size)
            elif laberinto[i][j] == 111:  # Trivia
                dibujar_celda(canvas, i, j, "orange", cell_size)
            elif laberinto[i][j] == 3 or laberinto[i][j] == 4:  # Teletransportación
                dibujar_celda(canvas, i, j, "blue", cell_size)
            elif laberinto[i][j] == 2:  # Salida
                dibujar_celda(canvas, i, j, "green", cell_size)

    # Resolver el laberinto con visualización
    resolver_laberinto(laberinto, 0, 0, solucion, memo, canvas, cell_size, delay)

    # Iniciar la interfaz gráfica
    root.mainloop()

# Ejecutamos la función principal
ejecutar_laberinto_visual()

