import pygame
import math

# Inicializa Pygame
pygame.init()

# Configuración de la ventana y colores
ancho_pantalla, alto_pantalla = 800, 600
ventana = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
color_pantalla, color_dibujo = (255, 255, 255), (0, 0, 0)

# Configuración de la línea y el círculo
linea = []
circulo_pos, circulo_radio = None, None
velocidad = 0.3
dibujando, tamaño_circulo = False, True
indice = 0

# Bucle principal
corriendo = True
while corriendo:
    ventana.fill(color_pantalla)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            linea.append(evento.pos)
            dibujando = True
            if circulo_pos is None:
                circulo_pos = evento.pos
        elif evento.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                if tamaño_circulo:
                    circulo_radio = int(math.hypot(evento.pos[0] - circulo_pos[0], evento.pos[1] - circulo_pos[1]))
                else:
                    linea.append(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONUP:
            dibujando, tamaño_circulo = False, False

    if len(linea) > 1:
        pygame.draw.lines(ventana, color_dibujo, False, linea, 3)

    if circulo_pos is not None and circulo_radio is not None:
        # Dibuja el círculo principal con el centro transparente
        circulo_surface = pygame.Surface((circulo_radio * 2, circulo_radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(circulo_surface, (color_dibujo[0], color_dibujo[1], color_dibujo[2], 128),
                           (circulo_radio, circulo_radio), circulo_radio)
        ventana.blit(circulo_surface, (circulo_pos[0] - circulo_radio, circulo_pos[1] - circulo_radio))

    if linea and not dibujando:
        dx, dy = linea[indice][0] - circulo_pos[0], linea[indice][1] - circulo_pos[1]
        distancia = math.sqrt(dx ** 2 + dy ** 2)

        if distancia > velocidad:
            dx, dy = dx / distancia, dy / distancia
            circulo_pos = (circulo_pos[0] + dx * velocidad, circulo_pos[1] + dy * velocidad)
        else:
            circulo_pos = linea[indice]
            indice += 1
            if indice >= len(linea):
                linea, indice = [], 0

    pygame.display.flip()

pygame.quit()
