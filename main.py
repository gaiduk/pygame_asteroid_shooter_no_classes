import random

import pygame
import sys


def laser_update(laser_list, speed=300):
    for rect in laser_list:
        rect.y -= speed * dt
        if rect.bottom < 0:
            laser_list.remove(rect)


def meteor_update(meteor_list, speed=200):
    for meteor_tuple in meteor_list:
        direction = meteor_tuple[1]

        meteor_tuple[0].center += direction * speed * dt
        if meteor_tuple[0].top > WINDOW_HEIGHT:
            meteor_list.remove(meteor_tuple)


def display_score():
    text_surf = font.render(f"Score {pygame.time.get_ticks() // 1000}", True, 'white')
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH//2 , WINDOW_HEIGHT - 80))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(30, 30), width=8, border_radius=5)


pygame.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

FPS = 120

clock = pygame.time.Clock()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid shooter")

ship_surf = pygame.image.load("graphics/ship.png").convert_alpha()
ship_rect = ship_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 150))

laser_surf = pygame.image.load("graphics/laser.png").convert_alpha()
laser_list = []

meteor_surf = pygame.image.load("graphics/meteor.png").convert_alpha()
meteor_list = []

can_shoot = True
shoot_time = 0


font = pygame.font.Font("graphics/subatomic.ttf", 50)
bg_surf = pygame.image.load("graphics/background.png").convert()

meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

laser_sound = pygame.mixer.Sound("sounds/laser.ogg")
explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
bg_music = pygame.mixer.Sound("sounds/music.wav")
bg_music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.re
            sys.exit()
        # if event.type == pygame.MOUSEMOTION:
        #     ship_rect.center = event.pos
        #
        if event.type == pygame.MOUSEBUTTONDOWN:
            laser_rect = laser_surf.get_rect()
            laser_rect.midbottom = ship_rect.midtop
            laser_list.append(laser_rect)
            laser_sound.play()
            # if can_shoot:
            #     laser_rect = laser_surf.get_rect()
            #     laser_rect.midbottom = ship_rect.midtop
            #     laser_list.append(laser_rect)
            #
            #     shoot_time = pygame.time.get_ticks()
            #
            #     can_shoot = False
            # if not can_shoot:
            #     current_time = pygame.time.get_ticks()
            #     if current_time - shoot_time > 100:
            #         can_shoot = True

        if event.type == meteor_timer:
            x_pos = random.randint(-50, WINDOW_WIDTH+50)
            y_pos = random.randint(-100, -50)
            meteor_rect = meteor_surf.get_rect(midbottom=(x_pos, y_pos))

            direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
            meteor_list.append((meteor_rect, direction))

    dt = clock.tick(FPS) / 1000

    ship_rect.center = pygame.mouse.get_pos()

    laser_update(laser_list)
    meteor_update(meteor_list)

    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            pygame.quit()
            sys.exit()

    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        for laser in laser_list:
            if meteor_rect.colliderect(laser):
                laser_list.remove(laser)
                meteor_list.remove(meteor_tuple)
                explosion_sound.play()

    display_surface.fill((0, 0, 0))
    display_surface.blit(bg_surf, (0, 0))
    for laser in laser_list:
        display_surface.blit(laser_surf, laser)

    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf, meteor_tuple[0])
    display_score()

    display_surface.blit(ship_surf, ship_rect)

    pygame.display.update()
