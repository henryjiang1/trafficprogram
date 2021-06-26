import pygame

intersection_hitbox1 = pygame.Rect(352, 240, 144, 144)
intersection_hitbox2 = pygame.Rect(1024, 240, 144, 144)

BLACK = (0, 0, 0)
RED = (230, 30, 30)


def draw_lanes(screen):
    # horizontal
    pygame.draw.line(screen, BLACK, (0, 240), (352, 240), 2)
    pygame.draw.line(screen, BLACK, (0, 384), (352, 384), 2)
    pygame.draw.line(screen, BLACK, (496, 240), (1024, 240), 2)
    pygame.draw.line(screen, BLACK, (496, 384), (1024, 384), 2)
    pygame.draw.line(screen, BLACK, (1168, 240), (1520, 240), 2)
    pygame.draw.line(screen, BLACK, (1168, 384), (1520, 384), 2)

    # vertical
    pygame.draw.line(screen, BLACK, (352, 0), (352, 240), 2)
    pygame.draw.line(screen, BLACK, (496, 0), (496, 240), 2)
    pygame.draw.line(screen, BLACK, (352, 384), (352, 624), 2)
    pygame.draw.line(screen, BLACK, (496, 384), (496, 624), 2)
    pygame.draw.line(screen, BLACK, (1024, 0), (1024, 240), 2)
    pygame.draw.line(screen, BLACK, (1168, 0), (1168, 240), 2)
    pygame.draw.line(screen, BLACK, (1024, 384), (1024, 624), 2)
    pygame.draw.line(screen, BLACK, (1168, 384), (1168, 624), 2)


def draw_boundaries(screen):
    # intersection
    pygame.draw.rect(screen, RED, intersection_hitbox1, 1)
    pygame.draw.rect(screen, RED, intersection_hitbox2, 1)

    # lane dividers
    pygame.draw.line(screen, BLACK, (0, 312), (352, 312), 1)
    pygame.draw.line(screen, BLACK, (496, 312), (1024, 312), 1)
    pygame.draw.line(screen, BLACK, (1168, 312), (1520, 312), 1)


    pygame.draw.line(screen, BLACK, (424, 0), (424, 240), 1)
    pygame.draw.line(screen, BLACK, (424, 384), (424, 624), 1)
    pygame.draw.line(screen, BLACK, (1096, 0), (1096, 240), 1)
    pygame.draw.line(screen, BLACK, (1096, 384), (1096, 624), 1)