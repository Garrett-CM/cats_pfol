# Cats, Paws of Fury
# ======================

import pygame
import math

# ---------------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------------
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TITLE         = "Cats: Paws of Fury"
FPS           = 60

# grabbed a gothic color palette (R, G, B)
DEEP_PURPLE = (40, 0, 60)
BLOOD_RED   = (139, 0, 0)
PALE_GOLD   = (200, 180, 100)
GHOST_WHITE = (220, 220, 240)
DARK_GREY   = (30, 30, 30)
LIGHT_GREY  = (80, 80, 80)
GREEN       = (0, 255, 0)
ORANGE      = (255, 165, 0)
PURPLE      = (128, 0, 128)
TOXIC_GREEN = (50, 205, 50)
POOP_BROWN  = (101, 67, 33)

#start game & window size
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True
dt = 0

# Font for UI
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# ---------------------------------------------------------------------------
# CHARACTER CLASSES
# ---------------------------------------------------------------------------
class Cat:
    def __init__(self, name, x, y, color, is_selected=False):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.is_selected = is_selected
        self.radius = 40
        self.health = 100
        self.max_health = 100
        self.attack_cooldown = 0
        self.attack_active = False
        self.attack_timer = 0
        self.attack_type = None
        
        # Movement
        self.speed = 300
        self.direction = pygame.Vector2(1, 0)
        
    def update(self, dt):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
        if self.attack_timer > 0:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attack_active = False
    
    def draw(self, screen):
        # Draw cat body (placeholder circle)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw eyes (placeholder)
        eye_offset = 15
        eye_size = 8
        # Left eye
        pygame.draw.circle(screen, GHOST_WHITE, (int(self.x - eye_offset), int(self.y - 10)), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x - eye_offset + 3), int(self.y - 8)), 4)
        # Right eye
        pygame.draw.circle(screen, GHOST_WHITE, (int(self.x + eye_offset), int(self.y - 10)), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + eye_offset + 3), int(self.y - 8)), 4)
        
        # Draw health bar
        bar_width = 60
        bar_height = 8
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 15
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLOOD_RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, PALE_GOLD, (bar_x, bar_y, bar_width * health_ratio, bar_height))
        
        # Draw attack effect if active
        if self.attack_active:
            if self.attack_type == "scratch":
                # Draw scratch marks
                for i in range(3):
                    angle = math.radians(i * 30 - 30)
                    start_x = self.x + math.cos(angle) * self.radius
                    start_y = self.y + math.sin(angle) * self.radius
                    end_x = self.x + math.cos(angle + 0.5) * (self.radius + 30)
                    end_y = self.y + math.sin(angle + 0.5) * (self.radius + 30)
                    pygame.draw.line(screen, GHOST_WHITE, (start_x, start_y), (end_x, end_y), 4)
            elif self.attack_type == "bodyslam":
                # Draw shockwave effect
                pygame.draw.circle(screen, PALE_GOLD, (int(self.x), int(self.y)), self.radius + 20, 3)
            elif self.attack_type == "tweeker_scratch":
                # Draw toxic scratch marks
                for i in range(3):
                    angle = math.radians(i * 30 - 30)
                    start_x = self.x + math.cos(angle) * self.radius
                    start_y = self.y + math.sin(angle) * self.radius
                    end_x = self.x + math.cos(angle + 0.5) * (self.radius + 30)
                    end_y = self.y + math.sin(angle + 0.5) * (self.radius + 30)
                    pygame.draw.line(screen, TOXIC_GREEN, (start_x, start_y), (end_x, end_y), 4)
            elif self.attack_type == "poopy_butt":
                # Draw brown aura
                pygame.draw.circle(screen, POOP_BROWN, (int(self.x), int(self.y)), self.radius + 25, 3)
                # Draw some dots
                for i in range(8):
                    angle = math.radians(i * 45)
                    dot_x = self.x + math.cos(angle) * (self.radius + 30)
                    dot_y = self.y + math.sin(angle) * (self.radius + 30)
                    pygame.draw.circle(screen, POOP_BROWN, (int(dot_x), int(dot_y)), 4)

class Luby(Cat):
    def __init__(self, x, y):
        super().__init__("Luby", x, y, (20, 20, 25))  # Dark grey/black
        self.speed = 200  # Slower
        self.health = 150
        self.max_health = 150
        self.description = "Heavy tank - Black cat with green eyes"
        
    def scratch(self, enemies):
        """Basic scratch attack"""
        if self.attack_cooldown <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "scratch"
            self.attack_timer = 0.3
            self.attack_cooldown = 0.8
            # Check if enemies are in range
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if distance < self.radius + 50:
                    enemy.health -= 15
                    enemy.knockback(self.direction, 100)
            return True
        return False
    
    def bodyslam(self, enemies):
        """Heavy bodyslam attack"""
        if self.attack_cooldown <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "bodyslam"
            self.attack_timer = 0.4
            self.attack_cooldown = 1.5
            # Check if enemies are in range (larger AoE)
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if distance < self.radius + 80:
                    enemy.health -= 30
                    enemy.knockback(self.direction, 200)
            return True
        return False

class Calzone(Cat):
    def __init__(self, x, y):
        super().__init__("Calzone", x, y, (210, 140, 50))  # Orange
        self.speed = 350  # Faster
        self.health = 70
        self.max_health = 70
        self.poopy_butt_active = False
        self.poopy_butt_timer = 0
        self.description = "Scraggly light orange cat - Vietnam vet vibes"
        
    def update(self, dt):
        super().update(dt)
        if self.poopy_butt_active:
            self.poopy_butt_timer -= dt
            if self.poopy_butt_timer <= 0:
                self.poopy_butt_active = False
                # Remove buff
                self.damage_multiplier = 1.0
                self.damage_taken_multiplier = 1.0
                # Reset color slightly
                self.color = (210, 140, 50)
    
    def tweeker_scratch(self, enemies):
        """Scratch with toxic debuff"""
        if self.attack_cooldown <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "tweeker_scratch"
            self.attack_timer = 0.3
            self.attack_cooldown = 0.6
            # Check if enemies are in range
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if distance < self.radius + 45:
                    # Apply toxic debuff (damage over time)
                    enemy.health -= 10
                    enemy.toxic_timer = 2.0  # Toxic effect for 2 seconds
                    enemy.is_toxic = True
                    enemy.knockback(self.direction, 80)
            return True
        return False
    
    def poopy_butt(self, enemies=None):
        """Poopy butt - 3x damage but take more damage"""
        if self.attack_cooldown <= 0 and not self.poopy_butt_active:
            self.poopy_butt_active = True
            self.poopy_butt_timer = 5.0  # Lasts 5 seconds
            self.attack_active = True
            self.attack_type = "poopy_butt"
            self.attack_timer = 0.5
            self.attack_cooldown = 8.0  # Long cooldown
            # Apply buff
            self.damage_multiplier = 3.0
            self.damage_taken_multiplier = 1.5
            # Change color to show buff
            self.color = (160, 100, 50)
            return True
        return False

# ---------------------------------------------------------------------------
# ENEMY CLASS
# ---------------------------------------------------------------------------
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 30
        self.health = 50
        self.max_health = 50
        self.speed = 80
        self.is_toxic = False
        self.toxic_timer = 0
        self.color = (150, 50, 50)  # Reddish
        self.direction = pygame.Vector2(0, 0)
    
    def update(self, dt, target):
        # Move towards target
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.hypot(dx, dy)
        if distance > 50:  # Don't get too close
            self.x += (dx / distance) * self.speed * dt if distance > 0 else 0
            self.y += (dy / distance) * self.speed * dt if distance > 0 else 0
        
        # Toxic damage over time
        if self.is_toxic:
            self.toxic_timer -= dt
            if self.toxic_timer <= 0:
                self.is_toxic = False
            else:
                self.health -= 5 * dt  # 5 damage per second
    
    def knockback(self, direction, force):
        self.x += direction.x * force * 0.1
        self.y += direction.y * force * 0.1
    
    def draw(self, screen):
        # Draw enemy
        if self.is_toxic:
            color = TOXIC_GREEN
        else:
            color = self.color
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        
        # Draw eyes (angry)
        eye_offset = 10
        # Left eye
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x - eye_offset), int(self.y - 5)), 6)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x - eye_offset - 3), int(self.y - 3)), 3)
        # Right eye
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x + eye_offset), int(self.y - 5)), 6)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + eye_offset + 3), int(self.y - 3)), 3)
        
        # Health bar
        bar_width = 40
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 10
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLOOD_RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, PALE_GOLD, (bar_x, bar_y, bar_width * health_ratio, bar_height))
        
        # Toxic indicator
        if self.is_toxic:
            pygame.draw.circle(screen, TOXIC_GREEN, (int(self.x), int(self.y)), self.radius + 10, 2)

# ---------------------------------------------------------------------------
# GAME STATE
# ---------------------------------------------------------------------------
class GameState:
    def __init__(self):
        self.state = "menu"  # menu, playing, game_over
        self.selected_character = None
        self.player = None
        self.enemies = []
        self.enemy_spawn_timer = 0
        
    def start_game(self, character_type):
        if character_type == "luby":
            self.player = Luby(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.player = Calzone(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.state = "playing"
        self.enemies = []
        self.enemy_spawn_timer = 0

game = GameState()

# ---------------------------------------------------------------------------
# MENU FUNCTIONS
# ---------------------------------------------------------------------------
def draw_menu():
    screen.fill(DEEP_PURPLE)
    
    # Title
    title_text = font.render("Cats: Paws of Fury", True, PALE_GOLD)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    
    subtitle = small_font.render("Choose your fighter:", True, GHOST_WHITE)
    subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 150))
    screen.blit(subtitle, subtitle_rect)
    
    # Character cards
    luby_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, 200, 200, 300)
    calzone_rect = pygame.Rect(SCREEN_WIDTH // 2 + 50, 200, 200, 300)
    
    # Luby card
    pygame.draw.rect(screen, DARK_GREY, luby_rect, border_radius=10)
    pygame.draw.rect(screen, PALE_GOLD, luby_rect, 2, border_radius=10)
    # Luby preview
    pygame.draw.circle(screen, (20, 20, 25), (luby_rect.centerx, luby_rect.centery - 30), 50)
    pygame.draw.circle(screen, GREEN, (luby_rect.centerx - 15, luby_rect.centery - 40), 6)
    pygame.draw.circle(screen, GREEN, (luby_rect.centerx + 15, luby_rect.centery - 40), 6)
    # Luby text
    luby_name = font.render("Luby", True, GHOST_WHITE)
    luby_name_rect = luby_name.get_rect(center=(luby_rect.centerx, luby_rect.bottom - 80))
    screen.blit(luby_name, luby_name_rect)
    luby_desc = small_font.render("Tank - Heavy", True, LIGHT_GREY)
    luby_desc_rect = luby_desc.get_rect(center=(luby_rect.centerx, luby_rect.bottom - 50))
    screen.blit(luby_desc, luby_desc_rect)
    luby_hint = small_font.render("Press 1", True, PALE_GOLD)
    luby_hint_rect = luby_hint.get_rect(center=(luby_rect.centerx, luby_rect.bottom - 20))
    screen.blit(luby_hint, luby_hint_rect)
    
    # Calzone card
    pygame.draw.rect(screen, DARK_GREY, calzone_rect, border_radius=10)
    pygame.draw.rect(screen, PALE_GOLD, calzone_rect, 2, border_radius=10)
    # Calzone preview
    pygame.draw.circle(screen, (210, 140, 50), (calzone_rect.centerx, calzone_rect.centery - 30), 45)
    pygame.draw.circle(screen, (0, 0, 0), (calzone_rect.centerx - 15, calzone_rect.centery - 40), 5)
    pygame.draw.circle(screen, (0, 0, 0), (calzone_rect.centerx + 15, calzone_rect.centery - 40), 5)
    # Calzone text
    calzone_name = font.render("Calzone", True, GHOST_WHITE)
    calzone_name_rect = calzone_name.get_rect(center=(calzone_rect.centerx, calzone_rect.bottom - 80))
    screen.blit(calzone_name, calzone_name_rect)
    calzone_desc = small_font.render("Scraggly - Fast", True, LIGHT_GREY)
    calzone_desc_rect = calzone_desc.get_rect(center=(calzone_rect.centerx, calzone_rect.bottom - 50))
    screen.blit(calzone_desc, calzone_desc_rect)
    calzone_hint = small_font.render("Press 2", True, PALE_GOLD)
    calzone_hint_rect = calzone_hint.get_rect(center=(calzone_rect.centerx, calzone_rect.bottom - 20))
    screen.blit(calzone_hint, calzone_hint_rect)
    
    # Instructions at bottom
    instructions = small_font.render("Select character with 1 or 2", True, GHOST_WHITE)
    instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(instructions, instructions_rect)

def draw_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    game_over_text = font.render("GAME OVER", True, BLOOD_RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(game_over_text, game_over_rect)
    
    restart_text = small_font.render("Press R to restart", True, GHOST_WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(restart_text, restart_rect)

# ---------------------------------------------------------------------------
# PLAYING STATE UI
# ---------------------------------------------------------------------------
def draw_hud():
    # Player info
    if game.player:
        name_text = small_font.render(f"{game.player.name}", True, PALE_GOLD)
        screen.blit(name_text, (20, 20))
        
        # Health bar
        health_text = small_font.render("HP", True, GHOST_WHITE)
        screen.blit(health_text, (20, 50))
        bar_width = 200
        bar_height = 20
        bar_x = 60
        bar_y = 50
        health_ratio = game.player.health / game.player.max_health
        pygame.draw.rect(screen, DARK_GREY, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, BLOOD_RED, (bar_x, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(screen, PALE_GOLD, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Attack info
        attack_text = small_font.render("1: Scratch  2: Bodyslam/Tweeker Scratch  3: Poopy Butt (Calzone)", True, GHOST_WHITE)
        screen.blit(attack_text, (20, SCREEN_HEIGHT - 40))
        
        # Enemy count
        enemy_text = small_font.render(f"Enemies: {len(game.enemies)}", True, GHOST_WHITE)
        screen.blit(enemy_text, (SCREEN_WIDTH - 150, 20))
        
        # Poison indicator for Calzone
        if game.player.__class__.__name__ == "Calzone":
            calzone = game.player
            if calzone.poopy_butt_active:
                buff_text = small_font.render("💩 POOPY BUTT ACTIVE! 3x DMG!", True, POOP_BROWN)
                screen.blit(buff_text, (SCREEN_WIDTH // 2 - 150, 20))
                # Timer remaining
                timer_text = small_font.render(f"{calzone.poopy_butt_timer:.1f}s", True, POOP_BROWN)
                timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
                screen.blit(timer_text, timer_rect)

# ---------------------------------------------------------------------------
# MAIN GAME LOOP
# ---------------------------------------------------------------------------
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game.state == "menu":
                if event.key == pygame.K_1:
                    game.start_game("luby")
                elif event.key == pygame.K_2:
                    game.start_game("calzone")
            elif game.state == "playing":
                if game.player:
                    if event.key == pygame.K_1:
                        if game.player.__class__.__name__ == "Luby":
                            game.player.scratch(game.enemies)
                        else:
                            game.player.tweeker_scratch(game.enemies)
                    elif event.key == pygame.K_2:
                        if game.player.__class__.__name__ == "Luby":
                            game.player.bodyslam(game.enemies)
                        else:
                            game.player.poopy_butt()
                    elif event.key == pygame.K_r:
                        # Reset enemies
                        game.enemies = []
                        game.player.health = game.player.max_health
                        if game.player.__class__.__name__ == "Calzone":
                            game.player.poopy_butt_active = False
                            game.player.damage_multiplier = 1.0
                            game.player.damage_taken_multiplier = 1.0
                            game.player.color = (210, 140, 50)
            elif game.state == "game_over":
                if event.key == pygame.K_r:
                    game.state = "menu"
                    game.enemies = []
                    game.player = None

    # Update
    if game.state == "playing" and game.player:
        # Player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        
        # Normalize diagonal movement
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length
            game.player.direction = pygame.Vector2(dx, dy)
            game.player.x += dx * game.player.speed * dt
            game.player.y += dy * game.player.speed * dt
        
        # Keep player on screen
        game.player.x = max(game.player.radius, min(game.player.x, SCREEN_WIDTH - game.player.radius))
        game.player.y = max(game.player.radius, min(game.player.y, SCREEN_HEIGHT - game.player.radius))
        
        # Update player
        game.player.update(dt)
        
        # Check if player is dead
        if game.player.health <= 0:
            game.state = "game_over"
            game.player.health = 0
        
        # Spawn enemies
        game.enemy_spawn_timer -= dt
        if game.enemy_spawn_timer <= 0:
            import random
            side = random.randint(0, 3)
            if side == 0:  # Top
                x = random.randint(0, SCREEN_WIDTH)
                y = -50
            elif side == 1:  # Bottom
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT + 50
            elif side == 2:  # Left
                x = -50
                y = random.randint(0, SCREEN_HEIGHT)
            else:  # Right
                x = SCREEN_WIDTH + 50
                y = random.randint(0, SCREEN_HEIGHT)
            game.enemies.append(Enemy(x, y))
            game.enemy_spawn_timer = 2.0  # Spawn every 2 seconds
        
        # Update enemies
        enemies_to_remove = []
        for i, enemy in enumerate(game.enemies):
            enemy.update(dt, game.player)
            if enemy.health <= 0:
                enemies_to_remove.append(i)
            # Check if enemy touches player
            distance = math.hypot(enemy.x - game.player.x, enemy.y - game.player.y)
            if distance < game.player.radius + enemy.radius:
                # Damage player
                damage = 10
                if hasattr(game.player, 'damage_taken_multiplier'):
                    damage *= game.player.damage_taken_multiplier
                game.player.health -= damage
                # Knockback player
                kb_direction = pygame.Vector2(game.player.x - enemy.x, game.player.y - enemy.y)
                if kb_direction.length() > 0:
                    kb_direction = kb_direction.normalize()
                    game.player.x += kb_direction.x * 50
                    game.player.y += kb_direction.y * 50
        
        # Remove dead enemies (reverse order)
        for i in sorted(enemies_to_remove, reverse=True):
            game.enemies.pop(i)
    
    # Draw everything
    screen.fill(DEEP_PURPLE)
    
    if game.state == "menu":
        draw_menu()
    elif game.state == "playing":
        # Draw player
        game.player.draw(screen)
        
        # Draw enemies
        for enemy in game.enemies:
            enemy.draw(screen)
        
        # Draw HUD
        draw_hud()
        
        # Attack cooldown indicator for Luby
        if game.player.__class__.__name__ == "Luby":
            if game.player.attack_cooldown > 0:
                cooldown_text = small_font.render(f"Cooldown: {game.player.attack_cooldown:.1f}s", True, LIGHT_GREY)
                screen.blit(cooldown_text, (20, 80))
        else:
            # Calzone poison bar
            if game.player.poopy_butt_active:
                poison_text = small_font.render(f"💩 {game.player.poopy_butt_timer:.1f}s", True, POOP_BROWN)
                screen.blit(poison_text, (20, 80))
    
    elif game.state == "game_over":
        draw_game_over()
    
    # Update display
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000

pygame.quit()