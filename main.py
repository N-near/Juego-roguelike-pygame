import math
import pygame
from mejoras import Mejora, elegir_opciones
from oleadas import WaveManager
#Inicindo pygame
pygame.init()

#Creando la pantalla y su complexion (anchoxalto)
p = pygame.display.set_mode((960,720))
rectangulos_mejoras = [pygame.Rect(70 + indice * 280, 310, 260, 190) for indice in range(3)]

COORDENADAS_SPRITES = [
    (17, 25, 73, 100), (97, 25, 90, 100), (185, 12, 91, 113), (283, 25, 73, 100),
    (371, 21, 78, 104), (460, 25, 73, 100), (549, 26, 73, 99), (633, 25, 82, 100),
    (17, 158, 73, 100), (97, 159, 81, 99), (190, 150, 81, 108), (283, 158, 73, 100),
    (367, 167, 82, 91), (456, 154, 77, 104), (549, 145, 73, 113), (637, 158, 73, 100),
]
hoja_enemigos = pygame.image.load("Jugador/sprite3.png").convert_alpha()
sprites_enemigos = [hoja_enemigos.subsurface(coordenadas) for coordenadas in COORDENADAS_SPRITES]

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
enemigos = []
gestor_oleadas = WaveManager()
menu_mejoras_activo = False
opciones_mejora: list[Mejora] = []
fuente_titulo_mejoras = pygame.font.Font(None, 48)
fuente_carta_mejora = pygame.font.Font(None, 30)
fuente_detalle_mejora = pygame.font.Font(None, 24)


def aplicar_mejora(mejora: Mejora) -> None:
    """Aplica el efecto seleccionado sobre las estadísticas actuales."""
    global vida_jugador, vida_maxima, velocidad_del_jugador
    global intervalo_disparo, daño_proyectil

    if mejora.identificador.startswith("curacion_"):
        vida_jugador = min(vida_maxima, vida_jugador + int(mejora.valor))
    elif mejora.identificador == "cadencia":
        intervalo_disparo = max(0.2, intervalo_disparo - mejora.valor)
    elif mejora.identificador == "velocidad":
        velocidad_del_jugador *= 1 + mejora.valor
    elif mejora.identificador == "danio":
        daño_proyectil += int(mejora.valor)
    elif mejora.identificador == "vida_maxima":
        vida_maxima += int(mejora.valor)


def seleccionar_mejora(indice: int) -> None:
    """Aplica una carta y devuelve el control al gestor de oleadas."""
    global menu_mejoras_activo, opciones_mejora

    if not 0 <= indice < len(opciones_mejora):
        return

    aplicar_mejora(opciones_mejora[indice])
    opciones_mejora = []
    menu_mejoras_activo = False
    gestor_oleadas.continue_after_reward()


def reiniciar_partida() -> None:
    """Restaura el estado inicial de una partida sin reiniciar Pygame."""
    global Variables_flotantes_para_x, Variables_flotantes_para_y
    global vida_maxima, vida_jugador, velocidad_del_jugador
    global intervalo_disparo, temporizador_disparo, daño_proyectil
    global invulnerabilidad_restante, jugador_derrotado, tiempo_supervivencia
    global tiempo_animacion, cuadro_actual, direccion_mirada
    global cultivos, inventario, proyectiles, enemigos, gestor_oleadas
    global menu_mejoras_activo, opciones_mejora

    Variables_flotantes_para_x = 50.0
    Variables_flotantes_para_y = 100.0
    py.topleft = (int(Variables_flotantes_para_x), int(Variables_flotantes_para_y))

    vida_maxima = 5
    vida_jugador = vida_maxima
    velocidad_del_jugador = 100
    intervalo_disparo = 0.8
    temporizador_disparo = 0.0
    daño_proyectil = 1
    invulnerabilidad_restante = 0.0

    jugador_derrotado = False
    tiempo_supervivencia = 0.0
    tiempo_animacion = 0.0
    cuadro_actual = 0
    direccion_mirada = (1, 0)

    proyectiles = []
    enemigos = []
    cultivos = {(3, 3): {"recurso": "zanahoria", "cosechado": False}}
    inventario = {"zanahoria": 0}
    gestor_oleadas = WaveManager()
    menu_mejoras_activo = False
    opciones_mejora = []


def dibujar_menu_mejoras() -> None:
    """Dibuja la pausa y las cartas usando solo primitivas y texto de Pygame."""
    capa = pygame.Surface(p.get_size(), pygame.SRCALPHA)
    capa.fill((0, 0, 0, 190))
    p.blit(capa, (0, 0))

    titulo = fuente_titulo_mejoras.render("OLEADA COMPLETADA", True, "white")
    p.blit(titulo, titulo.get_rect(center=(p.get_width() // 2, 220)))
    instruccion = fuente_detalle_mejora.render("Elige una mejora: teclas 1, 2, 3 o clic", True, "white")
    p.blit(instruccion, instruccion.get_rect(center=(p.get_width() // 2, 265)))

    for indice, mejora in enumerate(opciones_mejora):
        rect = rectangulos_mejoras[indice]
        pygame.draw.rect(p, (45, 66, 52), rect, border_radius=12)
        pygame.draw.rect(p, (170, 220, 125), rect, width=3, border_radius=12)
        etiqueta = fuente_detalle_mejora.render(f"{indice + 1}", True, "yellow")
        p.blit(etiqueta, (rect.x + 16, rect.y + 14))

        nombre = fuente_carta_mejora.render(mejora.nombre, True, "white")
        p.blit(nombre, nombre.get_rect(center=(rect.centerx, rect.y + 68)))

        palabras = mejora.descripcion.split()
        lineas: list[str] = []
        linea = ""
        for palabra in palabras:
            propuesta = f"{linea} {palabra}".strip()
            if fuente_detalle_mejora.size(propuesta)[0] > rect.width - 28 and linea:
                lineas.append(linea)
                linea = palabra
            else:
                linea = propuesta
        if linea:
            lineas.append(linea)
        for numero_linea, texto in enumerate(lineas):
            detalle = fuente_detalle_mejora.render(texto, True, (220, 230, 220))
            p.blit(detalle, detalle.get_rect(center=(rect.centerx, rect.y + 115 + numero_linea * 25)))

juego_encendido = True
#bucle para mantener la pantalla activa
while juego_encendido:
    tiempo_transcurrido = reloj.tick(60) / 1000
    if not jugador_derrotado and not menu_mejoras_activo:
        tiempo_supervivencia += tiempo_transcurrido
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_encendido = False
        if evento.type == pygame.MOUSEBUTTONDOWN and menu_mejoras_activo:
            if evento.button == 1:
                for indice, rect in enumerate(rectangulos_mejoras[:len(opciones_mejora)]):
                    if rect.collidepoint(evento.pos):
                        seleccionar_mejora(indice)
                        break
            continue
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  
                juego_encendido = False
            elif menu_mejoras_activo:
                teclas_mejora = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}
                if evento.key in teclas_mejora:
                    seleccionar_mejora(teclas_mejora[evento.key])
                continue
            elif jugador_derrotado:
                if evento.key == pygame.K_r:
                    reiniciar_partida()
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

    if not jugador_derrotado and not menu_mejoras_activo:
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
            ronda_completada = gestor_oleadas.update(
                tiempo_transcurrido,
                enemigos,
                p.get_size(),
                sprites_enemigos,
            )
            if ronda_completada:
                opciones_mejora = elegir_opciones(vida_jugador, vida_maxima)
                menu_mejoras_activo = True

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
        rect_sprite = enemigo["sprite"].get_rect(center=enemigo["rect"].center)
        p.blit(enemigo["sprite"], rect_sprite)

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
    texto_oleada = fuente_temporizador.render(f"OLEADA: {gestor_oleadas.wave_number}", True, "white")
    p.blit(texto_oleada, (10, 80))

    if menu_mejoras_activo:
        dibujar_menu_mejoras()

    if jugador_derrotado:
        texto_derrota = fuente_derrota.render("DERROTA", True, "red")
        p.blit(texto_derrota, texto_derrota.get_rect(center=p.get_rect().center))
        texto_reinicio = fuente_temporizador.render("Presiona R para reiniciar", True, "white")
        p.blit(texto_reinicio, texto_reinicio.get_rect(center=(p.get_width() // 2, p.get_height() // 2 + 55)))
   
    pygame.display.flip()
    
