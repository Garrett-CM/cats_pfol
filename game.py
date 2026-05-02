# Cats, Paws of litter 
# ======================

import pygame

# ---------------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------------
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TITLE         = "Cats, Pocket Full of Litter"
FPS           = 60

# grabbed a gothic color palette (R, G, B)
DEEP_PURPLE = (40, 0, 60)
BLOOD_RED   = (139, 0, 0)
PALE_GOLD   = (200, 180, 100)
GHOST_WHITE = (220, 220, 240)
DARK_GREY   = (30, 30, 30)

#start game & window size
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

#starting game loop
running = True
while running:
    #handle event
        #this handles closing the app
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update
    screen.fill(DARK_GREY)
    #draw
    pygame.display.flip()

pygame.quit