import pygame
#Inicindo pygame
pygame.init()







#Creando la pantalla y su complexion (anchoxalto)
p = pygame.display.set_mode((960,720))

sprite_Jugador = pygame.image.load('Jugador/fox.png').convert_alpha()
primer_zorro = sprite_Jugador.subsurface((0,0,32,32))
segundo_zorro = sprite_Jugador.subsurface((32,0,32,32))

#Creando rectangulo con pygame         
py = pygame.Rect(50,50,75,100)


#Creando variables con las medidas de el rect
Variables_flotantes_para_x = 50
Variables_flotantes_para_y = 100

#agregando con int la variable flotante
py.x = int(Variables_flotantes_para_x)
py.y = int(Variables_flotantes_para_y)


velocidad_del_jugador = 0.5

juego_encendido = True
#bucle para mantener la pantalla activa
while juego_encendido:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego_encendido = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:  
                juego_encendido = False

    teclas_presionadas = pygame.key.get_pressed()
    #DERECHA
    if teclas_presionadas[pygame.K_RIGHT]:
         if Variables_flotantes_para_x + py.width < p.get_width():
             Variables_flotantes_para_x = Variables_flotantes_para_x + velocidad_del_jugador
    #IZQUIERDA
    if teclas_presionadas[pygame.K_LEFT]:
        if Variables_flotantes_para_x  > 0:
            Variables_flotantes_para_x = Variables_flotantes_para_x - velocidad_del_jugador
            
    #ARRIBA
    if teclas_presionadas[pygame.K_UP]:
        if Variables_flotantes_para_y  > 0:
            Variables_flotantes_para_y = Variables_flotantes_para_y - velocidad_del_jugador
            
    #ABAJO
    if teclas_presionadas[pygame.K_DOWN]:
        if Variables_flotantes_para_y + py.height < p.get_height():
            Variables_flotantes_para_y = Variables_flotantes_para_y + velocidad_del_jugador
            
    py.x = int(Variables_flotantes_para_x)
    py.y = int(Variables_flotantes_para_y)

    p.fill('black')
    #pygame.draw.rect(p,'pink',py)
    p.blit(primer_zorro,py)
   
    pygame.display.flip()
    
