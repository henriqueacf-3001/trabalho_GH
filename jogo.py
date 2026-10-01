import os
import random
import pygame
pygame.init()

TAMANHO = WIDTH, HEIGHT = 720, 480
BACKGROUND_COLOR = pygame.Color('black')
FPS = 30
GRAVIDADE = 0.7
FORCA_IMPULSO = 15
VELOCIDADE_OBSTACULOS = 200

screen = pygame.display.set_mode(TAMANHO)
clock = pygame.time.Clock()


def load_images(path):
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert_alpha()
        images.append(image)
    return images


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position, images_running, images_idle):
        super(AnimatedSprite, self).__init__()

        tamanho_animaçao = (120, 120)
        resized = [pygame.transform.scale(image, tamanho_animaçao) for image in images_running]
        self.rect = pygame.Rect(position, tamanho_animaçao)
        self.images = resized
        self.index = 0
        self.images_idle = [pygame.transform.scale(image, tamanho_animaçao) for image in images_idle]

        self.image = self.images_idle[self.index]
        self.velocity = pygame.math.Vector2(0, 0)

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update(self, dt):
        self.velocity.x = 0
        self.images = self.images_idle

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.velocity.y += GRAVIDADE

        self.rect.move_ip(*self.velocity)

        if self.rect.y > HEIGHT-120:
            self.rect.y = HEIGHT-120
        if self.rect.y < 0:
            self.rect.y = 0

    def colidiu(self, obstaculos):
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo.rect):
                if pygame.sprite.collide_mask(self, obstaculo) is not None:
                    return obstaculo
        return None
       

class Fundo:
    def __init__(self, caminho, tamanho):
        imagem_original = pygame.image.load(caminho).convert()
        self.image = pygame.transform.scale(imagem_original, tamanho)

    def desenhar(self, tela):
        tela.blit(self.image, (0, 0))


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, cima_baixo):
        super(Obstaculo, self).__init__()
        self.cima_baixo = cima_baixo
        tamanhos_possiveis = [90, 140, 180, 210]
        posicoes_possiveis = [700, 850, 900,  1000, 1150, 1300]
        tamanho_imagem = random.choice(tamanhos_possiveis)

        if self.cima_baixo == 'cima':
            self.imagem_original = pygame.image.load('obstaculos' + os.sep + 'laser_cima.png').convert_alpha()
            altura_imagem = -7
        else:
            self.imagem_original = pygame.image.load('obstaculos' + os.sep + 'laser_baixo.png').convert_alpha()
            altura_imagem = HEIGHT-tamanho_imagem +7
        
        self.image = pygame.transform.scale(self.imagem_original, (80, tamanho_imagem))
        self.rect = self.image.get_rect(topleft=(random.choice(posicoes_possiveis), altura_imagem))
        self.x = float(self.rect.x)
        self.velocidade = VELOCIDADE_OBSTACULOS

    def update(self, dt):
        self.x -= self.velocidade * dt
        self.rect.x = int(self.x)

        if self.rect.right < 0:
            # self.x = float(random.randint(WIDTH + 100, WIDTH + 500))
            # self.rect.x = int(self.x)
            tamanhos_possiveis = [90, 140, 180, 220]
            posicoes_possiveis = [700, 850, 900,  1000, 1150, 1300]
            tamanho_imagem = random.choice(tamanhos_possiveis)
    
            if self.cima_baixo == 'cima':
                altura_imagem = -7
            else:
                altura_imagem = HEIGHT-tamanho_imagem +7

            self.image = pygame.transform.scale(self.imagem_original, (80, tamanho_imagem))
            self.rect = self.image.get_rect(topleft=(random.choice(posicoes_possiveis), altura_imagem))
            self.x = float(self.rect.x)

def main():
    fundo = Fundo('./fundo/WhatsApp Image 2026-09-23 at 19.08.39.jpeg', TAMANHO)
    images_running = load_images(path='./imagens')
    images_idle = images_running
    player = AnimatedSprite(position=(300, 300),images_running=images_running , images_idle=images_idle)
    all_sprites = pygame.sprite.Group(player)

    obstaculo_1 = Obstaculo('cima')
    obstaculo_2 = Obstaculo('baixo')
    obstaculo_3 = Obstaculo('cima')
    obstaculo_4 = Obstaculo('baixo')
    obstaculo_5 = Obstaculo('cima')
    obstaculo_6 = Obstaculo('baixo')
    obstaculo_7 = Obstaculo('cima')
    obstaculo_8 = Obstaculo('baixo')
    obstaculo_9 = Obstaculo('cima')
    obstaculo_10 = Obstaculo('baixo')
    obstaculo_11= Obstaculo('cima')
    obstaculo_12= Obstaculo('baixo')
    

    
    obstaculos = pygame.sprite.Group(
        obstaculo_1, obstaculo_2, obstaculo_3,
        obstaculo_4, obstaculo_5, obstaculo_6, obstaculo_7, obstaculo_8, obstaculo_9,
                obstaculo_10, obstaculo_11, obstaculo_12
    )

    clock.tick()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.velocity.y = 4
                elif event.key == pygame.K_UP:
                    player.velocity.y = -12
                elif event.key == pygame.K_SPACE:
                    player.velocity.y = - FORCA_IMPULSO
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    player.velocity.y = 0

        all_sprites.update(dt)
        obstaculos.update(dt)

        if player.colidiu(obstaculos):
            print('O jogador colidiu com um obstáculo')
            running = False

        fundo.desenhar(screen)
        obstaculos.draw(screen)
        all_sprites.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
