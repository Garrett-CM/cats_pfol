# Cats, Paws of Fury
# ======================

import pygame
import math
import random

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
SNOT_GREEN  = (150, 200, 50)

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
medium_font = pygame.font.Font(None, 28)

# ---------------------------------------------------------------------------
# HIGH SCORE SYSTEM
# ---------------------------------------------------------------------------
class HighScoreManager:
    def __init__(self):
        self.scores = []
        
    def add_score(self, name, score):
        self.scores.append({"name": name, "score": score})
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        if len(self.scores) > 10:
            self.scores = self.scores[:10]
            
    def get_top_scores(self):
        return self.scores

high_score_manager = HighScoreManager()
current_player_name = ""
showing_name_input = False

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
        self.attack_cooldown_j = 0
        self.attack_cooldown_k = 0
        self.attack_cooldown_l = 0
        self.attack_active = False
        self.attack_timer = 0
        self.attack_type = None
        
        # Movement
        self.speed = 300
        self.direction = pygame.Vector2(1, 0)
        self.facing = pygame.Vector2(1, 0)  # Last movement direction
        
        # Score tracking
        self.kills = 0
        
    def update(self, dt):
        if self.attack_cooldown_j > 0:
            self.attack_cooldown_j -= dt
        if self.attack_cooldown_k > 0:
            self.attack_cooldown_k -= dt
        if self.attack_cooldown_l > 0:
            self.attack_cooldown_l -= dt
        if self.attack_timer > 0:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attack_active = False
    
    def draw(self, screen):
        # Draw cat body (placeholder circle)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw facing direction indicator (small triangle)
        tip_x = self.x + self.facing.x * (self.radius + 10)
        tip_y = self.y + self.facing.y * (self.radius + 10)
        pygame.draw.polygon(screen, PALE_GOLD, [
            (tip_x, tip_y),
            (self.x + self.facing.x * self.radius - self.facing.y * 10,
             self.y + self.facing.y * self.radius + self.facing.x * 10),
            (self.x + self.facing.x * self.radius + self.facing.y * 10,
             self.y + self.facing.y * self.radius - self.facing.x * 10)
        ])
        
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
        self.draw_attack_effect(screen)
    
    def draw_attack_effect(self, screen):
        if not self.attack_active:
            return
            
        if self.attack_type == "scratch":
            # Draw scratch marks in facing direction
            for i in range(3):
                angle = math.radians(i * 30 - 30)
                start_x = self.x + self.facing.x * self.radius + math.cos(angle) * 15
                start_y = self.y + self.facing.y * self.radius + math.sin(angle) * 15
                end_x = self.x + self.facing.x * (self.radius + 40) + math.cos(angle + 0.5) * 15
                end_y = self.y + self.facing.y * (self.radius + 40) + math.sin(angle + 0.5) * 15
                pygame.draw.line(screen, GHOST_WHITE, (start_x, start_y), (end_x, end_y), 4)
                
        elif self.attack_type == "bodyslam":
            # Draw dash trail
            pygame.draw.circle(screen, PALE_GOLD, (int(self.x), int(self.y)), self.radius + 30, 3)
            pygame.draw.circle(screen, PALE_GOLD, (int(self.x + self.facing.x * 20), int(self.y + self.facing.y * 20)), self.radius + 10, 2)
            
        elif self.attack_type == "belly_drag":
            # Draw healing aura
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius + 25, 3)
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius + 15, 2)
            
        elif self.attack_type == "tweeker_scratch":
            # Draw toxic scratch marks
            for i in range(3):
                angle = math.radians(i * 30 - 30)
                start_x = self.x + self.facing.x * self.radius + math.cos(angle) * 15
                start_y = self.y + self.facing.y * self.radius + math.sin(angle) * 15
                end_x = self.x + self.facing.x * (self.radius + 40) + math.cos(angle + 0.5) * 15
                end_y = self.y + self.facing.y * (self.radius + 40) + math.sin(angle + 0.5) * 15
                pygame.draw.line(screen, TOXIC_GREEN, (start_x, start_y), (end_x, end_y), 4)
                
        elif self.attack_type == "poopy_butt":
            # Draw AoE zone
            zone_radius = self.radius * 2.75
            pygame.draw.circle(screen, POOP_BROWN, (int(self.x), int(self.y)), zone_radius, 3)
            pygame.draw.circle(screen, POOP_BROWN, (int(self.x), int(self.y)), zone_radius - 10, 2)
            # Draw some floating dots
            for i in range(12):
                angle = math.radians(i * 30)
                dot_x = self.x + math.cos(angle) * (zone_radius - 20)
                dot_y = self.y + math.sin(angle) * (zone_radius - 20)
                pygame.draw.circle(screen, POOP_BROWN, (int(dot_x), int(dot_y)), 4)
                
        elif self.attack_type == "sneeze":
            # Draw snot cone
            cone_length = 100
            cone_angle = 15  # 30° total arc
            points = []
            points.append((self.x + self.facing.x * self.radius, self.y + self.facing.y * self.radius))
            
            # Calculate cone spread
            left_angle = math.atan2(self.facing.y, self.facing.x) - math.radians(cone_angle)
            right_angle = math.atan2(self.facing.y, self.facing.x) + math.radians(cone_angle)
            
            left_x = self.x + self.facing.x * self.radius + math.cos(left_angle) * cone_length
            left_y = self.y + self.facing.y * self.radius + math.sin(left_angle) * cone_length
            right_x = self.x + self.facing.x * self.radius + math.cos(right_angle) * cone_length
            right_y = self.y + self.facing.y * self.radius + math.sin(right_angle) * cone_length
            
            points.append((left_x, left_y))
            points.append((right_x, right_y))
            
            pygame.draw.polygon(screen, SNOT_GREEN, points, 2)
            pygame.draw.polygon(screen, (SNOT_GREEN[0], SNOT_GREEN[1], SNOT_GREEN[2], 50), points, 0)
            # Draw some snot particles
            for i in range(5):
                dist = random.randint(20, 80)
                angle = math.atan2(self.facing.y, self.facing.x) + random.uniform(-0.3, 0.3)
                px = self.x + math.cos(angle) * dist
                py = self.y + math.sin(angle) * dist
                pygame.draw.circle(screen, SNOT_GREEN, (int(px), int(py)), 3)

class Luby(Cat):
    def __init__(self, x, y):
        super().__init__("Luby", x, y, (20, 20, 25))  # Dark grey/black
        self.speed = 180  # Slower
        self.health = 150
        self.max_health = 150
        self.description = "Heavy tank - Black cat with green eyes"
        self.slow_timer = 0
        self.base_speed = 180
        
    def update(self, dt):
        super().update(dt)
        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.speed = self.base_speed
    
    def scratch(self, enemies):
        """Basic scratch attack - deals 50% enemy HP"""
        if self.attack_cooldown_j <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "scratch"
            self.attack_timer = 0.3
            self.attack_cooldown_j = 0.8
            # Check if enemies are in range
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if distance < self.radius + 50:
                    # Check if enemy is in front (within 90° of facing direction)
                    to_enemy = pygame.Vector2(enemy.x - self.x, enemy.y - self.y)
                    if to_enemy.length() > 0:
                        to_enemy = to_enemy.normalize()
                        dot_product = self.facing.dot(to_enemy)
                        if dot_product > 0.3:  # Within ~72° cone
                            enemy.health -= enemy.max_health * 0.5  # 50% HP damage
                            enemy.knockback(self.facing, 100)
                            if enemy.health <= 0:
                                self.kills += 1
            return True
        return False
    
    def bodyslam(self, enemies):
        """Body slam - Dash/charge that damages and passes through enemies"""
        if self.attack_cooldown_k <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "bodyslam"
            self.attack_timer = 0.4
            self.attack_cooldown_k = 1.5
            # Dash in facing direction
            dash_distance = 150
            self.x += self.facing.x * dash_distance
            self.y += self.facing.y * dash_distance
            # Damage enemies in path
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if distance < self.radius + 60:
                    enemy.health -= 30
                    enemy.knockback(self.facing, 200)
                    if enemy.health <= 0:
                        self.kills += 1
            # Keep on screen
            self.x = max(self.radius, min(self.x, SCREEN_WIDTH - self.radius))
            self.y = max(self.radius, min(self.y, SCREEN_HEIGHT - self.radius))
            return True
        return False
    
    def belly_drag(self, enemies=None):
        """Belly drag - Heal 75% max HP, apply 2-second speed slow"""
        if self.attack_cooldown_l <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "belly_drag"
            self.attack_timer = 0.5
            self.attack_cooldown_l = 4.0  # Longer cooldown for healing
            # Heal 75% max HP
            self.health = min(self.max_health, self.health + self.max_health * 0.75)
            # Apply speed slow
            self.speed = self.base_speed * 0.5
            self.slow_timer = 2.0
            return True
        return False

class Calzone(Cat):
    def __init__(self, x, y):
        super().__init__("Calzone", x, y, (210, 140, 50))  # Orange
        self.speed = 350  # Faster
        self.health = 70
        self.max_health = 70
        self.description = "Scraggly light orange cat - Vietnam vet vibes"
        self.base_speed = 350
        
    def tweeker_scratch(self, enemies):
        """Tweaker scratch - Toxic debuff: kills in 3 hits or 1 hit + debuff"""
        if self.attack_cooldown_j <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "tweeker_scratch"
            self.attack_timer = 0.3
            self.attack_cooldown_j = 0.6
            # Check if enemies are in range
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if distance < self.radius + 45:
                    # Check if enemy is in front
                    to_enemy = pygame.Vector2(enemy.x - self.x, enemy.y - self.y)
                    if to_enemy.length() > 0:
                        to_enemy = to_enemy.normalize()
                        dot_product = self.facing.dot(to_enemy)
                        if dot_product > 0.3:
                            enemy.health -= 15  # Direct damage
                            # Apply toxic debuff (30% HP over 3 seconds)
                            if not enemy.is_toxic:
                                enemy.is_toxic = True
                                enemy.toxic_timer = 3.0
                                enemy.toxic_damage = enemy.max_health * 0.1  # 10% per second
                            enemy.knockback(self.facing, 80)
                            if enemy.health <= 0:
                                self.kills += 1
            return True
        return False
    
    def poopy_butt(self, enemies):
        """Poopy butt - AoE slow and poison zone (2.75x player size)"""
        if self.attack_cooldown_k <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "poopy_butt"
            self.attack_timer = 0.5
            self.attack_cooldown_k = 8.0  # Long cooldown
            
            # Create AoE zone
            zone_radius = self.radius * 2.75
            # Check enemies in zone
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if distance < zone_radius:
                    # Apply slow (50% speed reduction)
                    enemy.slowed = True
                    enemy.slow_timer = 3.0
                    enemy.base_speed = enemy.speed
                    enemy.speed = enemy.base_speed * 0.5
                    # Apply poison tick damage (3% max HP per tick every 0.5s)
                    enemy.poison_timer = 3.0
                    enemy.poison_tick_timer = 0.5
                    enemy.poison_damage = enemy.max_health * 0.03
                    enemy.is_poisoned = True
            return True
        return False
    
    def sneeze(self, enemies):
        """Sneeze - Snot cone (30° arc), heals 10% HP, deals 20% max HP damage"""
        if self.attack_cooldown_l <= 0 and not self.attack_active:
            self.attack_active = True
            self.attack_type = "sneeze"
            self.attack_timer = 0.4
            self.attack_cooldown_l = 2.0
            
            # Calculate cone area
            cone_angle = 15  # 30° total arc
            cone_length = 120
            
            for enemy in enemies:
                to_enemy = pygame.Vector2(enemy.x - self.x, enemy.y - self.y)
                distance = to_enemy.length()
                if distance < cone_length + enemy.radius:
                    # Check if enemy is within cone angle
                    angle_to_enemy = math.atan2(to_enemy.y, to_enemy.x)
                    facing_angle = math.atan2(self.facing.y, self.facing.x)
                    angle_diff = abs(angle_to_enemy - facing_angle)
                    # Normalize angle difference
                    if angle_diff > math.pi:
                        angle_diff = 2 * math.pi - angle_diff
                    if angle_diff < math.radians(cone_angle):
                        # Heal Calzone (10% HP)
                        self.health = min(self.max_health, self.health + self.max_health * 0.1)
                        # Deal 20% max HP damage
                        enemy.health -= enemy.max_health * 0.2
                        enemy.knockback(self.facing, 50)
                        if enemy.health <= 0:
                            self.kills += 1
            return True
        return False

# ---------------------------------------------------------------------------
# ENEMY CLASS
# ---------------------------------------------------------------------------
class Enemy:
    def __init__(self, x, y, level=1):
        self.x = x
        self.y = y
        self.radius = 30
        self.max_health = 50 + (level - 1) * 10
        self.health = self.max_health
        self.speed = 80 + (level - 1) * 5
        self.base_speed = self.speed
        self.is_toxic = False
        self.toxic_timer = 0
        self.toxic_damage = 0
        self.is_poisoned = False
        self.poison_timer = 0
        self.poison_tick_timer = 0
        self.poison_damage = 0
        self.slowed = False
        self.slow_timer = 0
        self.color = (150, 50, 50)  # Reddish
        self.direction = pygame.Vector2(0, 0)
        self.level = level
        
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
                self.health -= self.toxic_damage * dt  # Damage per second
        
        # Poison damage over time (from poopy butt)
        if self.is_poisoned:
            self.poison_timer -= dt
            self.poison_tick_timer -= dt
            if self.poison_tick_timer <= 0:
                self.health -= self.poison_damage
                self.poison_tick_timer = 0.5
            if self.poison_timer <= 0:
                self.is_poisoned = False
        
        # Slow effect
        if self.slowed:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.slowed = False
                self.speed = self.base_speed
    
    def knockback(self, direction, force):
        self.x += direction.x * force * 0.1
        self.y += direction.y * force * 0.1
    
    def draw(self, screen):
        # Draw enemy
        if self.is_toxic:
            color = TOXIC_GREEN
        elif self.is_poisoned:
            color = POOP_BROWN
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
        
        # Status indicators
        if self.is_toxic:
            pygame.draw.circle(screen, TOXIC_GREEN, (int(self.x), int(self.y)), self.radius + 10, 2)
        if self.is_poisoned:
            pygame.draw.circle(screen, POOP_BROWN, (int(self.x), int(self.y)), self.radius + 8, 2)
        if self.slowed:
            pygame.draw.circle(screen, (100, 100, 255), (int(self.x), int(self.y)), self.radius + 5, 2)

# ---------------------------------------------------------------------------
# GAME STATE
# ---------------------------------------------------------------------------
class GameState:
    def __init__(self):
        self.state = "menu"  # menu, playing, game_over, paused, high_scores, name_input
        self.selected_character = None
        self.player = None
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.wave = 1
        self.enemies_killed = 0
        self.game_time = 0
        
    def start_game(self, character_type):
        if character_type == "luby":
            self.player = Luby(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.player = Calzone(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.state = "playing"
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.wave = 1
        self.enemies_killed = 0
        self.game_time = 0
        
    def get_score(self):
        if self.player:
            return (self.player.kills * 10) + (self.wave * 5) + int(self.game_time / 60)
        return 0

game = GameState()

# ---------------------------------------------------------------------------
# MENU FUNCTIONS
# ---------------------------------------------------------------------------
def draw_menu():
    screen.fill(DEEP_PURPLE)
    
    # Title
    title_text = font.render("Cats: Paws of Fury", True, PALE_GOLD)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_text, title_rect)
    
    subtitle = small_font.render("Choose your fighter:", True, GHOST_WHITE)
    subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 130))
    screen.blit(subtitle, subtitle_rect)
    
    # High scores button
    hs_text = small_font.render("Press H for High Scores", True, PALE_GOLD)
    hs_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, 170))
    screen.blit(hs_text, hs_rect)
    
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
    luby_desc = small_font.render("Tank - Black Cat", True, LIGHT_GREY)
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
    calzone_desc = small_font.render("Rogue - Orange Cat", True, LIGHT_GREY)
    calzone_desc_rect = calzone_desc.get_rect(center=(calzone_rect.centerx, calzone_rect.bottom - 50))
    screen.blit(calzone_desc, calzone_desc_rect)
    calzone_hint = small_font.render("Press 2", True, PALE_GOLD)
    calzone_hint_rect = calzone_hint.get_rect(center=(calzone_rect.centerx, calzone_rect.bottom - 20))
    screen.blit(calzone_hint, calzone_hint_rect)
    
    # Instructions at bottom
    instructions = small_font.render("WASD to move | J, K, L for attacks", True, GHOST_WHITE)
    instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
    screen.blit(instructions, instructions_rect)

def draw_high_scores():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    title_text = font.render("High Scores", True, PALE_GOLD)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    
    scores = high_score_manager.get_top_scores()
    if not scores:
        no_scores = small_font.render("No scores yet!", True, GHOST_WHITE)
        no_scores_rect = no_scores.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(no_scores, no_scores_rect)
    else:
        y_pos = 170
        for i, score_data in enumerate(scores[:10]):
            rank = f"#{i+1}"
            name = score_data["name"][:15]  # Truncate long names
            score = score_data["score"]
            text = f"{rank} {name} - {score} pts"
            color = PALE_GOLD if i < 3 else GHOST_WHITE
            score_text = small_font.render(text, True, color)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(score_text, score_rect)
            y_pos += 35
    
    back_text = small_font.render("Press ESC to return", True, LIGHT_GREY)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    screen.blit(back_text, back_rect)

def draw_name_input():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    prompt = font.render("Enter your name:", True, GHOST_WHITE)
    prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(prompt, prompt_rect)
    
    # Draw name input box
    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20, 300, 50)
    pygame.draw.rect(screen, DARK_GREY, input_rect)
    pygame.draw.rect(screen, PALE_GOLD, input_rect, 2)
    
    name_text = font.render(current_player_name + ("_" if pygame.time.get_ticks() % 1000 < 500 else ""), True, PALE_GOLD)
    name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 5))
    screen.blit(name_text, name_rect)
    
    hint = small_font.render("Press ENTER to submit, ESC to cancel", True, LIGHT_GREY)
    hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(hint, hint_rect)

def draw_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    game_over_text = font.render("GAME OVER", True, BLOOD_RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(game_over_text, game_over_rect)
    
    score = game.get_score()
    score_text = medium_font.render(f"Score: {score}", True, PALE_GOLD)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
    screen.blit(score_text, score_rect)
    
    kills_text = small_font.render(f"Kills: {game.player.kills if game.player else 0}", True, GHOST_WHITE)
    kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(kills_text, kills_rect)
    
    wave_text = small_font.render(f"Wave: {game.wave}", True, GHOST_WHITE)
    wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(wave_text, wave_rect)
    
    restart_text = small_font.render("Press R to restart | ESC for menu", True, GHOST_WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))
    screen.blit(restart_text, restart_rect)

def draw_pause():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    pause_text = font.render("PAUSED", True, PALE_GOLD)
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(pause_text, pause_rect)
    
    resume_text = small_font.render("Press SPACE to resume", True, GHOST_WHITE)
    resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(resume_text, resume_rect)

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
        
        # Score and wave
        score = game.get_score()
        score_text = small_font.render(f"Score: {score}", True, PALE_GOLD)
        screen.blit(score_text, (20, 80))
        
        # Attack info
        attack_text = small_font.render("J: Scratch/Tweaker | K: Bodyslam/Poopy | L: Belly Drag/Sneeze", True, GHOST_WHITE)
        screen.blit(attack_text, (20, SCREEN_HEIGHT - 40))
        
        # Enemy count and wave
        enemy_text = small_font.render(f"Wave: {game.wave}  Enemies: {len(game.enemies)}", True, GHOST_WHITE)
        screen.blit(enemy_text, (SCREEN_WIDTH - 200, 20))
        
        # Controls hint
        controls_text = small_font.render("SPACE: Pause", True, LIGHT_GREY)
        screen.blit(controls_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40))
        
        # Slow indicator for Luby
        if isinstance(game.player, Luby) and game.player.slow_timer > 0:
            slow_text = small_font.render("🐌 SLOWED", True, (100, 100, 255))
            screen.blit(slow_text, (20, 110))

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
                elif event.key == pygame.K_h:
                    game.state = "high_scores"
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    
            elif game.state == "high_scores":
                if event.key == pygame.K_ESCAPE:
                    game.state = "menu"
                    
            elif game.state == "name_input":
                if event.key == pygame.K_RETURN and current_player_name.strip():
                    # Submit name and return to menu
                    if game.state == "game_over":
                        # Add score from game over
                        high_score_manager.add_score(current_player_name.strip(), game.get_score())
                    game.state = "menu"
                    current_player_name = ""
                    showing_name_input = False
                elif event.key == pygame.K_ESCAPE:
                    game.state = "menu"
                    current_player_name = ""
                    showing_name_input = False
                elif event.key == pygame.K_BACKSPACE:
                    current_player_name = current_player_name[:-1]
                else:
                    # Add character if printable
                    if len(current_player_name) < 20 and event.unicode.isprintable():
                        current_player_name += event.unicode
                        
            elif game.state == "playing":
                if game.player:
                    if event.key == pygame.K_j:
                        if isinstance(game.player, Luby):
                            game.player.scratch(game.enemies)
                        else:
                            game.player.tweeker_scratch(game.enemies)
                    elif event.key == pygame.K_k:
                        if isinstance(game.player, Luby):
                            game.player.bodyslam(game.enemies)
                        else:
                            game.player.poopy_butt(game.enemies)
                    elif event.key == pygame.K_l:
                        if isinstance(game.player, Luby):
                            game.player.belly_drag()
                        else:
                            game.player.sneeze(game.enemies)
                    elif event.key == pygame.K_SPACE:
                        game.state = "paused"
                    elif event.key == pygame.K_r:
                        # Reset game
                        game.state = "menu"
                        game.player = None
                        game.enemies = []
                        
            elif game.state == "paused":
                if event.key == pygame.K_SPACE:
                    game.state = "playing"
                elif event.key == pygame.K_ESCAPE:
                    game.state = "menu"
                    game.player = None
                    game.enemies = []
                    
            elif game.state == "game_over":
                if event.key == pygame.K_r:
                    # Restart with same character
                    if game.player:
                        character_type = "luby" if isinstance(game.player, Luby) else "calzone"
                        # Prompt for name
                        showing_name_input = True
                        game.state = "name_input"
                        current_player_name = ""
                elif event.key == pygame.K_ESCAPE:
                    game.state = "menu"
                    game.player = None
                    game.enemies = []

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
            game.player.facing = pygame.Vector2(dx, dy)  # Update facing direction
            game.player.x += dx * game.player.speed * dt
            game.player.y += dy * game.player.speed * dt
        
        # Keep player on screen
        game.player.x = max(game.player.radius, min(game.player.x, SCREEN_WIDTH - game.player.radius))
        game.player.y = max(game.player.radius, min(game.player.y, SCREEN_HEIGHT - game.player.radius))
        
        # Update player
        game.player.update(dt)
        game.game_time += dt
        
        # Check if player is dead
        if game.player.health <= 0:
            game.player.health = 0
            game.state = "game_over"
            showing_name_input = True
            current_player_name = ""
            # We'll handle name input in the game_over state
        
        # Spawn enemies (increasing difficulty)
        spawn_rate = max(0.5, 2.0 - (game.wave - 1) * 0.1)
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
            game.enemies.append(Enemy(x, y, game.wave))
            game.enemy_spawn_timer = spawn_rate
            
            # Increase wave after certain number of spawns
            if len(game.enemies) > 10 + game.wave * 2:
                game.wave += 1
        
        # Update enemies
        enemies_to_remove = []
        for i, enemy in enumerate(game.enemies):
            enemy.update(dt, game.player)
            if enemy.health <= 0:
                enemies_to_remove.append(i)
                game.player.kills += 1
                game.enemies_killed += 1
            # Check if enemy touches player
            distance = math.hypot(enemy.x - game.player.x, enemy.y - game.player.y)
            if distance < game.player.radius + enemy.radius:
                # Damage player
                damage = 10
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
    elif game.state == "high_scores":
        draw_menu()  # Draw menu behind
        draw_high_scores()
    elif game.state == "name_input":
        if game.state == "game_over":
            draw_game_over()
        draw_name_input()
    elif game.state == "playing":
        # Draw player
        game.player.draw(screen)
        
        # Draw enemies
        for enemy in game.enemies:
            enemy.draw(screen)
        
        # Draw HUD
        draw_hud()
        
    elif game.state == "paused":
        # Draw game behind pause
        if game.player:
            game.player.draw(screen)
        for enemy in game.enemies:
            enemy.draw(screen)
        draw_hud()
        draw_pause()
        
    elif game.state == "game_over":
        draw_game_over()
        if showing_name_input:
            draw_name_input()
    
    # Update display
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000

pygame.quit()