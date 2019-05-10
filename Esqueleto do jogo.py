# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:59:18 2019

@author: Tonera
"""

# Importando as bibliotecas necessárias.
import pygame
from os import path

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')

# Dados gerais do jogo.
WIDTH = 1400 # Largura da tela
HEIGHT = 750 # Altura da tela
FPS = 60 # Frames por segundo

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
        player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
        self.image = player_img
        
        #Diminuindo o tamanho da imagem
        self.image = pygame.transform.scale(player_img, (50,38))
        
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
        if self.rect.right > HEIGHT:
            self.rect.right = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
            


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


# Comando para evitar travamentos.
try:
    
    # Loop principal.
    running = True
    while running:
        
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado
            if event.type == pygame.QUIT:
                running = False
                
            #Verifica se apertou alguma tela 
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade
                if event.key == pygame.K_DOWN:
                    player.speedy = -8
                if event.key == pygame.K_UP:
                    player.speedy = 8
                    
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
    
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
