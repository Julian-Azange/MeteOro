import pygame, random

# Configuración de la ventana y colores
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Inicialización de Pygame y configuración de la ventana
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()


# Función para dibujar texto en la pantalla
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# Función para dibujar la barra de escudo del jugador
def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)


def show_menu():
    screen.fill(BLACK)
    draw_text(screen, "MeteOro", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Presione ENTER para iniciar", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Presione I para ver las instrucciones", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:  # Iniciar el juego al presionar ENTER
                    waiting = False
                if event.key == pygame.K_i:  # Mostrar instrucciones al presionar "I"
                    show_instructions()


def show_instructions():
    screen.fill(BLACK)
    draw_text(screen, "INSTRUCCIONES", 50, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "🔼 🔽 Mover con las flechas", 25, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(screen, "␣ Disparar con la barra espaciadora", 25, WIDTH // 2, HEIGHT // 2 + 50)
    draw_text(screen, "💥 Evita los meteoros y sobrevive", 25, WIDTH // 2, HEIGHT // 2 + 100)
    draw_text(screen, "Presiona la tecla BORRAR para volver", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:  # Volver al menú principal
                    show_menu()
                    waiting = False


def show_game_over_screen(score):
    screen.fill(BLACK)
    draw_text(screen, "JUEGO TERMINADO", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, f"Puntaje: {score}", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Presiona ENTER para volver al Menu", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:  # Volver al menú principal
                    show_menu()
                    waiting = False


# Clase que representa al jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

    # Actualiza la posición del jugador
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        # Evitar que el jugador se salga de la pantalla
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    # Crea una bala cuando el jugador dispara
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Clase que representa los meteoros enemigos
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    # Actualiza la posición del meteoro
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # Si el meteoro sale de la pantalla, reaparece desde arriba
        if (
            self.rect.top > HEIGHT + 10
            or self.rect.left < -40
            or self.rect.right > WIDTH + 40
        ):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10)


# Clase que representa las balas disparadas por el jugador
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    # Actualiza la posición de la bala
    def update(self):
        self.rect.y += self.speedy
        # Si la bala sale de la pantalla, se elimina
        if self.rect.bottom < 0:
            self.kill()


# Clase que representa las explosiones cuando un meteoro es destruido
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # Velocidad de la animación de explosión

    # Actualiza la animación de la explosión
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            # Si la animación ha terminado, elimina la explosión
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Pantalla de inicio del juego
def show_go_screen():
    screen.blit(background, [0, 0])
    draw_text(screen, "MeteOro", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Instruciones van aquí", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Presiona cualquier tecla", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# Cargar imágenes de los meteoros
meteor_images = []
meteor_list = [
    "assets/meteorGrey_big1.png",
    "assets/meteorGrey_big2.png",
    "assets/meteorGrey_big3.png",
    "assets/meteorGrey_big4.png",
    "assets/meteorGrey_med1.png",
    "assets/meteorGrey_med2.png",
    "assets/meteorGrey_small1.png",
    "assets/meteorGrey_small2.png",
    "assets/meteorGrey_tiny1.png",
    "assets/meteorGrey_tiny2.png",
]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

# Cargar imágenes de explosión
explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.image.load("assets/background.png").convert()

# Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)

# Variables para el control del juego
game_over = True
running = True
while running:
    if game_over:
        show_menu()  # Mostrar el menú inicial
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    # colisiones - meteoro - laser
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # colisiones - jugador - meteoro
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True
            show_game_over_screen(score)  # Mostrar el puntaje final

    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # Marcador
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # Escudo
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()

pygame.quit()
