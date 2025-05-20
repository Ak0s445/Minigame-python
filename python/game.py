import pygame
import random
import sys

# Inicializálás
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GáspárKiller - Többszintű")
clock = pygame.time.Clock()

# Színek és beállítások szintenként
LEVELS = [
    {"bg_color": (30, 30, 30), "enemy_speed": 2, "max_enemies": 8, "bullet_color": (255, 255, 0), "explosion_color": (255, 100, 0)},
    {"bg_color": (10, 50, 80), "enemy_speed": 3, "max_enemies": 12, "bullet_color": (0, 255, 255), "explosion_color": (0, 255, 100)},
    {"bg_color": (80, 0, 0), "enemy_speed": 5, "max_enemies": 20, "bullet_color": (255, 50, 0), "explosion_color": (255, 0, 0)},
]
current_level = 0

# Szövegek
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 48)

# Képek
enemy_img = pygame.image.load("assets/gaspi.png")
enemy_img = pygame.transform.scale(enemy_img, (80, 80))

# Célkereszt
crosshair_img = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.line(crosshair_img, (255, 0, 0), (15, 0), (15, 30), 2)
pygame.draw.line(crosshair_img, (255, 0, 0), (0, 15), (30, 15), 2)

# Játékállapotok
bullets = []
enemies = []
explosions = []
kill_count = 0
game_over = False
enemy_timer = 0
EXPLOSION_DURATION = 20
BULLET_SPEED = 10
enemy_spawn_delay = 60

# Ellenség létrehozása
def spawn_enemy():
    x = random.randint(0, WIDTH - 80)
    rect = enemy_img.get_rect(topleft=(x, -80))
    enemies.append(rect)

# Szint frissítése
def update_level():
    global current_level
    if kill_count >= 25:
        current_level = 2
    elif kill_count >= 10:
        current_level = 1

# Fő ciklus
running = True
while running:
    update_level()
    level_data = LEVELS[current_level]
    screen.fill(level_data["bg_color"])

    if not game_over:
        enemy_timer += 1
        if enemy_timer >= enemy_spawn_delay and len(enemies) < level_data["max_enemies"]:
            spawn_enemy()
            enemy_timer = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                bullet = pygame.Rect(mx - 4, my - 15, 8, 20 if current_level < 2 else 30)
                bullets.append(bullet)

        # Lövedék mozgás
        for bullet in bullets[:]:
            bullet.y -= BULLET_SPEED
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Ellenségek mozgása és találat
        for enemy in enemies[:]:
            enemy.y += level_data["enemy_speed"]
            if enemy.bottom > HEIGHT:
                game_over = True
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    explosions.append({'pos': enemy.center, 'timer': EXPLOSION_DURATION})
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    kill_count += 1
                    break

        # Rajzolás
        for enemy in enemies:
            screen.blit(enemy_img, enemy)

        for bullet in bullets:
            pygame.draw.rect(screen, level_data["bullet_color"], bullet)

        # Robbanások kirajzolása
        for explosion in explosions[:]:
            x, y = explosion['pos']
            pygame.draw.circle(screen, level_data["explosion_color"], (x, y), 30 + current_level * 10)
            explosion['timer'] -= 1
            if explosion['timer'] <= 0:
                explosions.remove(explosion)

        mx, my = pygame.mouse.get_pos()
        screen.blit(crosshair_img, (mx - 15, my - 15))

        level_text = f"GáspárKiller - Level {current_level + 1}"
        screen.blit(title_font.render(level_text, True, (255, 255, 255)), (WIDTH // 2 - 150, 10))
        kills_text = font.render(f"Megölt Gáspárok száma: {kill_count}", True, (255, 255, 255))
        screen.blit(kills_text, (20, HEIGHT - 40))

    else:
        over_text = title_font.render("VERESÉG! Gáspár elérte a földet!", True, (255, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
