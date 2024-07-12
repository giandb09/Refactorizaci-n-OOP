import pygame  # Importa la biblioteca Pygame para la creación de juegos y gráficos.
import heapq   # Importa heapq, una biblioteca para la manipulación de colas de prioridad.

# Definir colores
NEGRO = (0, 0, 0)  # Define el color negro.
BLANCO = (255, 255, 255)  # Define el color blanco.
VERDE = (0, 255, 0)  # Define el color verde.
AZUL = (0, 0, 255)  # Define el color azul.

# Clase para gestionar el mapa
class Mapa:
    def __init__(self, filas, columnas, tamano_celda):
        self.filas = filas  # Número de filas en el mapa.
        self.columnas = columnas  # Número de columnas en el mapa.
        self.tamano_celda = tamano_celda  # Tamaño de cada celda en píxeles.
        
        # Inicializa el mapa con celdas de tipo 'calle'.
        self.mapa = [['calle' for _ in range(columnas)] for _ in range(filas)]
        
        # Carga y escala las imágenes de los obstáculos.
        self.obstaculos = {
            'agua': pygame.transform.scale(pygame.image.load('static/agua.jpg').convert(), (tamano_celda, tamano_celda)),
            'edificio': pygame.transform.scale(pygame.image.load('static/edificio.jpg').convert(), (tamano_celda, tamano_celda)),
            'bache': pygame.transform.scale(pygame.image.load('static/bache.jpg').convert(), (tamano_celda, tamano_celda))
        }
        self.inicio = None  # Coordenadas de inicio.
        self.fin = None  # Coordenadas de fin.

    def agregar_obstaculo(self, x, y, tipo_obstaculo):
        if 0 <= x < self.filas and 0 <= y < self.columnas:  # Verifica si las coordenadas son válidas.
            self.mapa[x][y] = tipo_obstaculo  # Agrega el obstáculo en las coordenadas especificadas.
        else:
            print("Coordenadas inválidas")  # Mensaje de error si las coordenadas son inválidas.

    def eliminar_obstaculo(self, x, y):
        if 0 <= x < self.filas and 0 <= y < self.columnas:  # Verifica si las coordenadas son válidas.
            self.mapa[x][y] = 'calle'  # Elimina el obstáculo en las coordenadas especificadas.
        else:
            print("Coordenadas inválidas")  # Mensaje de error si las coordenadas son inválidas.

    def es_accesible(self, x, y):
        return 0 <= x < self.filas and 0 <= y < self.columnas and self.mapa[x][y] == 'calle'  # Verifica si la celda es accesible.

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)  # Limpiar la pantalla antes de dibujar.

        for x in range(self.filas):  # Para cada fila.
            for y in range(self.columnas):  # Para cada columna.
                # Dibujar fondo de la celda.
                rect = pygame.Rect(y * self.tamano_celda, x * self.tamano_celda, self.tamano_celda, self.tamano_celda)
                pygame.draw.rect(pantalla, NEGRO, rect)

                # Dibujar borde de la celda.
                pygame.draw.rect(pantalla, BLANCO, rect, 1)

                # Dibujar contenido de la celda según su tipo.
                if self.mapa[x][y] == 'agua':
                    pantalla.blit(self.obstaculos['agua'], rect)
                elif self.mapa[x][y] == 'edificio':
                    pantalla.blit(self.obstaculos['edificio'], rect)
                elif self.mapa[x][y] == 'bache':
                    pantalla.blit(self.obstaculos['bache'], rect)
                elif (x, y) == self.inicio:
                    # Dibujar el punto de inicio.
                    pygame.draw.circle(pantalla, VERDE, (y * self.tamano_celda + self.tamano_celda // 2, x * self.tamano_celda + self.tamano_celda // 2), self.tamano_celda // 4)
                elif (x, y) == self.fin:
                    # Dibujar el punto de fin.
                    pygame.draw.circle(pantalla, AZUL, (y * self.tamano_celda + self.tamano_celda // 2, x * self.tamano_celda + self.tamano_celda // 2), self.tamano_celda // 4)

# Clase para la calculadora de rutas
class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa  # Inicializa la calculadora de rutas con el mapa dado.

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Calcula la distancia de Manhattan entre dos puntos.

    def a_star(self, inicio, fin):
        self.mapa.inicio = inicio  # Establece el punto de inicio.
        self.mapa.fin = fin  # Establece el punto de fin.
        filas, columnas = self.mapa.filas, self.mapa.columnas
        abiertos = [(0, inicio)]  # Inicializa la lista de nodos abiertos con el nodo de inicio.
        heapq.heapify(abiertos)  # Convierte la lista en una cola de prioridad.
        costos = {inicio: 0}  # Inicializa los costos con el costo del nodo de inicio.
        padres = {inicio: None}  # Inicializa el diccionario de padres.

        while abiertos:  # Mientras haya nodos abiertos.
            _, actual = heapq.heappop(abiertos)  # Selecciona el nodo con la menor prioridad.

            if actual == fin:  # Si el nodo actual es el nodo de fin.
                ruta = []
                while actual:  # Reconstruir la ruta.
                    ruta.append(actual)
                    actual = padres[actual]
                ruta.reverse()  # Invierte la ruta para que vaya del inicio al fin.
                return ruta  # Devuelve la ruta.

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Para cada vecino del nodo actual.
                vecino = (actual[0] + dx, actual[1] + dy)

                if self.mapa.es_accesible(vecino[0], vecino[1]):  # Si el vecino es accesible.
                    nuevo_costo = costos[actual] + 1  # Calcula el nuevo costo para el vecino.
                    if vecino not in costos or nuevo_costo < costos[vecino]:  # Si el vecino no ha sido visitado o se encuentra un costo menor.
                        costos[vecino] = nuevo_costo  # Actualiza el costo.
                        prioridad = nuevo_costo + self.heuristica(fin, vecino)  # Calcula la prioridad del vecino.
                        heapq.heappush(abiertos, (prioridad, vecino))  # Añade el vecino a la cola de prioridad.
                        padres[vecino] = actual  # Establece el padre del vecino.

        return None  # Si no se encuentra una ruta, devuelve None.

# Función para permitir al usuario agregar y eliminar obstáculos con clics
def editar_obstaculos(mapa, pantalla):
    tipos_obstaculos = {
        pygame.K_1: 'agua',
        pygame.K_2: 'edificio',
        pygame.K_3: 'bache'
    }

    # Mostrar mensaje inicial
    font = pygame.font.Font(None, 36)
    mensaje_inicial = "Calculadora de Rutas"
    mensaje = font.render(mensaje_inicial, True, BLANCO)
    mensaje_rect = mensaje.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
    pantalla.blit(mensaje, mensaje_rect)
    pygame.display.flip()

    # Esperar un momento para que el mensaje sea visible antes de continuar
    pygame.time.wait(2000)

    editando_obstaculos = True
    while editando_obstaculos:  # Mientras se esté en el modo de edición de obstáculos.
        for evento in pygame.event.get():  # Para cada evento en la cola de eventos.
            if evento.type == pygame.QUIT:  # Si se cierra la ventana.
                return False  # Salir si el usuario cierra el juego.
            elif evento.type == pygame.MOUSEBUTTONDOWN:  # Si se presiona un botón del ratón.
                x, y = evento.pos  # Obtiene las coordenadas del ratón.
                fila = y // mapa.tamano_celda  # Calcula la fila en el mapa.
                columna = x // mapa.tamano_celda  # Calcula la columna en el mapa.
                teclas_presionadas = pygame.key.get_pressed()  # Obtiene las teclas presionadas.

                # Agregar obstáculo si se mantiene presionada una tecla numérica correspondiente.
                for tecla, obstaculo in tipos_obstaculos.items():
                    if teclas_presionadas[tecla]:
                        if mapa.es_accesible(fila, columna):
                            mapa.agregar_obstaculo(fila, columna, obstaculo)

                # Eliminar obstáculo si se presiona la tecla "7".
                if teclas_presionadas[pygame.K_7]:
                    mapa.eliminar_obstaculo(fila, columna)

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_0:  # Si se presiona la tecla "0".
                editando_obstaculos = False

        mapa.dibujar(pantalla)  # Dibujar el mapa cada vez que se interactúa.
        pygame.display.flip()  # Actualizar la pantalla.

    return True  # Continuar si el usuario completa la edición de obstáculos.

# Función para seleccionar los puntos de inicio y fin
def seleccionar_inicio_fin(mapa, pantalla):
    seleccionando_inicio = True
    while seleccionando_inicio:  # Mientras se estén seleccionando los puntos de inicio y fin.
        for evento in pygame.event.get():  # Para cada evento en la cola de eventos.
            if evento.type == pygame.QUIT:  # Si se cierra la ventana.
                return False  # Salir si el usuario cierra el juego.
            elif evento.type == pygame.MOUSEBUTTONDOWN:  # Si se presiona un botón del ratón.
                x, y = evento.pos  # Obtiene las coordenadas del ratón.
                fila = y // mapa.tamano_celda  # Calcula la fila en el mapa.
                columna = x // mapa.tamano_celda  # Calcula la columna en el mapa.
                if mapa.es_accesible(fila, columna):  # Si la celda es accesible.
                    if mapa.inicio is None:  # Si el punto de inicio no ha sido establecido.
                        mapa.inicio = (fila, columna)  # Establece el punto de inicio.
                    elif mapa.fin is None:  # Si el punto de fin no ha sido establecido.
                        mapa.fin = (fila, columna)  # Establece el punto de fin.
                        seleccionando_inicio = False

        mapa.dibujar(pantalla)  # Dibujar el mapa cada vez que se seleccione un punto.
        pygame.display.flip()  # Actualizar la pantalla.

    return True  # Continuar si el usuario completa la selección de puntos.

# Función principal
def main():
    pygame.init()  # Inicializa todas las variables y módulos de Pygame.

    filas, columnas = 10, 10  # Define el número de filas y columnas del mapa.
    tamano_celda = 60  # Define el tamaño de cada celda en píxeles.
    ancho_pantalla = columnas * tamano_celda  # Calcula el ancho de la pantalla.
    alto_pantalla = filas * tamano_celda  # Calcula el alto de la pantalla.
    pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))  # Establece el tamaño de la pantalla.
    pygame.display.set_caption("Obstáculos 1 Agua 2 Edificio 3 Bache 7 Borrar 0 Finalizar")  # Establece el título de la ventana.

    # Crear el mapa
    mapa = Mapa(filas, columnas, tamano_celda)

    # Mostrar mensaje inicial
    
    # Editar obstáculos y seleccionar puntos de inicio/fin
    if not editar_obstaculos(mapa, pantalla):  # Permite al usuario editar los obstáculos.
        pygame.quit()  # Si el usuario cierra la ventana, salir del programa.
        return

    if not seleccionar_inicio_fin(mapa, pantalla):  # Permite al usuario seleccionar los puntos de inicio y fin.
        pygame.quit()  # Si el usuario cierra la ventana, salir del programa.
        return

    # Crear la calculadora de rutas y encontrar la ruta
    calculadora = CalculadoraRutas(mapa)
    ruta = calculadora.a_star(mapa.inicio, mapa.fin)  # Calcula la ruta utilizando A*.

    # Bucle principal de Pygame
    corriendo = True
    while corriendo:  # Mientras el programa esté corriendo.
        for evento in pygame.event.get():  # Para cada evento en la cola de eventos.
            if evento.type == pygame.QUIT:  # Si se cierra la ventana.
                corriendo = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:  # Si se presiona la tecla Enter.
                corriendo = False  # Salir del bucle al presionar Enter.

        pantalla.fill(NEGRO)  # Limpiar la pantalla.
        mapa.dibujar(pantalla)  # Dibujar el mapa actualizado.
        if ruta:  # Si se ha encontrado una ruta.
            for paso in ruta:  # Para cada paso en la ruta.
                pygame.draw.circle(pantalla, BLANCO, (paso[1] * tamano_celda + tamano_celda // 2, paso[0] * tamano_celda + tamano_celda // 2), tamano_celda // 8)  # Dibujar un círculo blanco en el paso actual.

        pygame.display.flip()  # Actualizar la pantalla.

    # Salir de Pygame
    pygame.quit()  # Termina la ejecución de Pygame.

if __name__ == "__main__":
    main()  # Ejecuta la función principal si este archivo se ejecuta directamente.
