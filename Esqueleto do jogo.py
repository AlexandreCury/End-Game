# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:59:18 2019

@author: Tonera
"""

# Importando as bibliotecas necessárias.
import pygame
import random
from os import path, environ

environ['SDL_VIDEO_CENTERED'] = '1'

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# Dados gerais do jogo.
WIDTH = 1200 # Largura da tela
HEIGHT = 600 # Altura da tela
FPS = 50 # Frames por segundo

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



# Essa função assume que os sprites no sprite sheet possuem todos o mesmo tamanho.
def load_spritesheet(spritesheet, rows, columns):
    # Calcula a largura e altura de cada sprite.
    sprite_width = spritesheet.get_width() // columns
    sprite_height = spritesheet.get_height() // rows 
    
    # Percorre todos os sprites adicionando em uma lista.
    sprites = []
    for row in range(rows):
        for column in range(columns):
            # Calcula posição do sprite atual
            x = column * sprite_width
            y = row * sprite_height
            # Define o retângulo que contém o sprite atual
            dest_rect = pygame.Rect(x, y, sprite_width, sprite_height)

            # Cria uma imagem vazia do tamanho do sprite
            image = pygame.Surface((sprite_width, sprite_height))
                        
            # Copia o sprite atual (do spritesheet) na imagem
            image.blit(spritesheet, (0, 0), dest_rect)
            sprites.append(image)
    
    return sprites


#Classe Jogador que representa a nave:
class Player(pygame.sprite.Sprite):
    
    #Construtor da classe
    def __init__(self):
        
        #Construtor da classe pai (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        #Carregando a imagem de fundo
        
        player_img = pygame.image.load(path.join(img_dir, "sprite_player_sheet2.png")).convert_alpha()

        # Aumenta o tamanho do spritesheet para ficar mais fácil de ver
        player_sheet = pygame.transform.scale(player_img, (263, 240))
                
        # Define sequências de sprites de cada animação
        self.animation = load_spritesheet(player_sheet, 3, 3)
                        
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]

        
        #Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        #Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Posiciona o dog
        self.rect.centery = WIDTH / 10
        self.rect.bottom = HEIGHT - 375
              
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 300
              
        #Velocidade da nave
        self.speedy = 0
        self.speedx = 0
        
    # Metodo que atualiza a posição do dog
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now

            # Avança um quadro.
            self.frame += 1
        
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            #Deixa invisível
            self.image.set_colorkey(BLACK)
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            
        
        # Mantem dentro da tela
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > 350:
            self.rect.right = 350
        if self.rect.left < 0:
            self.rect.left = 0



class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "plane2.png")).convert()
        mob_img_mask = pygame.mask.from_surface(mob_img)
        self.image = mob_img_mask
        
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
        self.speedx = VEL_MAP -10
        self.speedy = 0

        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85 / 85)


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
        mob_img = pygame.image.load(path.join(img_dir, "bomba.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (70, 48))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = WIDTH
        
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(HEIGHT - 80)
        
        # Sorteia uma velocidade inicial
        self.speedx = VEL_MAP
        self.speedy=0

        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85/10)

        # Metodo que atualiza a posição da bomba
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Coins(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "moeda.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (70, 48))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = WIDTH
        
        # Sorteia um lugar inicial em y
        self.rect.y = random.randrange(HEIGHT - 80)
        
        # Sorteia uma velocidade inicial
        self.speedx = VEL_MAP
        self.speedy=0

        # Melhora a colisão estabelecendo um raio de um circulo
        self.radius = int(self.rect.width * .85/100)

        # Metodo que atualiza a posição da bomba
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
class Explosion1(pygame.sprite.Sprite):
    
    #constroi a classe
    def __init__(self,x,y):
         # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "explosion-2283147_960_720.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (70, 48))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        #posicao
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = x
        
        # Sorteia um lugar inicial em y
        self.rect.y = y
        
        self.speedx =VEL_MAP + 2
        self.speedy=0
        
        self.tempo = pygame.time.get_ticks()
        
        #atualiza a função
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        now =  pygame.time.get_ticks()
        if now - self.tempo > 200:
            self.kill()
            
class Explosion2(pygame.sprite.Sprite):
    
    #constroi a classe
    def __init__(self,x,y):
         # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "Explosao2.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (70, 48))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        #posicao
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = x
        
        # Sorteia um lugar inicial em y
        self.rect.y = y
        
        self.speedx = VEL_MAP + 2
        self.speedy=0
        
        self.tempo = pygame.time.get_ticks()
        
        #atualiza a função
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        now =  pygame.time.get_ticks()
        if now - self.tempo > 500:
            self.kill()
            
class Explosion3(pygame.sprite.Sprite):
    
    #constroi a classe
    def __init__(self,x,y):
         # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "explosao3.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (70, 48))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        #posicao
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = x
        
        # Sorteia um lugar inicial em y
        self.rect.y = y
        
        self.speedx = VEL_MAP + 2
        self.speedy=0
        
        self.tempo = pygame.time.get_ticks()
        
        #atualiza a função
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        now =  pygame.time.get_ticks()
        if now - self.tempo > 700:
            self.kill()
            

class Money(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        mob_img = pygame.image.load(path.join(img_dir, "cifrao.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(mob_img, (70, 48))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        #posicao
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = x
        
        # Sorteia um lugar inicial em y
        self.rect.y = y
        
         # Sorteia uma velocidade inicial
        self.speedx = -3 + VEL_MAP
        self.speedy=-3.5
        
        self.tempo = pygame.time.get_ticks()
        
        #atualiza a função
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        now =  pygame.time.get_ticks()
        if now - self.tempo > 500:
            self.kill()
        

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Nome do jogo
pygame.display.set_caption("End Game")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'Fundo.png')).convert()
background_rect = background.get_rect()

#musica de fundo do jogo
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

#Cria uma nave. O construtor será chamado automaticamente
player = Player()

# Cria um grupo de sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Cria um grupo só dos aviões n
mobs = pygame.sprite.Group()

# Cria um grupo só das bombas
bomb = pygame.sprite.Group()
boom_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))

# Cria um grupo só das moedas
coins = pygame.sprite.Group()

# cria um grupo só das explosoes
explosions = pygame.sprite.Group()

#cria um grupo dos cifores
moneys = pygame.sprite.Group()

# Define texto
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text_yellow(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Velocidade com que o mapa se move
VEL_MAP = -5

# Score
score = 0

#le recorde score
with open("Score.txt", "r") as arquivo:
    score_maximo= arquivo.read()

#Contador
contador = 0

# Comando para evitar travamentos.
try:
    
    #Variavel mudança de mapa
    X = 0
    X2 = WIDTH

    # Vida
    life = 1

    # Moedas
    moedas = 0
    
    pygame.mixer.music.play(loops=-1)
    # Loop principal.
    while life > 0:
        
        #contador
        contador += 1
        VEL_MAP-=0.003

        if contador == 10:
            score +=1
            contador = 0

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
            
        # Sortear quando vai ocorrer um evento (avião, bomba, etc)
        sorteia_eventos = random.randint(0,100)

        if sorteia_eventos == 1 or sorteia_eventos == 57 or sorteia_eventos == 80:
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        
        if sorteia_eventos == 46:
            b = Bomb()
            all_sprites.add(b)
            bomb.add(b)

        if sorteia_eventos == 30 or sorteia_eventos == 90:
            c = Coins()
            all_sprites.add(c)
            coins.add(c)

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
                    
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                    
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                    
            # Depois de processar os eventos.
            # Atualiza a ação de cada sprite.
        all_sprites.update()

        # Verifica se houve colisão

        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_mask)
        hits_bomb = pygame.sprite.spritecollide(player, bomb, True, pygame.sprite.collide_mask)
        hits_coins = pygame.sprite.spritecollide(player, coins, True, pygame.sprite.collide_mask)


        if hits:
            life -= 1
            VEL_MAP-=0.5
        
        if hits_bomb:
            life -= 1
            VEL_MAP-=0.5
        
        #chama a explosão com a bomba
        for m in hits_bomb:
            x=m.rect.centerx
            y=m.rect.centery
            e=Explosion1(x,y)
            all_sprites.add(e) 
            o=Explosion2(x,y)
            all_sprites.add(o)
            w=Explosion3(x,y)
            all_sprites.add(w)
        
        if hits_coins:
            # Toca o som da colisão
            boom_sound.play()
            moedas += 1
            
        for m in hits_coins:
            x=m.rect.centerx
            y=m.rect.centery
            j=Money(x,y)
            all_sprites.add(j)
        
        # Troca moedas por vida
        moedas_por_vida = 5
        if moedas == moedas_por_vida:
            if life < 4:
                moedas = 0
                life +=1
            else:
                moedas = moedas_por_vida
                
        for m in hits:
            x=m.rect.centerx
            y=m.rect.centery
            e=Explosion1(x,y)
            all_sprites.add(e)
            o=Explosion2(x,y)
            all_sprites.add(o)
            w=Explosion3(x,y)
            all_sprites.add(w)


        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK )
        screen.blit(background, background_rect)

        # Atualiza a posição da imagem de fundo.
        background_rect.x += VEL_MAP

        # Se o fundo saiu da janela, faz ele voltar para dentro.
        if background_rect.right < 0:
            background_rect.x += background_rect.width
            
        screen.blit(background, background_rect)

        background_rect2 = background_rect.copy()
        background_rect2.x += background_rect2.width
        screen.blit(background, background_rect2)
        all_sprites.draw(screen)

        # Mostrar Score
        pontuacao= "Seu score : {0}".format(score)
        draw_text_yellow(screen, pontuacao, 30, WIDTH / 2, 40)

        #Score Máximo:
        draw_text_yellow(screen, "Recorde {0}".format(str(score_maximo)), 30, WIDTH / 2, 10)
        #Atualiza o score maximo
        if score > int(score_maximo):
            with open("Score.txt", "w") as arquivo:
                arquivo.write(str(score))

        # Aviso de modas
        aviso= "A cada 5 moedas, você ganha 1 vida, chegando a 4 vidas no maximo"
        if score < 10: #mostra a mensagem por 4 segundos
            draw_text(screen, aviso, 30, WIDTH / 2, HEIGHT-50)
        
        # Vida
        vida_atual= "Vida = {}".format(life)
        draw_text(screen, str(vida_atual), 30, WIDTH*9/10, 10)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
