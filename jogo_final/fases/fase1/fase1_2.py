#configurações da janela
import pygame
from pygame.locals import*

def iniciar_fase2():
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
      self.velocidade=8
      self.gravidade=True
      self.pv=3
      self.gas=10
      self.max_gas=10
      self.balas=10
      self.max_balas=10
      self.chave=0
      self.direção='d'
      self.defesa=False
      self.movimento=False
      self.atual=0
      self.arma='pistola'
      self.bala_seg=1
      self.disparo=0
      self.pausa_music=0
      self.jogador=jogador
    
    def update(self):
      #verificação de vida
      dano=pygame.sprite.spritecollide(self, lista_balas_aliens, True, pygame.sprite.collide_mask)
      if dano:
        if not self.defesa:
          self.pv-=1
        else:
          self.balas+=1
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
            self.atual+=0.65
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
          elif keys[K_a]:
            self.movimento=True
            self.atual+=0.65
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
          if keys[K_w]:
            if self.gas>0:
              self.gravidade=False
              self.gas-=0.4
              self.y-=10
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
            self.atual+=0.65
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
            self.atual+=0.65
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
              self.gas-=0.4
              self.y-=10
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
        self.y+=10
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
        self.rect.x+=20
        if self.rect.x>1300:
          self.kill()
      if self.atirador=='inimigo':
        self.rect.x+=20
        if self.rect.x>1300 or self.rect.x<(-10):
          self.kill()
        if self.atual<9:
          self.atual+=0.5
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
        self.rect.x-=20
        if self.rect.x<0:
          self.kill()
        self.rect.topleft=self.rect.x, self.rect.y
      if self.atirador=='inimigo':
        self.rect.x-=20
        if self.rect.x<0:
          self.kill()
        if self.atual<9:
          self.atual+=0.5
        else:
          self.atual=0
        self.image=self.lista[int(self.atual)]
        self.image=pygame.transform.scale(self.image, (50, 50))
      self.rect.topleft=self.rect.x, self.rect.y
      
  #plataformas
  class Plataforma(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tam_x, tam_y):
      pygame.sprite.Sprite.__init__(self)
      self.tam_x=tam_x
      self.image=pygame.image.load('imagens/img_1/plataforma2.png')
      self.image=pygame.transform.scale(self.image, (tam_x, tam_y))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.center=pos_x, pos_y
  #coluna
  class Coluna(pygame.sprite.Sprite):
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
      self.rect.topleft=170, 390

  #aliens padrões
  class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y, mov, item):
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
      self.cadencia=0.40
      self.atirar=0
      self.item=item
    
    def update(self):
      #verificação de vida
      matar=pygame.sprite.spritecollide(self, lista_balas, True, pygame.sprite.collide_mask)
      if matar:
        self.pv-=1
      if self.pv<=0:
        if self.item=='chave':
          chave=Chave(self.x, self.y)
          lista_chaves.add(chave)
          lista_sprites.add(chave)
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
              novotiro=Tiro_d()
              novotiro.image=pygame.image.load('imagens/img_1/disparo_energia(d).png')
              novotiro.rect.x=self.x+50
              novotiro.rect.y=self.y-15
              lista_sprites.add(novotiro)
              lista_balas_aliens.add(novotiro)
              self.atirar=0
            if self.direção=='s':
              novotiro=Tiro_s('jogador')
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
          self.y-=5
          if self.y<=100:
            self.b=True
            self.c=False; self.d=False; self.e=False
        if self.b:
          self.c=False; self.d=False; self.e=False
          self.y+=5
          if self.y>=320:
            self.c=True
            self.b=False; self.d=False; self.e=False
      if self.mov=='sd':
        if self.s:
          self.b=False; self.d=False; self.c=False
          self.x-=4
          if self.x<=910:
            self.d=True
            self.c=False; self.b=False; self.s=False
        if self.d:
          self.c=False; self.b=False; self.s=False
          self.x+=4
          if self.x>=1100:
            self.s=True
            self.b=False; self.d=False; self.c=False
      self.rect.center=self.x, self.y
      self.image=pygame.transform.scale(self.image, (120, 120))

  #aliens subchefes
  class Subchefe(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
      self.x=posx; self.y=posy
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/subboss.png')
      self.image=pygame.transform.scale(self.image, (150,150))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.bottomright=self.x, self.y

      self.ativado=False
      self.pv=5

    def update(self):
      dano=pygame.sprite.spritecollide(self, lista_balas, True, pygame.sprite.collide_mask)
      if dano:
        self.pv-=1
      ataque=pygame.sprite.spritecollide(jogador, lista_morte_instatanea, False, pygame.sprite.collide_mask)
      if ataque and self.ativado:
        jogador.pv=0
      else:
        pass
      if self.pv<=0:
        chave=Chave(500, 500)
        lista_chaves.add(chave)
        lista_sprites.add(chave)
        self.kill()
      if self.ativado:
        if porta2.atuante=='jogador1' or porta1.atuante=='jogador1':
          if jogador.x>self.x:
            self.x+=4
          if jogador.x<self.x:
            self.x-=4
          if jogador.y>self.y:
            self.y+=1.5
          if jogador.y<self.y:
            self.y-=1.5
        if dois_jogadores:
          if porta2.atuante=='jogador2' or porta1.atuante=='jogador2':
            ataque2=pygame.sprite.spritecollide(jogador2, lista_morte_instatanea, False, pygame.sprite.collide_mask)
            if ataque2 and self.ativado:
              jogador2.pv=0
            else:
              pass
            if jogador2.x>self.x:
              self.x+=4
            if jogador2.x<self.x:
              self.x-=4
            if jogador2.y>self.y:
              self.y+=1.5
            if jogador2.y<self.y:
              self.y-=1.5

      self.rect.bottomright=self.x, self.y
      
  #chaves
  class Chave(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/chave.png')
      self.image=pygame.transform.scale(self.image, (50, 50))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.center=posx, posy
      
    def update(self):
      if not dois_jogadores:
        pegar=pygame.sprite.spritecollide(jogador, lista_chaves, True, pygame.sprite.collide_mask)
        if pegar:
          jogador.chave+=1
        if not jogador.vivo:
          self.kill()
      if dois_jogadores:
        pegar=pygame.sprite.spritecollide(jogador, lista_chaves, True, pygame.sprite.collide_mask)
        if pegar:
          jogador.chave+=1
        pegar2=pygame.sprite.spritecollide(jogador2, lista_chaves, True, pygame.sprite.collide_mask)
        if pegar2:
          jogador2.chave+=1
        if not jogador2.vivo and not jogador.vivo:
          self.kill()

  #ajudante
  class Ajudante(pygame.sprite.Sprite):
    def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image=pygame.image.load('imagens/img_1/robo_atk.png')
      self.image=pygame.transform.scale(self.image, (100,100))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.x=120; self.y=520
      self.rect.bottomright=self.x, self.y

      self.ligado=False
      
    def update(self):
      ativar=pygame.sprite.spritecollide(jogador, lista_ajudantes, False, pygame.sprite.collide_mask)
      if ativar:
        self.ligado=True
      ataque=pygame.sprite.spritecollide(ajudante, lista_morte_instatanea, False, pygame.sprite.collide_mask)
    
      if dois_jogadores:
        ativar2=pygame.sprite.spritecollide(jogador2, lista_ajudantes, False, pygame.sprite.collide_mask)
        if ativar2:
          self.ligado=True
        
      if self.ligado:
        if ataque:
          subchefe.pv=0
          self.kill()
        if subchefe.x>self.x:
          self.x+=4
        if subchefe.x<self.x:
          self.x-=4
        if subchefe.y>self.y:
          self.y+=1.5
        if subchefe.y<self.y:
          self.y-=1.5
      self.rect.bottomright=self.x, self.y

  #portas
  class Porta(pygame.sprite.Sprite):
    def __init__(self, posx, posy, efeito):
      pygame.sprite.Sprite.__init__(self)
      self.x=posx
      self.y=posy 
      self.efeito=efeito
      self.image=pygame.image.load('imagens/img_1/porta_trancada.png')
      self.image=pygame.transform.scale(self.image, (100,185))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.rect.center= self.x, self.y

      self.atuante=''
      
    def update(self):
      abrir = pygame.sprite.spritecollide(jogador, lista_portas, False, pygame.sprite.collide_mask)
      if abrir:
        portas=abrir[-1]
        if jogador.chave > 0:
          jogador.chave -= 1
          self.atuante='jogador1'
          if portas.efeito:
            subchefe.ativado = True
            if jogador.balas < 5:
              lista_ajudantes.add(ajudante)
              lista_sprites.add(ajudante)
          portas.kill()
        else:
          if jogador.x < self.rect.centerx:
            jogador.x -= 10
          if jogador.x > self.rect.centerx:
            jogador.x += 10
      if dois_jogadores: 
        abrir2 = pygame.sprite.spritecollide(jogador2, lista_portas, False, pygame.sprite.collide_mask)
        if abrir2:
          portas=abrir2[-1]
          if jogador2.chave > 0:
            jogador2.chave -= 1
            self.atuante='jogador2'
            if portas.efeito:
              subchefe.ativado = True
              if jogador2.balas < 5:
                lista_ajudantes.add(ajudante)
                lista_sprites.add(ajudante)
            portas.kill()
          else:
            if jogador2.x < self.rect.centerx:
              jogador2.x -= 10
            if jogador2.x > self.rect.centerx:
              jogador2.x += 10

  def reiniciar():
    if not dois_jogadores:
      jogador.balas=10; jogador.chave=0
      jogador.x=100; jogador.y=350
      jogador.pv=3; jogador.vivo=True 
      ajudante.ligado=False; ajudante.rect.bottomright=100, 500
      lista_sprites.remove(ajudante)
      l1.pv=2; subchefe.pv=5
      subchefe.ativado=False; subchefe.x=540; subchefe.y=570
      lista_sprites.add(jogador, l1, subchefe, l1, porta1, porta2)
      lista_portas.add(porta1, porta2)
      if dificuldade=='facil':
        jogador.pv=5; jogador.gas=13; jogador.balas=15
        jogador.max_balas=25; jogador.max_gas=13
        l1.cadencia=0.1; l1.pv=1
        subchefe.pv=2
      if dificuldade=='medio':
        jogador.pv=3; jogador.gas=10; jogador.balas=10
        jogador.max_balas=20; jogador.max_gas=10
        l1.cadencia=0.4; l1.pv=2
        subchefe.pv=5
      if dificuldade=='dificil':
        jogador.pv=1; jogador.gas=9; jogador.balas=5
        jogador.max_balas=15; jogador.max_gas=9
        l1.cadencia=0.6; l1.pv=3
        subchefe.pv=8
    elif dois_jogadores:
      jogador.balas=10; jogador.chave=0
      jogador2.balas=10; jogador2.chave=0
      jogador.x=100; jogador.y=500
      jogador2.x=80; jogador2.y=500
      jogador.pv=3; jogador.vivo=True 
      jogador2.pv=3; jogador2.vivo=True
      ajudante.ligado=False; ajudante.rect.bottomright=100, 500
      lista_sprites.remove(ajudante)
      l1.pv=2; subchefe.pv=5
      subchefe.ativado=False; subchefe.x=540; subchefe.y=570
      lista_sprites.add(jogador, jogador2, l1, subchefe, l1, porta1, porta2)
      lista_portas.add(porta1, porta2)
      if dificuldade=='facil':
        jogador.pv=5; jogador.gas=13; jogador.balas=15
        jogador2.pv=5; jogador2.gas=13; jogador2.balas=15
        jogador2.max_balas=25; jogador2.max_gas=13
        l1.cadencia=0.1; l1.pv=1
        subchefe.pv=2
      if dificuldade=='medio':
        jogador.pv=3; jogador.gas=10; jogador.balas=10
        jogador.max_balas=20; jogador.max_gas=10
        jogador2.pv=3; jogador2.gas=10; jogador2.balas=10
        jogador2.max_balas=20; jogador2.max_gas=10
        l1.cadencia=0.4; l1.pv=2
        subchefe.pv=5
      if dificuldade=='dificil':
        jogador.pv=1; jogador.gas=9; jogador.balas=5
        jogador.max_balas=15; jogador.max_gas=9
        jogador2.pv=1; jogador2.gas=9; jogador2.balas=5
        jogador2.max_balas=15; jogador2.max_gas=9
        
        l1.cadencia=0.6; l1.pv=3
        subchefe.pv=8

  #atribuição dos objetos e personagens
  lista_sprites=pygame.sprite.Group()
  lista_plataformas=pygame.sprite.Group()
  lista_balas=pygame.sprite.Group()
  lista_aliens=pygame.sprite.Group()
  lista_morte_instatanea=pygame.sprite.Group()
  lista_balas_aliens=pygame.sprite.Group()
  lista_colunas=pygame.sprite.Group()
  lista_chaves=pygame.sprite.Group()
  lista_portas=pygame.sprite.Group()
  lista_ajudantes=pygame.sprite.Group()
  jogador=Player('jogador1')
  l1=Aliens(1000, 320, 'cb', 'chave')
  subchefe=Subchefe(540, 570)
  ch1=Plataforma(janela_x/2, 600, janela_x, 50)
  coluna1=Coluna(200, 480, 50, 200)
  pi1=Plataforma(675, 380, 1000, 40)
  portal=Portal()
  porta1=Porta(360, 480, False)
  porta2=Porta(560, 480, True)
  ajudante=Ajudante()
  lista_aliens.add(l1)
  lista_morte_instatanea.add(subchefe)
  lista_plataformas.add(ch1, pi1)
  lista_colunas.add(coluna1)
  lista_portas.add(porta1, porta2)
  lista_sprites.add(porta1, porta2, portal, ch1, coluna1, pi1, l1, subchefe, jogador)

  if dois_jogadores:
    jogador2=Player('jogador2')
    jogador2.x-=20
    lista_sprites.add(jogador2)

  #fundo de imagem
  fundo=pygame.image.load('imagens/img_1/fundo_teste1.png')
  fundo=pygame.transform.scale(fundo, (1300, 600))

  #textos do jogo
  fonte=pygame.font.SysFont('Comic Sans', 40, True, True)
  fonte2=pygame.font.SysFont('Comic Sans', 60, True, True)

  #dificuldade
  if dificuldade=='facil':
    jogador.pv=5; jogador.gas=13; jogador.balas=15
    jogador.max_balas=25; jogador.max_gas=13
    l1.cadencia=0.1; l1.pv=1
    subchefe.pv=2
    if dois_jogadores:
      jogador2.pv=5; jogador2.gas=13; jogador2.balas=15
      jogador2.max_balas=25; jogador2.max_gas=13
  elif dificuldade=='medio':
    jogador.pv=3; jogador.gas=10; jogador.balas=10
    jogador.max_balas=20; jogador.max_gas=10
    l1.cadencia=0.4; l1.pv=2
    subchefe.pv=5
    if dois_jogadores:
      jogador2.pv=3; jogador2.gas=10; jogador2.balas=10
      jogador2.max_balas=20; jogador2.max_gas=10
  elif dificuldade=='dificil':
    jogador.pv=1; jogador.gas=9; jogador.balas=5
    jogador.max_balas=15; jogador.max_gas=9
    l1.cadencia=0.6; l1.pv=3
    subchefe.pv=8
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
          pausar('fase_2')
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
    parede=pygame.sprite.spritecollide(jogador, lista_colunas, False, pygame.sprite.collide_mask)
    bala_plataforma=pygame.sprite.groupcollide(lista_balas, lista_plataformas, True, False, pygame.sprite.collide_mask)
    bala_plataforma_alien=pygame.sprite.groupcollide(lista_balas_aliens, lista_plataformas, True, False, pygame.sprite.collide_mask)
    bala_coluna=pygame.sprite.groupcollide(lista_balas, lista_colunas, True, False, pygame.sprite.collide_mask)
    bala_porta=pygame.sprite.groupcollide(lista_balas, lista_portas, True, False, pygame.sprite.collide_mask)
    bala_coluna_alien=pygame.sprite.groupcollide(lista_balas_aliens, lista_colunas, True, False, pygame.sprite.collide_mask)
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
        if jogador.x<plataforma.rect.centerx-450:
          jogador.x-=10
        if jogador.x>plataforma.rect.centerx+450:
          jogador.x+=10
    else:
      jogador.gravidade=True
    if parede:
      barreira=parede[-1]
      if jogador.x<barreira.rect.centerx+20:
        jogador.x-=10
      if jogador.x>barreira.rect.centerx:
        jogador.x+=10

    if dois_jogadores:
      pisando2=pygame.sprite.spritecollide(jogador2, lista_plataformas, False, pygame.sprite.collide_mask)
      if pisando2:
        plataforma2=pisando2[-1]
        if jogador2.y<plataforma2.rect.centery:
          jogador2.gravidade=False
          if jogador2.gas<jogador2.max_gas:
            jogador2.gas+=0.25
        else:
          if jogador2.y>plataforma2.rect.centery+50:
            jogador2.y+=10
          if jogador2.x<plataforma2.rect.centerx-450:
            jogador2.x-=10
          if jogador2.x>plataforma2.rect.centerx+450:
            jogador2.x+=10
      else:
        jogador2.gravidade=True

      parede2=pygame.sprite.spritecollide(jogador2, lista_colunas, False, pygame.sprite.collide_mask)
      if parede2:
        barreira2=parede2[-1]
        if jogador2.x<barreira2.rect.centerx+20:
          jogador2.x-=10
        if jogador2.x>barreira2.rect.centerx:
          jogador2.x+=10

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
          from fases.fase1.fase1_3 import iniciar_fase3
          iniciar_fase3()

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
        continuar = fonte2.render('pressionem SPACE ou 0 para avançar', True, (0, 0, 0))
        janela.blit(ganhou, (375, 200))
        janela.blit(continuar, (100, 300))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_KP0]:
          from fases.fase1.fase1_3 import iniciar_fase3
          iniciar_fase3()
      
    pygame.display.flip()