import math
import pygame
#Inicindo pygame
pygame.init()

#Creando la pantalla y su complexion (anchoxalto)
p = pygame.display.set_mode((960,720))

sprite_Jugador = pygame.image.load("Jugador/sprite4.png").convert_alpha()
print(sprite_Jugador.get_size())
primer_zorro = sprite_Jugador.subsurface((2,214,67,97))
segundo_zorro = sprite_Jugador.subsurface((155,214,64,97))

#Creando rectangulo con pygame         
py = pygame.Rect(50,50,67,97)


#Creando variables con las medidas de el rect
Variables_flotantes_para_x = 50
Variables_flotantes_para_y = 100

#agregando con int la variable flotante
py.x = int(Variables_flotantes_para_x)
py.y = int(Variables_flotantes_para_y)


velocidad_del_jugador = 100
reloj = pygame.time.Clock()
tiempo_supervivencia = 0
fuente_temporizador = pygame.font.Font(None, 32)
fuente_derrota = pygame.font.Font(None, 72)
tiempo_animacion = 0
intervalo_animacion = 0.15
cuadro_actual = 0
tamaño_casilla = 32
direccion_mirada = (1, 0)
cultivos = {(3, 3): {"recurso": "zanahoria", "cosechado": False}}
inventario = {"zanahoria": 0}
vida_maxima = 5
vida_jugador = vida_maxima
daño_por_impacto = 1
duracion_invulnerabilidad = 0.8
invulnerabilidad_restante = 0
jugador_derrotado = False
intervalo_disparo = 0.8
temporizador_disparo = 0
velocidad_proyectil = 300
daño_proyectil = 1
proyectiles = []
enemigos = [
    {"rect": pygame.Rect(900, 60, 24, 24), "x": 900.0, "y": 60.0, "velocidad": 35, "vida": 3},
    {"rect": pygame.Rect(900, 650, 24, 24), "x": 900.0, "y": 650.0, "velocidad": 35, "vida": 3},
    {"rect": pygame.Rect(60, 650, 24, 24), "x": 60.0, "y": 650.0, "velocidad": 35, "vida": 3},
]

juego_encendido = True
#bucle para mantener la pantalla activa
while juego_encendido:
    tiempo_transcurrido = reloj.tick(60) / 1000
    if not jugador_derrotado:
        tiempo_supervivencia += tiempo_transcurrido
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_encendido = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  
                juego_encendido = False
            elif jugador_derrotado:
                continue
            elif evento.key == pygame.K_RIGHT:
                direccion_mirada = (1, 0)
            elif evento.key == pygame.K_LEFT:
                direccion_mirada = (-1, 0)
            elif evento.key == pygame.K_UP:
                direccion_mirada = (0, -1)
            elif evento.key == pygame.K_DOWN:
                direccion_mirada = (0, 1)
            elif evento.key == pygame.K_e:
                columna_jugador = py.centerx // tamaño_casilla
                fila_jugador = py.centery // tamaño_casilla
                casilla_objetivo = (
                    columna_jugador + direccion_mirada[0],
                    fila_jugador + direccion_mirada[1],
                )
                cultivo = cultivos.get(casilla_objetivo)

                if cultivo is None:
                    print("No hay un cultivo delante.")
                elif cultivo["cosechado"]:
                    print("Ese cultivo ya fue cosechado.")
                else:
                    cultivo["cosechado"] = True
                    recurso = cultivo["recurso"]
                    inventario[recurso] += 1
                    print(f"Cosechaste {recurso}. Tienes: {inventario[recurso]}")

    if not jugador_derrotado:
        teclas_presionadas = pygame.key.get_pressed()
        jugador_caminando = any(teclas_presionadas[tecla] for tecla in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN))

        if jugador_caminando:
            tiempo_animacion += tiempo_transcurrido
            if tiempo_animacion >= intervalo_animacion:
                cuadro_actual = 1 - cuadro_actual
                tiempo_animacion = 0
        else:
            cuadro_actual = 0
            tiempo_animacion = 0

        direccion_x = teclas_presionadas[pygame.K_RIGHT] - teclas_presionadas[pygame.K_LEFT]
        direccion_y = teclas_presionadas[pygame.K_DOWN] - teclas_presionadas[pygame.K_UP]

        longitud_direccion = math.hypot(direccion_x, direccion_y)
        if longitud_direccion > 0:
            direccion_x /= longitud_direccion
            direccion_y /= longitud_direccion

        Variables_flotantes_para_x += direccion_x * velocidad_del_jugador * tiempo_transcurrido
        Variables_flotantes_para_y += direccion_y * velocidad_del_jugador * tiempo_transcurrido
            
        py.x = int(Variables_flotantes_para_x)
        py.y = int(Variables_flotantes_para_y)

        # Mantener al jugador dentro de los límites de la pantalla
        if py.left < 0:
            py.left = 0
            Variables_flotantes_para_x = py.x
        if py.right > p.get_width():
            py.right = p.get_width()
            Variables_flotantes_para_x = py.x
        if py.top < 0:
            py.top = 0
            Variables_flotantes_para_y = py.y
        if py.bottom > p.get_height():
            py.bottom = p.get_height()
            Variables_flotantes_para_y = py.y

        invulnerabilidad_restante = max(0, invulnerabilidad_restante - tiempo_transcurrido)
        for enemigo in enemigos:
            diferencia_x = py.centerx - enemigo["rect"].centerx
            diferencia_y = py.centery - enemigo["rect"].centery
            distancia = math.hypot(diferencia_x, diferencia_y)
            if distancia > 0:
                enemigo["x"] += diferencia_x / distancia * enemigo["velocidad"] * tiempo_transcurrido
                enemigo["y"] += diferencia_y / distancia * enemigo["velocidad"] * tiempo_transcurrido

            enemigo["x"] = max(0, min(enemigo["x"], p.get_width() - enemigo["rect"].width))
            enemigo["y"] = max(0, min(enemigo["y"], p.get_height() - enemigo["rect"].height))
            enemigo["rect"].topleft = (int(enemigo["x"]), int(enemigo["y"]))

            if enemigo["rect"].colliderect(py) and invulnerabilidad_restante == 0:
                vida_jugador -= daño_por_impacto
                invulnerabilidad_restante = duracion_invulnerabilidad
                if vida_jugador <= 0:
                    vida_jugador = 0
                    jugador_derrotado = True
                break

        if not jugador_derrotado:
            temporizador_disparo += tiempo_transcurrido
            proyectiles_restantes = []
            for proyectil in proyectiles:
                proyectil["x"] += proyectil["velocidad_x"] * tiempo_transcurrido
                proyectil["y"] += proyectil["velocidad_y"] * tiempo_transcurrido
                proyectil["rect"].topleft = (int(proyectil["x"]), int(proyectil["y"]))

                impacto = False
                for enemigo in enemigos:
                    if enemigo["vida"] > 0 and proyectil["rect"].colliderect(enemigo["rect"]):
                        enemigo["vida"] -= daño_proyectil
                        impacto = True
                        break

                if not impacto and p.get_rect().colliderect(proyectil["rect"]):
                    proyectiles_restantes.append(proyectil)

            proyectiles = proyectiles_restantes
            enemigos = [enemigo for enemigo in enemigos if enemigo["vida"] > 0]

            if enemigos and temporizador_disparo >= intervalo_disparo:
                objetivo = min(
                    enemigos,
                    key=lambda enemigo: (enemigo["rect"].centerx - py.centerx) ** 2
                    + (enemigo["rect"].centery - py.centery) ** 2,
                )
                diferencia_x = objetivo["rect"].centerx - py.centerx
                diferencia_y = objetivo["rect"].centery - py.centery
                distancia = math.hypot(diferencia_x, diferencia_y)
                if distancia > 0:
                    proyectiles.append({
                        "rect": pygame.Rect(py.centerx - 5, py.centery - 5, 10, 10),
                        "x": py.centerx - 5.0,
                        "y": py.centery - 5.0,
                        "velocidad_x": diferencia_x / distancia * velocidad_proyectil,
                        "velocidad_y": diferencia_y / distancia * velocidad_proyectil,
                    })
                    temporizador_disparo = 0

    for y in range(0, p.get_height(), tamaño_casilla):
        for x in range(0, p.get_width(), tamaño_casilla):
            color_casilla = 'forestgreen' if (x // tamaño_casilla + y // tamaño_casilla) % 2 == 0 else 'green'
            ancho_casilla = min(tamaño_casilla, p.get_width() - x)
            alto_casilla = min(tamaño_casilla, p.get_height() - y)
            pygame.draw.rect(p, color_casilla, (x, y, ancho_casilla, alto_casilla))

    for (columna, fila), cultivo in cultivos.items():
        x_cultivo = columna * tamaño_casilla
        y_cultivo = fila * tamaño_casilla
        pygame.draw.rect(p, 'saddlebrown', (x_cultivo, y_cultivo, tamaño_casilla, tamaño_casilla))
        if not cultivo["cosechado"]:
            pygame.draw.rect(p, 'darkgreen', (x_cultivo + 14, y_cultivo + 10, 4, 15))
            pygame.draw.rect(p, 'limegreen', (x_cultivo + 7, y_cultivo + 9, 9, 5))
            pygame.draw.rect(p, 'limegreen', (x_cultivo + 16, y_cultivo + 5, 9, 5))

    for enemigo in enemigos:
        pygame.draw.rect(p, "firebrick", enemigo["rect"])

    for proyectil in proyectiles:
        pygame.draw.rect(p, "gold", proyectil["rect"])

    #pygame.draw.rect(p,'pink',py)
    cuadro_zorro = primer_zorro if cuadro_actual == 0 else segundo_zorro
    p.blit(cuadro_zorro,py)

    minutos, segundos = divmod(int(tiempo_supervivencia), 60)
    texto_temporizador = fuente_temporizador.render(f"{minutos:02}:{segundos:02}", True, "white")
    p.blit(texto_temporizador, (10, 10))
    texto_vida = fuente_temporizador.render(f"VIDA: {vida_jugador}/{vida_maxima}", True, "white")
    p.blit(texto_vida, (10, 45))

    if jugador_derrotado:
        texto_derrota = fuente_derrota.render("DERROTA", True, "red")
        p.blit(texto_derrota, texto_derrota.get_rect(center=p.get_rect().center))
   
    pygame.display.flip()
    
