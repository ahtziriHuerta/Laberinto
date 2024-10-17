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
        # Teletransportar al destino correspondiente (4)
        for i in range(len(laberinto)):
            for j in range(len(laberinto[0])):
                if laberinto[i][j] == 4:
                    return i, j
    elif laberinto[x][y] == 4:
        # Teletransportar al destino correspondiente (3)
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
            # Mostrar un mensaje de error y volver a preguntar
            messagebox.showerror("Error", "Respuesta incorrecta. Inténtalo de nuevo.")

# Mover el jugador a la nueva posición si es válida
def mover_jugador(laberinto, canvas, jugador_pos, nueva_x, nueva_y, cell_size, root):
    x, y = jugador_pos
    if es_camino_valido(laberinto, nueva_x, nueva_y):
        # Limpiar la posición anterior del jugador
        dibujar_celda(canvas, x, y, "white", cell_size)

        # Si entra en una celda de trivia (111)
        if laberinto[nueva_x][nueva_y] == 111:
            if not trivia(root):  # Pasamos 'root' aquí para cerrar la ventana si es necesario
                dibujar_celda(canvas, x, y, "yellow", cell_size)  # Si falla la trivia, se queda en el lugar
                return

        # Si entra en una celda de teletransportación (3 o 4)
        if laberinto[nueva_x][nueva_y] in (3, 4):
            nueva_x, nueva_y = teletransportar(laberinto, nueva_x, nueva_y)

        # Actualizar la posición del jugador
        jugador_pos[0], jugador_pos[1] = nueva_x, nueva_y
        # Dibujar el jugador en la nueva posición
        dibujar_celda(canvas, nueva_x, nueva_y, "yellow", cell_size)
        
        # Verificar si el jugador ha llegado a la salida
        if laberinto[nueva_x][nueva_y] == 2:
            messagebox.showinfo("¡Éxito!", "¡Encontraste la salida!")
            root.destroy()

# Función para manejar los eventos del teclado
def manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root):
    x, y = jugador_pos
    if event.keysym == "Up":
        mover_jugador(laberinto, canvas, jugador_pos, x - 1, y, cell_size, root)
    elif event.keysym == "Down":
        mover_jugador(laberinto, canvas, jugador_pos, x + 1, y, cell_size, root)
    elif event.keysym == "Left":
        mover_jugador(laberinto, canvas, jugador_pos, x, y - 1, cell_size, root)
    elif event.keysym == "Right":
        mover_jugador(laberinto, canvas, jugador_pos, x, y + 1, cell_size, root)

# Función principal para ejecutar la resolución del laberinto con visualización
def ejecutar_laberinto_visual():
    # Dimensiones y tamaño de las celdas
    cell_size = 50
    laberinto = [
        [0, 1, 0, 0, 0, 0, 0, 1, 1,1],
        [0, 1, 1, 0, 1, 1, 0, 0, 1,1],
        [0, 0, 0, 0, 1, 0, 111, 0, 0,3],
        [1, 1, 1, 0, 1, 0, 1, 0, 1,1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0,1],
        [1, 4, 0, 0, 0, 0, 1, 0, 0,1],
        [1, 0, 1, 1, 1, 0, 1, 0, 0,1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0,2]  # Añadido un 0 al final para igualar el número de columnas
    ]
    # Posición inicial del jugador
    jugador_pos = [0, 0]
    
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
                dibujar_celda(canvas, i, j, "white", cell_size)  # Cambiado el color de teletransportación a azul
            elif laberinto[i][j] == 111:  # Trivia
                dibujar_celda(canvas, i, j, "white", cell_size)  # Cambiado el color de trivia a naranja
            else:  # Camino (celdas con valor 0)
                dibujar_celda(canvas, i, j, "white", cell_size)

    # Dibujar al jugador en la posición inicial
    dibujar_celda(canvas, jugador_pos[0], jugador_pos[1], "yellow", cell_size)

    # Vincular las teclas de flecha al movimiento del jugador
    root.bind("<Up>", lambda event: manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root))
    root.bind("<Down>", lambda event: manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root))
    root.bind("<Left>", lambda event: manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root))
    root.bind("<Right>", lambda event: manejar_teclado(event, laberinto, canvas, jugador_pos, cell_size, root))

    # Iniciar la interfaz gráfica
    root.mainloop()

# Ejecutamos la función principal
ejecutar_laberinto_visual()
