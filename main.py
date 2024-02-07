import pygame
import sys
import time
import random
import math
#IMPORTS
pygame.init()
pygame.font.init()
pygame.mixer.init()
#Initializing
WIN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#WINDOW
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
#Screen Dimensions

TAN = 210, 180, 140
GREY = 169, 169, 169
RED = 255,0,0
GREEN = 0,255,0
#colors

start_image = pygame.image.load("_internal\\Images\\start.png")
exit_image = pygame.image.load("_internal\\Images\\exit.png")
upgrade_image = pygame.image.load("_internal\\Images\\upgrades.png")
panel_image = pygame.image.load("_internal\\Images\\panel.png")
panel_image = pygame.transform.scale(panel_image,(WIDTH, 300))
sword_img = pygame.image.load("_internal\\Images\\sword.png")


shield_upgrade_img = pygame.image.load("_internal\\Images\\shield_upgrade.png")
shield_upgrade_img = pygame.transform.scale(shield_upgrade_img, (95,95))
sword_upgrade_img = pygame.image.load("_internal\\Images\\sword_upgrade.png")
sword_upgrade_img = pygame.transform.scale(sword_upgrade_img, (95,95))
coin_upgrade_img = pygame.image.load("_internal\\Images\\coin_upgrade.png")
coin_upgrade_img = pygame.transform.scale(coin_upgrade_img, (95,95))
empty_tile_img = pygame.image.load("_internal\\Images\\empty_tile.png")
empty_tile_img = pygame.transform.scale(empty_tile_img, (95,95))
#Upgrades menu buttons
coin_img = pygame.image.load("_internal\\Images\\coin.png")
coin_img = pygame.transform.scale(shield_upgrade_img, (95,95))
#Images
pygame.display.set_icon(sword_img)
#Icon
pygame.display.set_caption("KnightsRoyal")
#Name

clock = pygame.time.Clock()
FPS = 120
#Frames Per Second
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect(center = (x,y))

        self.clicked = False
    def draw(self):
	    action = False
	    pos = pygame.mouse.get_pos()

	    if self.rect.collidepoint(pos):
		    if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
			    self.clicked = True
			    action = True

	    if pygame.mouse.get_pressed()[0] == 0:
		    self.clicked = False

	    WIN.blit(self.image, (self.rect.x, self.rect.y))

	    return action
#Button class
class Player():
    def __init__(self, x, y, name, scale, hp, damage, coins, max_hp):
        self.name = name
        self.action = 0
        
        self.alive = True
        self.coins = coins
        self.damage = damage
        self.hp = hp
        self.max_hp = max_hp

        self.x = x
        self.y = y

        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        temp_list = []
        

        for i in range(8):
            img = pygame.image.load(f'_internal/Images/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
		#load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'_internal/Images/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
		#load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'_internal/Images/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
		#load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'_internal/Images/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center = (x,y))
        self.rect.x = x
    def movement(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_d]:
            self.rect.x+=3.3

        elif keys[pygame.K_a]:
            self.rect.x-=3.3
    def update(self):
        animation_cooldown = 100 #millisecond
		#handle animation
        self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
		#if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
    def idle(self):
		#set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def attack(self):
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def hurt(self, move):
		#set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.rect.x += move
    def death(self):
		#set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def draw(self):
        WIN.blit(self.image, self.rect)
        self.rect.clamp_ip(WIN.get_rect())
def draw_panel():
    WIN.blit(panel_image, (0, HEIGHT-300))
class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp


	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(WIN, RED, (self.x, self.y, 500, 30))
		pygame.draw.rect(WIN, GREEN, (self.x, self.y, 500 * ratio, 30))
def bg_music(name):
    pygame.mixer.music.load(f"_internal\\Music\\{name}")
    pygame.mixer.music.play(-1,0.5)
class draw_text():
    def __init__(self,blit_text, x, y, scale):
        self.my_font = pygame.font.SysFont("Comic Sans", scale)
        self.text = self.my_font.render(f'{blit_text}', False, (0, 0, 0))
        self.rect = self.text.get_rect(center = (x,y))
    def draw(self):
        WIN.blit(self.text, (self.rect.x,self.rect.y))
class draw_image():
    def __init__(self,name, x, y, scale):
        self.image = pygame.image.load(f"_internal\\Images\\{name}")
        self.image = pygame.transform.scale(self.image, (scale,scale))
        self.rect = self.image.get_rect(center = (x,y))
    def draw(self):
        WIN.blit(self.image, (self.rect.x,self.rect.y))
#Player class
playing_exit_button = Button(48, 22, exit_image, 0.4)
#Creating objects

knight = Player(100, 500, 'Knight', 4, 100, 6, 0, 100)
knight_health_bar = HealthBar(50, HEIGHT - 150, knight.hp, knight.max_hp)
bandit = Player(800, 515, 'Bandit', 4, 100, 6, 0, 100)
bandit_health_bar = HealthBar(WIDTH/2 + 50, HEIGHT - 100, bandit.hp, bandit.max_hp)
bg_music("bg_music.mp3")

def playing():
    amplitude = 15
    frequency = 0.005

    knight_hp = 100
    bandit_hp = 100
    knight_coins = 10
    
    bandit_cooldown = 45
    knight_cooldown = 45
    new_game_cooldown = 120
    upgrade_cooldown = 0
    #cooldowns
    upgrade_height = 0


    sword_upgrade_cost = 5
    shield_upgrade_cost = 10
    coin_upgrade_cost = 15
    
    #upgrade costs
    while True:
        WIN.fill(TAN)
        clock.tick(FPS)
        bandit_cooldown -=1
        knight_cooldown -= 1
        upgrade_cooldown -= 2

        wave = 1

        current_time = pygame.time.get_ticks()
        y_position = HEIGHT // 2 + int(amplitude * math.sin(frequency * current_time))
        x_position = WIDTH // 2 + int(amplitude * math.sin(frequency * current_time))
        
        playing_start_button = Button(x_position, y_position, start_image, 0.8)
        
        upgrade_button = Button(WIDTH-20, HEIGHT/2+120-upgrade_height, upgrade_image, 0.5)
        shield_upgrade_button = Button(WIDTH-20, HEIGHT/2-200, shield_upgrade_img, 0.5)
        sword_upgrade_button = Button(WIDTH-20, HEIGHT/2-105, sword_upgrade_img, 0.5)
        coin_upgrade_button = Button(WIDTH-20, HEIGHT/2-10, coin_upgrade_img, 0.5)
        coins_amount_text = draw_text(knight.coins, WIDTH/2, y_position - 350, 40)
        coins_amount_image = draw_image("coin.png", WIDTH/2+50, y_position-350, 40)
        
        
        if playing_exit_button.draw():
            pygame.quit()
            sys.exit()
        if upgrade_cooldown > 0:
            if shield_upgrade_button.draw()and knight.coins >= shield_upgrade_cost:
                knight_hp += 20
                knight.coins -= shield_upgrade_cost
                shield_upgrade_cost += random.randint(5,25)
            if sword_upgrade_button.draw() and knight.coins >= sword_upgrade_cost:
                knight.damage += 4
                knight.coins -= sword_upgrade_cost
                sword_upgrade_cost += random.randint(5,20)
            if coin_upgrade_button.draw()and knight.coins >= coin_upgrade_cost:
                knight_coins += 5
                knight.coins -= coin_upgrade_cost
                coin_upgrade_cost += random.randint(15,30)
            shield_upgrade_coins_amount_image = draw_image("coin.png", WIDTH-10, HEIGHT/2-165, 20)
            shield_upgrade_coins_amount_text = draw_text(shield_upgrade_cost, WIDTH-35, HEIGHT/2-165, 20)

            sword_upgrade_coins_amount_image = draw_image("coin.png", WIDTH-10, HEIGHT/2-70, 20)
            sword_upgrade_coins_amount_text = draw_text(sword_upgrade_cost, WIDTH-35, HEIGHT/2-70, 20)

            coin_upgrade_coins_amount_image = draw_image("coin.png", WIDTH-10, HEIGHT/2+20, 20)
            coin_upgrade_coins_amount_text = draw_text(coin_upgrade_cost, WIDTH-35, HEIGHT/2+20, 20)
            
            shield_upgrade_coins_amount_image.draw()
            shield_upgrade_coins_amount_text.draw()
            sword_upgrade_coins_amount_image.draw()
            sword_upgrade_coins_amount_text.draw()
            coin_upgrade_coins_amount_image.draw()
            coin_upgrade_coins_amount_text.draw()
        if upgrade_cooldown <= 0:
            upgrade_height = 0
            
        #Buttons
        
        bandit.update()
        bandit.draw()
        knight.update()
        knight.draw()
        draw_panel()
        coins_amount_text.draw()
        coins_amount_image.draw()
        knight_health_bar.draw(knight.hp)
        bandit_health_bar.draw(bandit.hp)
        #Drawing objects
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and knight_cooldown <= 0 and knight.alive == True and bandit.alive == True:
            knight.attack()
            knight_cooldown = 45
            if knight.rect.colliderect(bandit.rect):
                random_knight_damage = random.randint(-2, 4)
                bandit.hp -= knight.damage + random_knight_damage
                bandit_cooldown = 38
                knight_cooldown = 38 + random.randint(-3,2)
                bandit.hurt(random.randint(110,150))
                if bandit.hp <= 0:
                    bandit.death()
                    bandit_cooldown = -1
                    bandit.alive = False
                    knight.coins += knight_coins
        if bandit_cooldown == 0 and knight.alive == True and bandit.alive == True:
            bandit_cooldown = 40
            bandit.attack()
            if bandit.rect.colliderect(knight.rect):
                random_bandit_damage = random.randint(-2, 5)
                knight.hp -= bandit.damage + random_bandit_damage
                knight.hurt(random.randint(-110,-90))
                knight_cooldown = 40
                bandit_cooldown = 36+random.randint(-5,3)
                bandit.rect.x -= random.randint(115, 130)
                if knight.hp <= 0:
                    knight.death()
                    bandit_cooldown = -1
                    knight.alive = False
                    knight.coins -= 5
        if bandit.alive == False or knight.alive == False:
            if playing_start_button.draw():
                knight.alive = True
                bandit.alive = True
                if bandit_hp <= 140:
                    bandit_hp+=15
                wave += 1
                knight.hp = knight_hp
                bandit.hp = bandit_hp
                if bandit.damage <= 40:
                    bandit.damage += 6 + random.randint(-2,5)
                knight.x = 100
                bandit.x = 700
                bandit.idle()
                knight.idle()
                if bandit_cooldown <= 15:
                    bandit_cooldown-=1.5
            if upgrade_button.draw():
                upgrade_height += 10000
                upgrade_cooldown = 120
            if wave == 15:
                bandit.damage += 10
        #Damage and cooldowns

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            knight.movement()
            
        pos = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)
        WIN.blit(sword_img, pos)
	#Custom cursor
        pygame.display.update()
def mainscreen_loop():

    amplitude = 15
    frequency = 0.005
    while True:
        WIN.fill(TAN)
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        y_position = HEIGHT // 2 + int(amplitude * math.sin(frequency * current_time))
        y_position2 = HEIGHT // 2 + int(amplitude * math.sin(frequency * -current_time))
        x_position = WIDTH // 2 + int(amplitude * math.sin(frequency * current_time))
        title = draw_text("KnightsRoyal", WIDTH/2, HEIGHT/2 - 350, 200)
        
        DEV_NAME = draw_text("Adyanth Rao", x_position, HEIGHT//2 + 300, 70)
        
        start_button = Button(WIDTH/2-150, y_position, start_image, 0.8)
        exit_button = Button(WIDTH/2+150, y_position2, exit_image, 0.8)
        if start_button.draw():
            playing()    
            
        if exit_button.draw():
            pygame.quit()
            sys.exit()
        title.draw()
        DEV_NAME.draw()
            
        pos = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)
        WIN.blit(sword_img, pos)
        #Custom cursor
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
mainscreen_loop()
