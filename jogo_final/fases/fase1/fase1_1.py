  #configurações da janela
import pygame
from pygame.locals import*
def iniciar_fase1():
  from menu import dois_jogadores
  from geral.som import som_geral, som_musica
  from geral.dificuldade import dificuldade
  pygame.init()
  janela_x=1300; janela_y=600
  janela=pygame.display.set_mode([janela_x, janela_y])
  pygame.display.set_caption('jogo')

  jogador_img1=pygame.image.load('imagens/img_1/jogador_d.png')
  jogador_img2=pygame.image.load('imagens/img_1/jogador_e.png')
  bala_inimigo_img1=pygame.image.load('imagens/img_1/foguinho_verde_direita.png')
  bala_inimigo_img2=pygame.image.load('imagens/img_1/foguinho_verde_esquerda.png')
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
      self.x=100; self.y=150
      self.rect.bottomright= self.x, self.y

      self.vivo=True
      self.venceu=False
      self.velocidade=1.5
      self.gravidade=True
      self.pv=3
      self.gas=10
      self.max_gas=10
      self.balas=10
      self.max_balas=10
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
      dano=pygame.sprite.spritecollide(self, lista_balas_aliens, True, pygame.sprite.collide_mask)
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
        self.pv=0
      keys=pygame.key.get_pressed()
      if self.jogador=='jogador1':
        if not self.defesa:
          if keys[K_d]:
            self.movimento=True
            self.atual+=0.1
            self.direção='d'
            self.x+=self.velocidade
            if pisando:
              self.pausa_music+=0.1
              if self.pausa_music>=4:
                self.pausa_music=0
                andar.play()
            if self.atual>=18:
              self.atual=0
            self.image=self.direita[int(self.atual)]
          elif keys[K_a]:
            self.movimento=True
            self.atual+=0.1
            self.direção='s'
            self.x-=self.velocidade
            if pisando:
              self.pausa_music+=0.1
              if self.pausa_music>=4:
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
              self.gas-=0.06
              self.y-=1.60
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
            self.atual+=0.1
            self.direção='d'
            self.x+=self.velocidade
            if pisando:
              self.pausa_music+=0.1
              if self.pausa_music>=2:
                self.pausa_music=0
                andar.play()
            if self.atual>=18:
              self.atual=0
            self.image=self.direita[int(self.atual)]
          elif keys[K_LEFT]:
            self.movimento=True
            self.atual+=0.1
            self.direção='s'
            self.x-=self.velocidade
            if pisando:
              self.pausa_music+=0.1
              if self.pausa_music>=2:
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
              self.gas-=0.06
              self.y-=1.60
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
        self.y+=2
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
          novotiro=Tiro_d('jogador')
          novotiro.rect.x=self.x-20
          novotiro.rect.y=self.y-50
          lista_sprites.add(novotiro)
          lista_balas.add(novotiro)
        if self.direção=='s':
          self.balas-=1
          novotiro=Tiro_s('jogador')
          novotiro.rect.x=self.x-100
          novotiro.rect.y=self.y-50
          lista_sprites.add(novotiro)
          lista_balas.add(novotiro)
      
  #balas
  class Tiro_d(pygame.sprite.Sprite):
    def __init__(self, atirador):
      pygame.sprite.Sprite.__init__(self)
      self.atirador=atirador
      if self.atirador=='jogador':
        self.image=pygame.image.load('imagens/img_1/bala_d.png')
        self.image=pygame.transform.scale(self.image, (20, 20))
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
      if self.atirador=='inimigo':
        self.lista=[]
        for N in range(10):
          self.lista.append(bala_inimigo_img1.subsurface((0,N*100+200), (100, 100)))
        self.image=self.lista[0]
        self.image=pygame.transform.scale(self.image, (20, 20))
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.atual=0
    def update(self):
      if self.atirador=='jogador':
        self.rect.x+=3.5
        if self.rect.x>1300:
          self.kill()
      if self.atirador=='inimigo':
        self.rect.x+=3.5
        if self.rect.x>1300 or self.rect.x<(-10):
          self.kill()
        if self.atual<9:
          self.atual+=0.1
        else:
          self.atual=0
        self.image=self.lista[int(self.atual)]
        self.image=pygame.transform.scale(self.image, (50, 50))
      self.rect.topleft=self.rect.x, self.rect.y
      
  class Tiro_s(pygame.sprite.Sprite):
    def __init__(self, atirador):
      pygame.sprite.Sprite.__init__(self)
      self.atirador=atirador
      if self.atirador=='jogador':
        self.image=pygame.image.load('imagens/img_1/bala_s.png')
        self.image=pygame.transform.scale(self.image, (20, 20))
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
      if self.atirador=='inimigo':
        self.lista=[]
        for N in range(10):
          self.lista.append(bala_inimigo_img2.subsurface((0,N*100), (100, 100)))
        self.image=self.lista[0]
        self.image=pygame.transform.scale(self.image, (20, 20))
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.atual=0
    def update(self):
      if self.atirador=='jogador':
        self.rect.x-=3.5
        if self.rect.x<0:
          self.kill()
        self.rect.topleft=self.rect.x, self.rect.y
      if self.atirador=='inimigo':
        self.rect.x-=3.5
        if self.rect.x<0:
          self.kill()
        if self.atual<9:
          self.atual+=0.1
        else:
          self.atual=0
        self.image=self.lista[int(self.atual)]
        self.image=pygame.transform.scale(self.image, (50, 50))
      self.rect.topleft=self.rect.x, self.rect.y 

      
  #plataformas
  class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tam_x, tam_y):
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/plataforma.png')
      self.image=pygame.transform.scale(self.image, (tam_x, tam_y))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.center=pos_x, pos_y

  #portal
  class Portal(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/portal.png')
      self.image=pygame.transform.scale(self.image, (200, 200))
      self.rect=self.image.get_rect()
      self.rect.topleft=1150, 370

  #aliens padrões
  class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, mov):
      pygame.sprite.Sprite.__init__(self)
      self.x=x; self.y=y; self.mov=mov
      self.lista=[]
      self.lista.append(pygame.image.load('imagens/img_1/inimigo_base(e).png'))
      self.lista.append(pygame.image.load('imagens/img_1/inimigo_base(d).png'))
      self.image=self.lista[0]
      self.image=pygame.transform.scale(self.image, (100, 100))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.center=self.x, self.y

      self.pv=2
      self.c=True
      self.b=False
      self.d=True
      self.s=False
      self.direção='s'
      self.cadencia=0.05
      self.atirar=0
      self.distancia1=0
      self.distancia2=0
    
    def update(self):
      #verificação de vida
      matar=pygame.sprite.spritecollide(self, lista_balas, True, pygame.sprite.collide_mask)
      if matar:
        self.pv-=1
      if self.pv<=0:
        self.kill()
      #direção
      if jogador.rect.x<self.x:
        self.image=self.lista[0]
        self.direção='s'
      if jogador.rect.x>self.x:
        self.image=self.lista[1]
        self.direção='d'
      
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
            self.image=self.lista[0]
            self.direção='s'
          if jogador.rect.x>self.x:
            self.image=self.lista[1]
            self.direção='d'
        else:
          if jogador2.rect.x<self.x:
            self.image=self.lista[0]
            self.direção='s'
          if jogador2.rect.x>self.x:
            self.image=self.lista[1]
            self.direção='d'

      #padrão de ataque
      self.atirar+=self.cadencia
      if self.atirar>=10:
        if self.y-50<jogador.y-100<self.y+50:
          if self.direção=='d':
            novotiro=Tiro_d('inimigo')
            novotiro.image=pygame.image.load('imagens/img_1/disparo_energia(d).png')
            novotiro.rect.x=self.x+50
            novotiro.rect.y=self.y-15
            lista_sprites.add(novotiro)
            lista_balas_aliens.add(novotiro)
            self.atirar=0
          if self.direção=='s':
            novotiro=Tiro_s('inimigo')
            novotiro.image=pygame.image.load('imagens/img_1/disparo_energia(e).png')
            novotiro.rect.x=self.x-60
            novotiro.rect.y=self.y-15
            lista_sprites.add(novotiro)
            lista_balas_aliens.add(novotiro)
            self.atirar=0

      if dois_jogadores:
        self.atirar+=self.cadencia
        if self.atirar>=10:
          if self.y-50<jogador2.y-100<self.y+50:
            if self.direção=='d':
              novotiro=Tiro_d('inimigo')
              novotiro.image=pygame.image.load('imagens/img_1/disparo_energia(d).png')
              novotiro.rect.x=self.x+50
              novotiro.rect.y=self.y-15
              lista_sprites.add(novotiro)
              lista_balas_aliens.add(novotiro)
              self.atirar=0
            if self.direção=='s':
              novotiro=Tiro_s('inimigo')
              novotiro.image=pygame.image.load('imagens/img_1/disparo_energia(e).png')
              novotiro.rect.x=self.x-60
              novotiro.rect.y=self.y-15
              lista_sprites.add(novotiro)
              lista_balas_aliens.add(novotiro)
              self.atirar=0
      #movimentações
      if self.mov=='cb':
        if self.c:
          self.b=False; self.d=False; self.e=False
          self.y-=1
          if self.y<=225:
            self.b=True
            self.c=False; self.d=False; self.e=False
        if self.b:
          self.c=False; self.d=False; self.e=False
          self.y+=1
          if self.y>=380:
            self.c=True
            self.b=False; self.d=False; self.e=False
      if self.mov=='sd':
        if self.s:
          self.b=False; self.d=False; self.c=False
          self.x-=1
          if self.x<=910:
            self.d=True
            self.c=False; self.b=False; self.s=False
        if self.d:
          self.c=False; self.b=False; self.s=False
          self.x+=1
          if self.x>=1100:
            self.s=True
            self.b=False; self.d=False; self.c=False
      self.rect.center=self.x, self.y
      self.image=pygame.transform.scale(self.image, (120, 120))

  def reiniciar():
    for sprite in lista_balas_aliens:
      sprite.kill()
    if not dois_jogadores:
      l1.pv=2; l2.pv=2; l3.pv=2
      lista_sprites.add(jogador, l1, l2, l3)
      jogador.vivo=True; jogador.pv=3
      jogador.balas=10
      jogador.x=100; jogador.y=150
    if dois_jogadores:
      l1.pv=2; l2.pv=2; l3.pv=2
      lista_sprites.add(jogador, jogador2, l1, l2, l3)
      jogador.vivo=True; jogador.pv=3
      jogador.balas=10
      jogador.x=100; jogador.y=150
      jogador2.vivo=True; jogador2.pv=3
      jogador2.balas=10
      jogador2.x=80; jogador2.y=150
    if dificuldade=='facil':
      jogador.pv=5; jogador.gas=13; jogador.balas=15
      jogador.max_balas=25; jogador.max_gas=13
      l1.cadencia=0.05;l2.cadencia=0.05;l3.cadencia=0.05
      l1.pv=1; l2.pv=1; l3.pv=1
      if dois_jogadores:
        jogador2.pv=5; jogador2.gas=13; jogador2.balas=15
        jogador2.max_balas=25; jogador2.max_gas=13
    elif dificuldade=='medio':
      jogador.pv=3; jogador.gas=10; jogador.balas=10
      jogador.max_balas=20; jogador.max_gas=10
      l1.cadencia=0.1;l2.cadencia=0.1;l3.cadencia=0.1
      l1.pv=2; l2.pv=2; l3.pv=2
      if dois_jogadores:
        jogador2.pv=3; jogador2.gas=10; jogador2.balas=10
        jogador.max_balas=20; jogador.max_gas=10
    elif dificuldade=='dificil':
      jogador.pv=1; jogador.gas=9; jogador.balas=5
      jogador.max_balas=15; jogador.max_gas=9
      l1.cadencia=0.12;l2.cadencia=0.12;l3.cadencia=0.12
      l1.pv=3; l2.pv=3; l3.pv=3
      if dois_jogadores:
        jogador2.pv=1; jogador2.gas=9; jogador2.balas=5
        jogador.max_balas=15; jogador.max_gas=9

  #atribuição dos objetos e personagens
  lista_sprites=pygame.sprite.Group()
  lista_jogadores=pygame.sprite.Group()
  lista_plataformas=pygame.sprite.Group()
  lista_balas=pygame.sprite.Group()
  lista_aliens=pygame.sprite.Group()
  lista_balas_aliens=pygame.sprite.Group()
  jogador=Player('jogador1')
  l1=Aliens(550, 380, 'cb')
  l2=Aliens(720, 225, 'cb')
  l3=Aliens(1100, 500, 'sd')
  c1=Plataforma(200, 575, 400, 50)
  c2=Plataforma(1100, 575, 400, 50)
  p1=Plataforma(550, 450, 50, 50)
  p2=Plataforma(720, 450, 50, 50)
  portal=Portal()
  lista_aliens.add(l1, l2, l3)
  lista_plataformas.add(c1, c2, p1, p2)
  lista_jogadores.add(jogador)
  lista_sprites.add(portal, l1, l2, l3, c1, c2, p1, p2, jogador)
    
  if dois_jogadores:
    jogador2=Player('jogador2')
    jogador2.x-=20
    lista_jogadores.add(jogador2)
    lista_sprites.add(jogador2)

  #fundo de imagem
  fundo=pygame.image.load('imagens/img_1/fundo_teste0.jpeg')
  fundo=pygame.transform.scale(fundo, (1300, 600))

  #textos do jogo
  fonte=pygame.font.SysFont('Comic Sans', 40, True, True)
  fonte2=pygame.font.SysFont('Comic Sans', 60, True, True)
  
  #dificuldade
  if dificuldade=='facil':
    jogador.pv=5; jogador.gas=13; jogador.balas=15
    jogador.max_balas=25; jogador.max_gas=13
    l1.cadencia=0.05;l2.cadencia=0.05;l3.cadencia=0.05
    l1.pv=1; l2.pv=1; l3.pv=1
    if dois_jogadores:
      jogador2.pv=5; jogador2.gas=13; jogador2.balas=15
      jogador2.max_balas=25; jogador2.max_gas=13
  elif dificuldade=='medio':
    jogador.pv=3; jogador.gas=10; jogador.balas=10
    jogador.max_balas=20; jogador.max_gas=10
    l1.cadencia=0.1;l2.cadencia=0.1;l3.cadencia=0.1
    l1.pv=2; l2.pv=2; l3.pv=2
    if dois_jogadores:
      jogador2.pv=3; jogador2.gas=10; jogador2.balas=10
      jogador.max_balas=20; jogador.max_gas=10
  elif dificuldade=='dificil':
    jogador.pv=1; jogador.gas=9; jogador.balas=5
    jogador.max_balas=15; jogador.max_gas=9
    l1.cadencia=0.12;l2.cadencia=0.12;l3.cadencia=0.12
    l1.pv=3; l2.pv=3; l3.pv=3
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
        exit()
      if evento.type==pygame.KEYDOWN:
        if evento.key == pygame.K_ESCAPE:
          from geral.pause import pausar
          pausar('fase_1')
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
    
    #colisões gerais
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
        if jogador.x<plataforma.rect.centerx+50:
          jogador.x-=10
        else:
          jogador.x+=10
    else:
      jogador.gravidade=True

    if dois_jogadores:
      pisando2=pygame.sprite.spritecollide(jogador2, lista_plataformas, False, pygame.sprite.collide_mask)
      if pisando2:
        plataforma2=pisando2[-1]
        if jogador2.y<plataforma2.rect.centery:
          jogador2.gravidade=False
          if jogador2.gas<jogador2.max_gas:
            jogador2.gas+=0.25
        else:
          if jogador2.x<plataforma2.rect.centerx+50:
            jogador2.x-=10
          else:
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
    if not dois_jogadores:
      if portal in vencer:
        jogador.venceu=True
        lista_sprites.empty()
        win = 'VOCÊ GANHOU'
        ganhou = fonte2.render(win, True, (255, 255, 0))
        continuar = fonte2.render('pressione SPACE para avançar', True, (0, 0, 0))
      if jogador.venceu:
        janela.blit(ganhou, (375, 200))
        janela.blit(continuar, (200, 300))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
          from fases.fase1.fase1_2 import iniciar_fase2
          iniciar_fase2()

    if dois_jogadores:
      vencer=pygame.sprite.spritecollide(jogador, lista_sprites, False, pygame.sprite.collide_mask)
      vencer2=pygame.sprite.spritecollide(jogador2, lista_sprites, False, pygame.sprite.collide_mask)
      if portal in vencer:
        jogador.venceu=True
        jogador.kill()
      if portal in vencer2:
        jogador2.venceu=True
        jogador2.kill()
      if (jogador.venceu and jogador2.venceu) or (not jogador.vivo and jogador2.venceu) or (jogador.venceu and not jogador2.vivo):
        lista_sprites.empty()
        win = 'VOCÊ GANHOU'
        ganhou = fonte2.render(win, True, (255, 255, 0))
        continuar = fonte2.render('pressione SPACE ou 0 para avançar', True, (0, 0, 0))
        janela.blit(ganhou, (375, 200))
        janela.blit(continuar, (100, 300))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_KP0]:
          from fases.fase1.fase1_2 import iniciar_fase2
          iniciar_fase2()
      
    pygame.display.flip()
