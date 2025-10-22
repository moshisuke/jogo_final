import pygame

def saindo_pause(destino):
    import time
    import cv2

    # Inicialize o pygame
    pygame.init()

    # Inicialize a captura de vídeo
    cap = cv2.VideoCapture('videos/pause_saindo.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]

    # Crie a janela do pygame
    janela_x=1300; janela_y=600
    janela=pygame.display.set_mode([janela_x, janela_y])

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
        if success:
            # Converta a imagem OpenCV para o formato Pygame
            pygame_img = pygame.image.frombuffer(img.tobytes(), shape, "BGR")

            # Blit a imagem na janela do pygame
            janela.blit(pygame_img, (300, 150))
            
            pygame.display.update()

            success, img = cap.read()
            time.sleep(0.06)
        else:
            if destino=='jogo1':
                from fases.fase1.fase1_1 import iniciar_fase1
                iniciar_fase1()
            elif destino=='jogo2':
                from fases.fase1.fase1_2 import iniciar_fase2
                iniciar_fase2()
            elif destino=='jogo3':
                from fases.fase1.fase1_3 import iniciar_fase3
                iniciar_fase3()
            elif destino=='configurações1':
                from geral.config import configurações
                configurações('fase_1')
            elif destino=='configurações2':
                from geral.config import configurações
                configurações('fase_2')
            elif destino=='configurações3':
                from geral.config import configurações
                configurações('fase_3')
            elif destino=='menu':
                from menu import menu_principal
                menu_principal()

def pausar(local):
    import time
    import cv2

    # Inicialize o pygame
    pygame.init()

    # Inicialize a captura de vídeo
    cap = cv2.VideoCapture('videos/pause.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]

    # Crie a janela do pygame
    janela_x=1300; janela_y=600
    janela=pygame.display.set_mode([janela_x, janela_y])

    class Seta(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load('imagens/menu_imgs/cranio_copy.png')
            self.image=pygame.transform.scale(self.image, (60,60))
            self.rect=self.image.get_rect()
            self.lista_pos=[(480, 232), (429, 294), (486, 351)]
            self.pos_atual=0
            self.rect.center=self.lista_pos[self.pos_atual]

        def update(self):
            self.rect.center=self.lista_pos[self.pos_atual]

    seta=Seta()
    fundo=pygame.image.load('imagens/menu_imgs/pause.jpg')
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_w:
                    if seta.pos_atual>0:
                        seta.pos_atual-=1
                if evento.key==pygame.K_s:
                    if seta.pos_atual<2:
                        seta.pos_atual+=1
                if evento.key==pygame.K_RETURN:
                    if seta.pos_atual==0:
                        if local=='fase_1':
                            saindo_pause('jogo1')
                        if local=='fase_2':
                            saindo_pause('jogo2')
                        if local=='fase_3':
                            saindo_pause('jogo3')
                    if seta.pos_atual==1:
                        if local=='fase_1':
                            saindo_pause('configurações1')
                        if local=='fase_2':
                            saindo_pause('configurações2')
                        if local=='fase_3':
                            saindo_pause('configurações3')
                    if seta.pos_atual==2:
                        saindo_pause('menu')
        if success:
            # Converta a imagem OpenCV para o formato Pygame
            pygame_img = pygame.image.frombuffer(img.tobytes(), shape, "BGR")

            # Blit a imagem na janela do pygame
            janela.blit(pygame_img, (300, 150))
            
            pygame.display.update()

            success, img = cap.read()
            time.sleep(0.06)
        else:
            # O vídeo chegou ao fim, continue exibindo a última imagem
            janela.fill((0,0,0))
            janela.blit(fundo, (300,150))
            janela.blit(seta.image, (seta.lista_pos[seta.pos_atual]))
            seta.update()
            pygame.display.update()
