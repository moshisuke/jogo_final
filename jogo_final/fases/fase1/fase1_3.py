#configurações da janela
import pygame
from pygame.locals import*

def iniciar_fase3():
  from geral.som import som_geral, som_musica
  from geral.dificuldade import dificuldade
  from menu import dois_jogadores
  from sys import exit
  pygame.init()
  janela_x=1300; janela_y=600
  janela=pygame.display.set_mode([janela_x, janela_y])
  pygame.display.set_caption('jogo')

  jogador_img1=pygame.image.load('imagens/img_1/jogador_d.png')
  jogador_img2=pygame.image.load('imagens/img_1/jogador_e.png')

  andar=pygame.mixer.Sound('sons/andar.mp3')
  andar.set_volume(som_geral)
  disparo_pistola=pygame.mixer.Sound('sons/disparo_pistola.mp3')
  disparo_pistola.set_volume(som_geral)
  disparo_metralhadora=pygame.mixer.Sound('sons/disparo_metralhadora.mp3')
  disparo_metralhadora.set_volume(som_geral)

  #personagem
  class Player(pygame.sprite.Sprite):
    def __init__(self, jogador):
      pygame.sprite.Sprite.__init__(self)
      self.parado=[]
      self.parado.append(pygame.image.load('imagens/img_1/homem(d).png'))
      self.parado.append(pygame.image.load('imagens/img_1/homem(e).png'))
      self.direita=[]
      for N in range(10):
        self.direita.append(jogador_img1.subsurface((N*99.8,0), (99.8, 102)))
      for N in range(9):
        self.direita.append(jogador_img1.subsurface((N*99.8,102), (100, 102)))
      self.esquerda=[]
      for N in range(10):
        self.esquerda.append(jogador_img2.subsurface((N*99.8,0), (99.8, 102)))
      for N in range(9):
        self.esquerda.append(jogador_img2.subsurface((N*99.8+99.8,102), (99.8, 102)))
      self.image=self.parado[0]
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.x=100; self.y=500
      self.rect.bottomright= self.x, self.y

      self.vivo=True
      self.venceu=False
      self.velocidade=1.5
      self.gravidade=True
      self.pv=3
      self.gas=10
      self.max_gas=10
      self.balas=10
      self.max_balas=20
      self.chave=0
      self.direção='d'
      self.defesa=False
      self.movimento=False
      self.atual=0
      self.arma='pistola'
      self.bala_seg=0.2
      self.disparo=0
      self.pausa_music=0
      self.jogador=jogador
    
    def update(self):
      #verificação de vida
      dano=pygame.sprite.spritecollide(self, lista_cranios, True, pygame.sprite.collide_mask)
      if dano:
        if self.defesa:
          if self.balas<self.max_balas:
            self.balas+=1
        else:
          self.pv-=1
      if self.pv<=0:
        self.kill()
      if self.x<70:
        self.x=70
      if self.x>janela_x:
        self.x=janela_x
      if self.y>700:
        self.vivo=False
      keys=pygame.key.get_pressed()
      if self.jogador=='jogador1':  
        if not self.defesa:
          if keys[K_d]:
            self.movimento=True
            self.atual+=0.15
            self.direção='d'
            self.x+=self.velocidade
            if pisando:
              self.pausa_music+=0.1
              if self.pausa_music>=15:
                self.pausa_music=0
                andar.play()
            if self.atual>=18:
              self.atual=0
            self.image=self.direita[int(self.atual)]
          elif keys[K_a]:
            self.movimento=True
            self.atual+=0.15
            self.direção='s'
            self.x-=self.velocidade
            if pisando:
              self.pausa_music+=0.1
              if self.pausa_music>=15:
                self.pausa_music=0
                andar.play()
            if self.atual>=18:
              self.atual=0
            self.image=self.esquerda[int(self.atual)]
          else:
            self.movimento=False
          if keys[K_w]:
            if self.gas>0:
              self.gravidade=False
              self.gas-=0.05
              self.y-=1.5
          if self.arma=='metralhadora':
            if keys[K_SPACE]:
              self.disparo+=self.bala_seg
              if self.disparo>=5:
                self.disparo=0
                if jogador.balas>0:
                  if jogador.pv>0:
                    jogador.atirar()
                    if not self.defesa:
                      disparo_metralhadora.play()
        if keys[K_s]:
          self.defesa=True
        else:
            self.defesa=False
      if self.jogador=='jogador2':
        if not self.defesa:
          if keys[K_RIGHT]:
            self.movimento=True
            self.atual+=0.15
            self.direção='d'
            self.x+=self.velocidade
            if pisando:
              self.pausa_music+=0.1
              if self.pausa_music>=15:
                self.pausa_music=0
                andar.play()
            if self.atual>=18:
              self.atual=0
            self.image=self.direita[int(self.atual)]
          elif keys[K_LEFT]:
            self.movimento=True
            self.atual+=0.15
            self.direção='s'
            self.x-=self.velocidade
            if pisando:
              self.pausa_music+=0.1
              if self.pausa_music>=15:
                self.pausa_music=0
                andar.play()
            if self.atual>=18:
              self.atual=0
            self.image=self.esquerda[int(self.atual)]
          else:
            self.movimento=False
          if keys[K_UP]:
            if self.gas>0:
              self.gravidade=False
              self.gas-=0.05
              self.y-=1.5
          if self.arma=='metralhadora':
            if keys[K_KP0]:
              self.disparo+=self.bala_seg
              if self.disparo>=5:
                self.disparo=0
                if jogador2.balas>0:
                  if jogador2.pv>0:
                    jogador2.atirar()
                    if not self.defesa:
                      disparo_metralhadora.play()
        if keys[K_DOWN]:
          self.defesa=True
        else:
          self.defesa=False
        
      if self.gravidade:
        self.y+=3
      if self.pv<=0:
        self.pv=0
        self.vivo=False
      if not self.movimento:
        if self.direção=='d':
          self.image=self.parado[0]
        else:
          self.image=self.parado[1]
      self.rect.bottomright= self.x, self.y
      
    def atirar(self):
      if not self.defesa:
        if self.direção=='d':
          self.balas-=1
          novotiro=Tiro_d()
          novotiro.rect.x=self.x-20
          novotiro.rect.y=self.y-50
          lista_sprites.add(novotiro)
          lista_balas.add(novotiro)
        if self.direção=='s':
          self.balas-=1
          novotiro=Tiro_s()
          novotiro.rect.x=self.x-100
          novotiro.rect.y=self.y-50
          lista_sprites.add(novotiro)
          lista_balas.add(novotiro)

  #balas
  class Tiro_d(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/bala_d.png')
      self.image=pygame.transform.scale(self.image, (20, 20))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
    def update(self):
      self.rect.x+=3
      if self.rect.x>1300 or self.rect.x<(-10):
        self.kill()
      self.rect.topleft=self.rect.x, self.rect.y
      
  class Tiro_s(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/bala_s.png')
      self.image=pygame.transform.scale(self.image, (20, 20))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
    def update(self):
      self.rect.x-=3
      if self.rect.x<0:
        self.kill()
      self.rect.topleft=self.rect.x, self.rect.y

  #plataformas
  class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tam_x, tam_y):
      pygame.sprite.Sprite.__init__(self)
      self.tam_x=tam_x
      self.image=pygame.image.load('imagens/img_1/plataforma3.png')
      self.image=pygame.transform.scale(self.image, (tam_x, tam_y))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.center=pos_x, pos_y

  #BOSS
  class Boss(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
      self.x=posx; self.y=posy
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/boss.png')
      self.image=pygame.transform.scale(self.image, (200,200))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.center=self.x, self.y

      self.atirar=0
      self.cadencia=0.10
      self.pv=100
      self.direção='c'

    def update(self):
      if self.y>=220:
        self.direção='c'
      if self.y<=120:
        self.direção='b'
      if self.direção=='c':
        self.y-=0.1
      if self.direção=='b':
        self.y+=0.1
      dano=pygame.sprite.spritecollide(self, lista_balas, True, pygame.sprite.collide_mask)
      if dano:
        self.pv-=1
        if self.pv==80:
          subchefe=Subchefe(100, 300)
          lista_morte_instatanea.add(subchefe)
          lista_sprites.add(subchefe)
        if self.pv==60:
          subchefe=Subchefe(1300, 300)
          lista_morte_instatanea.add(subchefe)
          lista_sprites.add(subchefe)
        if self.pv==40:
          subchefe=Subchefe(100, 300)
          lista_morte_instatanea.add(subchefe)
          lista_sprites.add(subchefe)
          subchefe=Subchefe(1300, 300)
          lista_morte_instatanea.add(subchefe)
          lista_sprites.add(subchefe)
        if self.pv==20:
          subchefe1=Subchefe(100, 300)
          subchefe2=Subchefe(boss.x, 300)
          subchefe3=Subchefe(1300, 300)
          lista_morte_instatanea.add(subchefe1, subchefe2, subchefe3)
          lista_sprites.add(subchefe1, subchefe2, subchefe3)
      if self.pv<=10:
        self.image=pygame.transform.scale(self.image, (250,250))
        self.mask=pygame.mask.from_surface(self.image)
        lista_morte_instatanea.add(boss)
        ataque=pygame.sprite.spritecollide(jogador, lista_morte_instatanea, False, pygame.sprite.collide_mask)

        if ataque:
          jogador.pv=0
        if self.atirar>=49.9:
          cranio=Cranio()
          cranio.y=self.y+50
          lista_cranios.add(cranio)
          lista_sprites.add(cranio)
          cranio=Cranio()
          cranio.y=self.y+100
          lista_cranios.add(cranio)
          lista_sprites.add(cranio)
        if self.x<jogador.x:
          self.x+=0.1
        if self.x>jogador.x:
          self.x-=0.1
        
        if dois_jogadores:
          if jogador.rect.x>self.rect.x:
            self.distancia1=jogador.rect.x-self.rect.x
          if jogador2.rect.x>self.rect.x:
            self.distancia2=jogador2.rect.x-self.rect.x
          if jogador.rect.x<self.rect.x:
            self.distancia1=self.rect.x-jogador.rect.x
          if jogador2.rect.x<self.rect.x:
            self.distancia2=self.rect.x-jogador2.rect.x

          if self.distancia1<self.distancia2:
            if jogador.rect.x<self.x:
              self.x-=0.5
            if jogador.rect.x>self.x:
              self.x+=0.5
          else:
            if jogador2.rect.x<self.x:
              self.x-=0.5
            if jogador2.rect.x>self.x:
              self.x+=0.5

      if self.pv<=0:
        self.kill()
        jogador.venceu=True
        if dois_jogadores:
          jogador2.venceu=True
      self.atirar+=self.cadencia
      if self.atirar>=50:
        cranio=Cranio()
        lista_cranios.add(cranio)
        lista_sprites.add(cranio)
        self.atirar=0
      self.rect.center=self.x, self.y

  class Cranio(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.lista=[]
      self.lista.append(pygame.image.load('imagens/img_1/cranio.png'))
      self.lista.append(pygame.image.load('imagens/img_1/cranio(1).png'))
      self.image=self.lista[0]
      self.image=pygame.transform.scale(self.image, (40, 40))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.x=boss.x; self.y=boss.y
      self.rect.bottomright=self.x, self.y

      self.pv=2
      self.vel=0.5
      self.distancia1=0
      self.distancia2=0
      self.alvo=''
      
    def update(self):
      destruido=pygame.sprite.spritecollide(self, lista_balas, True, pygame.sprite.collide_mask)
      if len(lista_cranios)>10:
        primeiro_cranio=lista_cranios.sprites()[0]
        lista_cranios.remove(primeiro_cranio)
      if destruido:
        self.pv-=1
      if not dois_jogadores:
        if self.pv<=0:
          jogador.balas+=4
          self.kill()

        if jogador.x-20>self.x:
          self.x+=self.vel
          self.image=self.lista[0]
        if jogador.x-20<self.x:
          self.x-=self.vel
          self.image=self.lista[1]
        if jogador.y-20>self.y:
          self.y+=self.vel
        if jogador.y-20<self.y:
          self.y-=self.vel
      if dois_jogadores:
        if self.pv<=0:
          jogador2.balas+=2
          jogador.balas+=2
          self.kill()
        if jogador.x>self.x:
          self.distancia1=jogador.x-self.x
        if jogador2.x>self.x:
          self.distancia2=jogador2.x-self.x
        if jogador.x<self.x:
          self.distancia1=self.x-jogador.x
        if jogador2.x<self.x:
          self.distancia2=self.x-jogador2.x

        if self.distancia1<self.distancia2 and jogador.vivo:
          self.alvo='jogador1'
        if not jogador2.vivo:
          self.alvo='jogador1'
        if self.alvo=='jogador1':
          if jogador.x-20<self.x:
            self.image=self.lista[1]
            self.x-=self.vel
          if jogador.x-20>self.x:
            self.image=self.lista[0]
            self.x+=self.vel
          if jogador.y-20<self.y:
            self.y-=self.vel
          if jogador.y-20>self.y:
            self.y+=self.vel

        if self.distancia1>self.distancia2 and jogador2.vivo:
          self.alvo='jogador2'
        if not jogador.vivo:
          self.alvo='jogador2'
        if self.alvo=='jogador2':
          if jogador2.x-20<self.x:
            self.image=self.lista[1]
            self.x-=self.vel
          if jogador2.x-20>self.x:
            self.image=self.lista[0]
            self.x+=self.vel
          if jogador2.y-20<self.y:
            self.y-=self.vel
          if jogador2.y-20>self.y:
            self.y+=self.vel
      self.image=pygame.transform.scale(self.image, (40, 40))
      self.rect.bottomright=self.x, self.y

  #subchefe
  class Subchefe(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
      self.x=posx; self.y=posy
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/subboss.png')
      self.image=pygame.transform.scale(self.image, (150,150))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.bottomright=self.x, self.y

      self.pv=10
      self.vel=0.5
      self.distancia1=0
      self.distancia2=0
      self.alvo=''

    def update(self):
      dano=pygame.sprite.spritecollide(self, lista_balas, True, pygame.sprite.collide_mask)
      if dano:
        self.pv-=1
      if self.pv<=0:
        self.kill()
      if not dois_jogadores:
        ataque=pygame.sprite.spritecollide(jogador, lista_morte_instatanea, False, pygame.sprite.collide_mask)
        if ataque:
          jogador.pv=0
        if jogador.x-20>self.x:
          self.x+=self.vel
        if jogador.x-20<self.x:
          self.x-=self.vel
        if jogador.y-20>self.y:
          self.y+=self.vel
        if jogador.y-20<self.y:
          self.y-=self.vel
      if dois_jogadores:
        if jogador.x>self.x:
          self.distancia1=jogador.x-self.x
        if jogador2.x>self.x:
          self.distancia2=jogador2.x-self.x
        if jogador.x<self.x:
          self.distancia1=self.x-jogador.x
        if jogador2.x<self.x:
          self.distancia2=self.x-jogador2.x

        if self.distancia1<self.distancia2 and jogador.vivo:
          self.alvo='jogador1'
        if not jogador2.vivo:
          self.alvo='jogador1'
        if self.distancia2<self.distancia1 and jogador2.vivo:
          self.alvo='jogador2'
        if not jogador.vivo:
          self.alvo='jogador2'

        if self.alvo=='jogador1':
          ataque=pygame.sprite.spritecollide(jogador, lista_morte_instatanea, False, pygame.sprite.collide_mask)
          if ataque:
            jogador.pv=0
          if jogador.x<self.x:
            self.x-=self.vel
          if jogador.x>self.x:
            self.x+=self.vel
          if jogador.y<self.y:
            self.y-=self.vel
          if jogador.y>self.y:
            self.y+=self.vel
        if self.alvo=='jogador2':
          ataque2=pygame.sprite.spritecollide(jogador2, lista_morte_instatanea, False, pygame.sprite.collide_mask)
          if ataque2:
            jogador2.pv=0
          if jogador2.x<self.x:
            self.x-=self.vel
          if jogador2.x>self.x:
            self.x+=self.vel
          if jogador2.y<self.y:
            self.y-=self.vel
          if jogador2.y>self.y:
            self.y+=self.vel
      self.rect.bottomright=self.x, self.y

  def reiniciar():
    lista_sprites.empty()
    lista_cranios.empty()
    lista_morte_instatanea.empty()
    jogador.chave=0
    jogador.x=100; jogador.y=500
    jogador.vivo=True
    boss.pv=100; boss.x, boss.y= 675, 250
    lista_sprites.add(ch1, pi1, pi2, pi3, boss, jogador)
    if dois_jogadores:
      jogador2.chave=0
      jogador2.x=100; jogador2.y=500
      jogador2.vivo=True
      lista_sprites.add(ch1, pi1, pi2, pi3, boss, jogador2)
    if dificuldade=='facil':
      jogador.pv=5; jogador.gas=13; jogador.balas=15
      jogador.max_balas=25; jogador.max_gas=13
      if dois_jogadores:
        jogador2.pv=5; jogador2.gas=13; jogador2.balas=15
        jogador2.max_balas=25; jogador2.max_gas=13
    elif dificuldade=='medio':
      jogador.pv=3; jogador.gas=10; jogador.balas=10
      jogador.max_balas=20; jogador.max_gas=10
      if dois_jogadores:
        jogador2.pv=3; jogador2.gas=10; jogador2.balas=10
        jogador2.max_balas=20; jogador2.max_gas=10
    elif dificuldade=='dificil':
      jogador.pv=1; jogador.gas=9; jogador.balas=5
      jogador.max_balas=15; jogador.max_gas=9
      if dois_jogadores:
        jogador2.pv=1; jogador2.gas=9; jogador2.balas=5
        jogador2.max_balas=15; jogador2.max_gas=9

  #atribuição dos objetos e personagens
  lista_sprites=pygame.sprite.Group()
  lista_plataformas=pygame.sprite.Group()
  lista_balas=pygame.sprite.Group()
  lista_boss=pygame.sprite.Group()
  lista_cranios=pygame.sprite.Group()
  lista_morte_instatanea=pygame.sprite.Group()
  jogador=Player('jogador1')
  boss=Boss(675, 250)
  ch1=Plataforma(janela_x/2, 590, janela_x, 50)
  pi1=Plataforma(675, 380, 500, 40)
  pi2=Plataforma(100, 380, 150, 40)
  pi3=Plataforma(1200, 380, 150, 40)
  lista_plataformas.add(ch1, pi1, pi2, pi3)
  lista_sprites.add(ch1, pi1, pi2, pi3, boss, jogador)

  if dois_jogadores:
    jogador2=Player('jogador2')
    jogador2.x-=20
    lista_sprites.add(jogador2)

  #fundo de imagem
  fundo=pygame.image.load('imagens/img_1/fundo3.jpg')
  fundo=pygame.transform.scale(fundo, (1300, 600))

  #textos do jogo
  fonte=pygame.font.SysFont('Comic Sans', 40, True, True)
  fonte2=pygame.font.SysFont('Comic Sans', 60, True, True)

  #dificuldade
  if dificuldade=='facil':
    jogador.pv=5; jogador.gas=13; jogador.balas=15
    jogador.max_balas=25; jogador.max_gas=13
    if dois_jogadores:
      jogador2.pv=5; jogador2.gas=13; jogador2.balas=15
      jogador2.max_balas=25; jogador2.max_gas=13
  elif dificuldade=='medio':
    jogador.pv=3; jogador.gas=10; jogador.balas=10
    jogador.max_balas=20; jogador.max_gas=10
    if dois_jogadores:
      jogador2.pv=3; jogador2.gas=10; jogador2.balas=10
      jogador2.max_balas=20; jogador2.max_gas=10
  elif dificuldade=='dificil':
    jogador.pv=1; jogador.gas=9; jogador.balas=5
    jogador.max_balas=15; jogador.max_gas=9
    if dois_jogadores:
      jogador2.pv=1; jogador2.gas=9; jogador2.balas=5
      jogador2.max_balas=15; jogador2.max_gas=9

  #laço principal
  while True:
    janela.fill((255,255,255))
    janela.blit(fundo, (0, 0))

    #controle de tiros player
    for evento in pygame.event.get():
      if evento.type==pygame.QUIT:
        pygame.quit()
        exit()
      if evento.type==pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
          from geral.pause import pausar
          pausar('fase_3')
        if evento.key == pygame.K_1:
          jogador.arma='pistola'
        if evento.key == pygame.K_2:
          jogador.arma='metralhadora'
        if evento.key == pygame.K_SPACE:
          if jogador.arma=='pistola':
            if jogador.balas>0:
              if jogador.pv>0:
                jogador.atirar()
                if not jogador.defesa:
                  disparo_pistola.play()
          if not dois_jogadores:
            if not jogador.vivo:
              reiniciar()
          else:
            if not jogador.vivo and not jogador2.vivo:
              reiniciar()
        if dois_jogadores:
          if evento.key == pygame.K_KP1:
            jogador2.arma='pistola'
          if evento.key == pygame.K_KP2:
            jogador2.arma='metralhadora'
          if evento.key == pygame.K_KP0:
            if jogador2.arma=='pistola':
              if jogador2.balas>0:
                if jogador2.pv>0:
                  jogador2.atirar()
                  if not jogador2.defesa:
                    disparo_pistola.play()
            if not jogador2.vivo and not jogador.vivo:
              reiniciar()

    #impactos e colisões
    pisando=pygame.sprite.spritecollide(jogador, lista_plataformas, False, pygame.sprite.collide_mask)
    bala_plataforma=pygame.sprite.groupcollide(lista_balas, lista_plataformas, True, False, pygame.sprite.collide_mask)
    vencer=pygame.sprite.spritecollide(jogador, lista_sprites, False, pygame.sprite.collide_mask)
    
    if pisando:
      plataforma=pisando[-1]
      if jogador.y<plataforma.rect.centery:
        jogador.gravidade=False
        if jogador.gas<jogador.max_gas:
          jogador.gas+=0.25
      else:
        if jogador.y>plataforma.rect.centery+50:
          jogador.y+=10
        if plataforma==pi1:
          if jogador.x<plataforma.rect.centerx-270:
            jogador.x-=10
          if jogador.x>plataforma.rect.centerx+270:
            jogador.x+=10
        else:
          if jogador.x<plataforma.rect.centerx-100:
            jogador.x-=10
          if jogador.x>plataforma.rect.centerx+100:
            jogador.x+=10
    else:
      jogador.gravidade=True
    if dois_jogadores:
      pisando2=pygame.sprite.spritecollide(jogador2, lista_plataformas, False, pygame.sprite.collide_mask)
      bala_plataforma2=pygame.sprite.groupcollide(lista_balas, lista_plataformas, True, False, pygame.sprite.collide_mask)
      vencer2=pygame.sprite.spritecollide(jogador2, lista_sprites, False, pygame.sprite.collide_mask)
      if pisando2:
        plataforma2=pisando2[-1]
        if jogador2.y<plataforma2.rect.centery:
          jogador2.gravidade=False
          if jogador2.gas<jogador2.max_gas:
            jogador2.gas+=0.25
        else:
          if jogador2.y>plataforma2.rect.centery+50:
            jogador2.y+=10
          if plataforma2==pi1:
            if jogador2.x<plataforma2.rect.centerx-270:
              jogador2.x-=10
            if jogador2.x>plataforma2.rect.centerx+270:
              jogador2.x+=10
          else:
            if jogador2.x<plataforma2.rect.centerx-100:
              jogador2.x-=10
            if jogador2.x>plataforma2.rect.centerx+100:
              jogador2.x+=10
      else:
        jogador2.gravidade=True

    #STATUS DO JOGADOR
    pv=f'PV: {int(jogador.pv)}'
    pv_formatado=fonte.render(pv, True, (0,0,0))
    janela.blit(pv_formatado, (10, 10))

    gas=f'gás: {int(jogador.gas)}'
    gas_formatado=fonte.render(gas, True, (0,0,0))
    janela.blit(gas_formatado, (140, 10))

    munição=f'balas: {int(jogador.balas)}'
    munição_formatado=fonte.render(munição, True, (0,0,0))
    janela.blit(munição_formatado, (320, 10))

    if dois_jogadores:
      pv=f'PV: {int(jogador2.pv)}'
      pv_formatado=fonte.render(pv, True, (0,0,0))
      janela.blit(pv_formatado, (10, 50))

      gas=f'gás: {int(jogador2.gas)}'
      gas_formatado=fonte.render(gas, True, (0,0,0))
      janela.blit(gas_formatado, (140, 50))

      munição=f'balas: {int(jogador2.balas)}'
      munição_formatado=fonte.render(munição, True, (0,0,0))
      janela.blit(munição_formatado, (320, 50))
    
    #STATUS BOSS
    pv_boss=f'PV_boss: {int(boss.pv)}'
    pv_boss_formatado=fonte.render(pv_boss, True, (255,0,0))
    janela.blit(pv_boss_formatado, (1000, 10))

    #atualização de tela
    lista_sprites.draw(janela)
    lista_sprites.update()

    #morte
    if not dois_jogadores:
      if not jogador.vivo:
        mensagem='GAME OVER'
        gameover=fonte2.render(mensagem, True, (255,0,0))
        janela.blit(gameover, (425, 200))
        jogador.pv=0
        jogador.kill()
    if dois_jogadores:
      if not jogador.vivo:
        jogador.pv=0
        jogador.kill()
      if not jogador2.vivo:
        jogador2.pv=0
        jogador2.kill()
      if not jogador.vivo and not jogador2.vivo:
        mensagem='GAME OVER'
        gameover=fonte2.render(mensagem, True, (255,0,0))
        janela.blit(gameover, (425, 200))

    #venceu
    if jogador.venceu:
      lista_sprites.empty()
      win = 'VOCÊ GANHOU'
      ganhou = fonte2.render(win, True, (255, 255, 0))
      continuar = fonte2.render('OBRIGADO POR JOGAR', True, (0, 0, 0))
      janela.blit(ganhou, (375, 200))
      janela.blit(continuar, (250, 300))
      keys = pygame.key.get_pressed()
    if dois_jogadores:
      if jogador.venceu and jogador2.venceu:
        lista_sprites.empty()
        win = 'VOCÊ GANHOU'
        ganhou = fonte2.render(win, True, (255, 255, 0))
        continuar = fonte2.render('OBRIGADO POR JOGAR', True, (0, 0, 0))
        janela.blit(ganhou, (375, 200))
        janela.blit(continuar, (250, 300))
        keys = pygame.key.get_pressed()
      
    pygame.display.flip()