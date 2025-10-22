import pygame

def saindo_config(destino):
    import time
    import cv2

    # Inicialize o pygame
    pygame.init()

    # Inicialize a captura de vídeo
    cap = cv2.VideoCapture('videos/config2_saindo.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]

    # Crie a janela do pygame
    janela = pygame.display.set_mode(shape)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
        if success:
            # Converta a imagem OpenCV para o formato Pygame
            pygame_img = pygame.image.frombuffer(img.tobytes(), shape, "BGR")

            # Blit a imagem na janela do pygame
            janela.blit(pygame_img, (0, 0))
            
            pygame.display.update()

            success, img = cap.read()
            time.sleep(0.06)
        else:
            if destino=='menu':
                from menu import menu_principal
                menu_principal()
            elif destino=='som':
                from geral.som import entrar_som
                entrar_som('configurações')
            elif destino=='som1':
                from geral.som import entrar_som
                entrar_som('configurações1')
            elif destino=='som2':
                from geral.som import entrar_som
                entrar_som('configurações2')
            elif destino=='som3':
                from geral.som import entrar_som
                entrar_som('configurações3')
            elif destino=='skin':
                pass


def configurações(local):
    import time
    import cv2

    # Inicialize o pygame
    pygame.init()

    # Inicialize a captura de vídeo
    cap = cv2.VideoCapture('videos/config2.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]

    # Crie a janela do pygame
    janela = pygame.display.set_mode(shape)

    class Seta(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load('imagens/menu_imgs/cranio_copy.png')
            self.image=pygame.transform.scale(self.image, (60,60))
            self.rect=self.image.get_rect()
            self.lista_pos=[(480, 232), (480, 420)]
            self.pos_atual=0
            self.rect.center=self.lista_pos[self.pos_atual]

        def update(self):
            self.rect.center=self.lista_pos[self.pos_atual]

    seta=Seta()
    fundo=pygame.image.load('imagens/menu_imgs/configurações.jpg')
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
                    if seta.pos_atual<1:
                        seta.pos_atual+=1
                if evento.key==pygame.K_RETURN:
                    if seta.pos_atual==0:
                        if local=='menu':
                            from geral.config import saindo_config
                            saindo_config('som')
                        if local=='fase_1':
                            from geral.config import saindo_config
                            saindo_config('som1')
                        if local=='fase_2':
                            from geral.config import saindo_config
                            saindo_config('som2')
                        if local=='fase_3':
                            from geral.config import saindo_config
                            saindo_config('som3')
                if evento.key==pygame.K_ESCAPE:
                    if local=='menu':
                        from geral.config import saindo_config
                        saindo_config('menu')
                    if local=='fase_1':
                        from geral.pause import pausar
                        pausar('fase_1')
                    elif local=='fase_2':
                        from geral.pause import pausar
                        pausar('fase_2')
                    elif local=='fase_3':
                        from geral.pause import pausar
                        pausar('fase_3')
        if success:
            # Converta a imagem OpenCV para o formato Pygame
            pygame_img = pygame.image.frombuffer(img.tobytes(), shape, "BGR")

            # Blit a imagem na janela do pygame
            janela.blit(pygame_img, (0, 0))
            
            pygame.display.update()

            success, img = cap.read()
            time.sleep(0.06)
        else:
            # O vídeo chegou ao fim, continue exibindo a última imagem
            janela.fill((0,0,0))
            janela.blit(fundo, (0,0))
            janela.blit(seta.image, (seta.lista_pos[seta.pos_atual]))
            seta.update()
            pygame.display.update()
