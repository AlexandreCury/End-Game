# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:59:18 2019

@author: Tonera
"""

# Importando as bibliotecas necessárias.
import pygame
import random
from os import path

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')

# Dados gerais do jogo.
WIDTH = 1200 # Largura da tela
HEIGHT = 600 # Altura da tela
<<<<<<< HEAD
FPS = 50 # Frames por segundo
=======
FPS = 40 # Frames por segundo
>>>>>>> fb912d129043a49539775b0c4bb395aff004544b

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

#Classe Jogador que representa a nave:
class Player(pygame.sprite.Sprite):
    
    #Construtor da classe
    def __init__(self):
        
        #Construtor da classe pai (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando a imagem de fundo
        player_img = pygame.image.load(path.join(img_dir, "Dog.png")).convert()
        self.image = player_img
        
        #Diminuindo o tamanho da imagem
        self.image = pygame.transform.scale(player_img, (100,68))
        
        #Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        #Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        #Centraliza embaixo da tela
        self.rect.centery = WIDTH / 10
        self.rect.bottom = HEIGHT - 375
        
        #Velocidade da nave
        self.speedy = 0
        
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.y += self.speedy
        
        # Mantem dentro da tela
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "plane2.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (80, 48))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = WIDTH
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(HEIGHT - 80)
        # Sorteia uma velocidade inicial
        self.speedx = -5
        self.speedy = 0

        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 2)

        # Metodo que atualiza a posição do avião
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Bomb(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "Bomb2.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (80, 48))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = 400 #random.randrange(400 - 500)
        # Sorteia um lugar inicial em y
        self.rect.y = 0
        # Sorteia uma velocidade inicial
        self.speedx = -6
        self.speedy = 6

        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85)

        # Metodo que atualiza a posição da bomba
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
      
# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("End Game")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'Fundo.png')).convert()
background_rect = background.get_rect()

#Cria uma nave. O construtor será chamado automaticamente
player = Player()
# Cria um grupo de sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Cria um grupo só dos aviões
mobs = pygame.sprite.Group()

# Cria um grupo só das bombas
bomb = pygame.sprite.Group()

# Comando para evitar travamentos.
try:
    
    # Loop principal.
    running = True
    while running:
        
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Sortear quando vai ocorrer um evento (avião, bomba, etc)
        sorteia_eventos = random.randint(0,30)
        if sorteia_eventos == 1:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        
        if sorteia_eventos == 5:
            b = Bomb()
            all_sprites.add(b)
            bomb.add(b)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
                
            #Verifica se apertou alguma tela 
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade
                if event.key == pygame.K_DOWN:
                    player.speedy = 8
                if event.key == pygame.K_UP:
                    player.speedy = -8
                    
            #Verifica se solto alguma tecla
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade
                if event.key == pygame.K_DOWN:
                    player.speedy = 0
                if event.key == pygame.K_UP:
                    player.speedy = 0
                    
            # Depois de processar os eventos.
            # Atualiza a ação de cada sprite.
        all_sprites.update()

        # Verifica se houve colisão
        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        hits_bomb = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle) #substituir mobs por bomb p poder matar
        if hits:
            # Toca o som da colisão
            #boom_sound.play()
            #time.sleep(1) # Precisa esperar senão fecha
            running = False
        if hits_bomb:
            # Toca o som da colisão
            #boom_sound.play()
            #time.sleep(1) # Precisa esperar senão fecha
            running = False
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
