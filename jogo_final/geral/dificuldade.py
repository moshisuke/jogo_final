import pygame
dificuldade=''

def saindo_dificuldade(destino):
    import time
    import cv2

    # Inicialize o pygame
    pygame.init()

    # Inicialize a captura de vídeo
    cap = cv2.VideoCapture('videos/dificuldade_saindo.mp4')
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
            elif destino=='fase1':
                from fases.fase1.fase1_1 import iniciar_fase1
                iniciar_fase1()

def entrar_dificuldade():
    global dificuldade
    import time
    import cv2

    # Inicialize o pygame
    pygame.init()

    # Inicialize a captura de vídeo
    cap = cv2.VideoCapture('videos/dificuldade.mp4')
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
            self.lista_pos=[(37, 330), (424, 336), (864, 330)]
            self.pos_atual=0
            self.rect.center=self.lista_pos[self.pos_atual]

        def update(self):
            self.rect.center=self.lista_pos[self.pos_atual]

    seta=Seta()
    fundo=pygame.image.load('imagens/menu_imgs/dificuldade.jpg')
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type==pygame.KEYDOWN:
                if evento.key==pygame.K_a:
                    if seta.pos_atual>0:
                        seta.pos_atual-=1
                if evento.key==pygame.K_d:
                    if seta.pos_atual<2:
                        seta.pos_atual+=1
                if evento.key==pygame.K_RETURN:
                    if seta.pos_atual==0:
                        dificuldade='facil'
                    if seta.pos_atual==1:
                        dificuldade='medio'
                    if seta.pos_atual==2:
                        dificuldade='dificil'
                    saindo_dificuldade('fase1')
                if evento.key==pygame.K_ESCAPE:
                    saindo_dificuldade('menu')
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