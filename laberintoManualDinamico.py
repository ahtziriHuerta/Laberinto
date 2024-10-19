import tkinter as tk
from tkinter import simpledialog, messagebox

# Función para dibujar una celda en la GUI
def dibujar_celda(canvas, x, y, color, cell_size):
    canvas.create_rectangle(y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, fill=color)

# Función para comprobar si la nueva posición es válida
def es_camino_valido(laberinto, x, y):
    if 0 <= x < len(laberinto) and 0 <= y < len(laberinto[0]):
        return laberinto[x][y] == 0 or laberinto[x][y] == 2 or laberinto[x][y] in (3, 4, 111)  # Celdas especiales y normales
    return False

# Función de teletransportación
def teletransportar(laberinto, x, y):
    if laberinto[x][y] == 3:
        for i in range(len(laberinto)):
            for j in range(len(laberinto[0])):
                if laberinto[i][j] == 4:
                    return i, j
    elif laberinto[x][y] == 4:
        for i in range(len(laberinto)):
            for j in range(len(laberinto[0])):
                if laberinto[i][j] == 3:
                    return i, j
    return x, y  # Si no hay teletransportación

# Función para manejar la trivia
def trivia(root):
    pregunta = "¿Cuál es la capital de Francia?"
    respuesta_correcta = "paris"

    while True:
        respuesta_usuario = simpledialog.askstring("Trivia", pregunta)

        if respuesta_usuario is None:  # Si el usuario presiona cancelar
            root.quit()  # Cerramos la ventana principal
            return False  # Devolvemos False para indicar que se ha cancelado
        elif respuesta_usuario.lower() == respuesta_correcta.lower():
            return True  # Trivia correcta
        else:
            messagebox.showerror("Error", "Respuesta incorrecta. Inténtalo de nuevo.")

# Función para mover al jugador
def mover_jugador(laberinto, canvas, jugador_pos, nueva_x, nueva_y, cell_size, root, memo):
    x, y = jugador_pos
    if es_camino_valido(laberinto, nueva_x, nueva_y):
        # Pintar de amarillo la celda por la que ya pasó
        dibujar_celda(canvas, x, y, "yellow", cell_size)

        # Si entra en una celda de trivia (111)
        if laberinto[nueva_x][nueva_y] == 111:
            if not trivia(root):
                return

        # Si entra en una celda de teletransportación (3 o 4)
        if laberinto[nueva_x][nueva_y] in (3, 4):
            nueva_x, nueva_y = teletransportar(laberinto, nueva_x, nueva_y)

        # Verificar si el jugador ha llegado a la salida
        if laberinto[nueva_x][nueva_y] == 2:
            messagebox.showinfo("¡Éxito!", "¡Encontraste la salida!")
            root.destroy()
            return

        # Actualizar la posición del jugador
        jugador_pos[0], jugador_pos[1] = nueva_x, nueva_y
        # Dibujar al jugador en la nueva posición
        dibujar_celda(canvas, nueva_x, nueva_y, "cyan", cell_size)

        # Comprobar si se puede llegar a la salida desde la nueva posición
        if puede_llegar_a_salida(laberinto, nueva_x, nueva_y, memo):
            print(f"El jugador puede llegar a la salida desde la posición ({nueva_x}, {nueva_y})")
        else:
            print(f"El jugador NO puede llegar a la salida desde la posición ({nueva_x}, {nueva_y})")
    else:
        print(f"No se puede mover a la posición ({nueva_x}, {nueva_y}) porque es inválida.")

# Programación dinámica para verificar si se puede llegar a la salida
def puede_llegar_a_salida(laberinto, x, y, memo):
    if x < 0 or y < 0 or x >= len(laberinto) or y >= len(laberinto[0]):
        return False  # Fuera de los límites del laberinto
    
    if laberinto[x][y] == 1:  # Pared
        print(f"Posición ({x}, {y}) es una pared.")
        return False
    
    if laberinto[x][y] == 2:  # Salida encontrada
        print(f"Salida encontrada en ({x}, {y})")
        return True
    
    if memo[x][y] is not None:  # Si ya calculamos para esta celda
        print(f"Posición ({x}, {y}) ya fue calculada previamente. Valor: {memo[x][y]}")
        return memo[x][y]

    # Marcar como visitado temporalmente
    print(f"Calculando para posición ({x}, {y}) por primera vez.")
    memo[x][y] = False

    # Intentamos moverse en 4 direcciones y almacenamos el resultado en memo[x][y]
    memo[x][y] = (puede_llegar_a_salida(laberinto, x + 1, y, memo) or  # Abajo
                  puede_llegar_a_salida(laberinto, x - 1, y, memo) or  # Arriba
                  puede_llegar_a_salida(laberinto, x, y + 1, memo) or  # Derecha
                  puede_llegar_a_salida(laberinto, x, y - 1, memo))    # Izquierda
    
    print(f"Resultado de memo[{x}][{y}] = {memo[x][y]}")
    return memo[x][y]

# Función para manejar los eventos del teclado
def manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root, memo):
    x, y = jugador_pos
    if event.keysym == "Up":
        mover_jugador(laberinto, canvas, jugador_pos, x - 1, y, cell_size, root, memo)
    elif event.keysym == "Down":
        mover_jugador(laberinto, canvas, jugador_pos, x + 1, y, cell_size, root, memo)
    elif event.keysym == "Left":
        mover_jugador(laberinto, canvas, jugador_pos, x, y - 1, cell_size, root, memo)
    elif event.keysym == "Right":
        mover_jugador(laberinto, canvas, jugador_pos, x, y + 1, cell_size, root, memo)

# Función principal para ejecutar la resolución del laberinto con visualización
def ejecutar_laberinto_visual():
    # Dimensiones y tamaño de las celdas
    cell_size = 50
    laberinto = [
        [0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 1, 0, 111, 0, 0, 3],
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 4, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 2]  # Añadido un 0 al final para igualar el número de columnas
    ]
    
    # Posición inicial del jugador
    jugador_pos = [0, 0]

    # Tabla de memoización
    memo = [[None for _ in range(len(laberinto[0]))] for _ in range(len(laberinto))]

    # Crear la ventana y el canvas
    root = tk.Tk()
    root.title("Laberinto Interactivo")
    canvas = tk.Canvas(root, width=len(laberinto[0]) * cell_size, height=len(laberinto) * cell_size)
    canvas.pack()

    # Dibujar el laberinto inicial
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == 1:  # Pared
                dibujar_celda(canvas, i, j, "black", cell_size)
            elif laberinto[i][j] == 2:  # Salida
                dibujar_celda(canvas, i, j, "green", cell_size)
            elif laberinto[i][j] == 3 or laberinto[i][j] == 4:  # Teletransportación
                dibujar_celda(canvas, i, j, "blue", cell_size)
            elif laberinto[i][j] == 111:  # Trivia
                dibujar_celda(canvas, i, j, "orange", cell_size)
            else:  # Camino (celdas con valor 0)
                dibujar_celda(canvas, i, j, "white", cell_size)

    # Dibujar al jugador en la posición inicial
    dibujar_celda(canvas, jugador_pos[0], jugador_pos[1], "cyan", cell_size)

    # Vincular las teclas de flecha al movimiento del jugador
    root.bind("<Up>", lambda event: manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root, memo))
    root.bind("<Down>", lambda event: manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root, memo))
    root.bind("<Left>", lambda event: manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root, memo))
    root.bind("<Right>", lambda event: manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root, memo))

    # Iniciar la interfaz gráfica
    root.mainloop()

# Ejecutamos la función principal
ejecutar_laberinto_visual()
