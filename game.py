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
clock = pygame.time.Clock()
running = True
# dt is delta time in seconds since last frame, used for framerate independent physics.
dt = 0


#TODO what does this MEAN?
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

#game loop
while running:
    #handle event
        #this handles closing the app
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update
    screen.fill(DARK_GREY)
        #makes user a circle
    pygame.draw.circle(screen, PALE_GOLD, player_pos, 40)

        #key movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    #keep player on screen
    if player_pos.x < 0 or player_pos.x > SCREEN_WIDTH:
        player_pos.x = max(0, min(player_pos.x, SCREEN_WIDTH))
    if player_pos.y < 0 or player_pos.y > SCREEN_HEIGHT:
        player_pos.y = max(0, min(player_pos.y, SCREEN_HEIGHT))


    #display the updates
    pygame.display.flip()
    #limit FPS? IDK but it allows the dot to move
    dt = clock.tick(60) / 1000

#game ends when this is hit
pygame.quit