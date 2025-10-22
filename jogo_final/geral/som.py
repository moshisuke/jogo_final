import pygame
from pygame.locals import *

som_musica=0.5
som_geral=0.5

def saindo_som(destino):
    import time
    import cv2

    # Inicialize o pygame
    pygame.init()

    # Inicialize a captura de vídeo
    cap = cv2.VideoCapture('videos/som_saindo.mp4')
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
            if destino=='configurações':
                from geral.config import configurações
                configurações('menu')
            if destino=='configurações1':
                from geral.config import configurações
                configurações('fase_1')
            if destino=='configurações2':
                from geral.config import configurações
                configurações('fase_2')
            if destino=='configurações3':
                from geral.config import configurações
                configurações('fase_3')
            

def entrar_som(local):
    global som_geral, som_musica
    import time
    import cv2

    # Inicialize o pygame
    pygame.init()

    # Inicialize a captura de vídeo
    cap = cv2.VideoCapture('videos/som.mp4')
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
            self.lista_pos=[(160, 200), (160, 400)]
            self.pos_atual=0
            self.rect.center=self.lista_pos[self.pos_atual]

        def update(self):
            self.rect.center=self.lista_pos[self.pos_atual]

    class Barra(pygame.sprite.Sprite):
        def __init__(self, direção):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load('imagens/menu_imgs/barra_som.png')
            self.largura=50
            self.image=pygame.transform.scale(self.image, (self.largura,65))
            self.rect=self.image.get_rect()
            self.lista_pos=[(636, 208), (636, 390)]
            self.pos_atual=seta.pos_atual
            self.rect.bottomleft=self.lista_pos[self.pos_atual]
            self.direção=direção
            self.som_musica=som_musica
            self.som_geral=som_geral
            self.pausa=0
        def update(self):
            keys=pygame.key.get_pressed()
            if keys[K_d]:
                self.pausa+=0.5
                if self.pausa>=20:
                    if self.direção=='cima' and seta.pos_atual==0 and self.som_musica<0.9:
                        self.som_musica+=0.1
                    if self.direção=='baixo' and seta.pos_atual==1 and self.som_geral<0.9:
                        self.som_geral+=0.1
                    self.pausa=0
            if keys[K_a]:
                self.pausa+=1
                if self.pausa>=20:
                    if self.direção=='cima' and seta.pos_atual==0  and self.som_musica>0.2:
                        self.som_musica-=0.1
                    if self.direção=='baixo' and seta.pos_atual==1  and self.som_geral>0.2:
                        self.som_geral-=0.1
                    self.pausa=0
            if self.direção=='cima' and seta.pos_atual==0:
                self.largura=(self.som_musica*10)*50
            if self.direção=='baixo' and seta.pos_atual==1:
                self.largura=(self.som_geral*10)*50

            self.pos_atual=seta.pos_atual
            som_musica=self.som_musica
            som_geral=self.som_geral
            self.rect.bottomleft=self.lista_pos[self.pos_atual]
            self.image=pygame.transform.scale(self.image, (self.largura,65))
    seta=Seta()
    barra1=Barra('cima')
    barra2=Barra('baixo')
    fundo=pygame.image.load('imagens/menu_imgs/tela_de_som.jpg')
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
                    som_musica=barra1.som_musica
                    som_geral=barra2.som_geral
                if evento.key==pygame.K_ESCAPE:
                    if local=='configurações':
                        saindo_som('configurações')
                    elif local=='configurações1':
                        saindo_som('configurações1')
                    elif local=='configurações2':
                        saindo_som('configurações2')
                    elif local=='configurações3':
                        saindo_som('configurações3')
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
            janela.blit(barra1.image, (barra1.lista_pos[0]))
            barra1.update()
            janela.blit(barra2.image, (barra2.lista_pos[1]))
            barra2.update()
            pygame.display.update()