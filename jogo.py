import os
import pygame
pygame.init()

TAMANHO = WIDTH, HEIGHT = 720, 480
BACKGROUND_COLOR = pygame.Color('black')
FPS = 30
GRAVIDADE = 0.7
FORCA_IMPULSO = 15

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

        tamanho_animaçao = (120, 120)  # This should match the tamanho_animaçao of the images.
        resized = [pygame.transform.scale(image, tamanho_animaçao) for image in images_running]
        self.rect = pygame.Rect(position, tamanho_animaçao)
        self.images = resized
        self.images_right = resized  # images
        self.images_left = [pygame.transform.flip(image, True, False) for image in resized]  # Flipping every image.
        self.index = 0
        self.images_idle = [pygame.transform.scale(image, tamanho_animaçao) for image in images_idle]

        self.image = self.images_idle[self.index]
        self.velocity = pygame.math.Vector2(0, 0)

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update(self, dt):
        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left
        else:
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
def main():
    images_running = load_images(path='./imagens')
    images_idle = load_images(path='./imagens')
    player = AnimatedSprite(position=(300, 300),
        images_running=images_running , images_idle=images_idle)
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.velocity.x = 4
                elif event.key == pygame.K_LEFT:
                    player.velocity.x = -4
                elif event.key == pygame.K_DOWN:
                    player.velocity.y = 4
                if event.key == pygame.K_UP:
                    player.velocity.y = -12
                elif event.key == pygame.K_SPACE:
                    player.velocity.y = - FORCA_IMPULSO
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.velocity.x = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    player.velocity.y = 0

        all_sprites.update(dt)
        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
