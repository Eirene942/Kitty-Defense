import pygame
import sys
import math
import random

pygame.init()



#screen

WIDTH= 1200
HEIGHT= 700
FPS = 60
screen= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kitty Defense!")
icon = pygame.image.load("icon.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# map settings
ROAD_Y = 300
ROAD_HEIGHT = 100
HOME_WIDTH = 300
HOME_X = WIDTH - HOME_WIDTH
#dog settings
DOG_SIZE = 80
DOG_RADIUS = DOG_SIZE // 2 

#cat settings
CAT_SIZE = 100
CAT_RADIUS = CAT_SIZE // 2 
CAT_RANGE = 180

#fonts
font = pygame.font.SysFont("arial", 24)
title_font = pygame.font.SysFont("arial", 30, bold=True)
title_extra_font = pygame.font.SysFont("arial", 55, bold= True)
help_font = pygame.font.SysFont("arial", 22, bold= True)
small_font = pygame.font.SysFont("arial", 18)

#sounds
meow_sound= pygame.mixer.Sound("dragon-studio-cute-cat-meow-472372.mp3")
bark_sound = pygame.mixer.Sound("dragon-studio-dog-bark-494308.mp3")


#images

#home
home_image = pygame.image.load("home.png").convert_alpha()
HOME_IMAGE_HEIGHT = 420
home_image = pygame.transform.scale(home_image, (HOME_WIDTH, HOME_IMAGE_HEIGHT))

#dogs
dog_image = pygame.image.load("chihuahua_right.png").convert_alpha()
dog_image = pygame.transform.scale(dog_image, (DOG_SIZE,DOG_SIZE))

dachshund_image = pygame.image.load("dachshund_right.png").convert_alpha()
dachshund_image = pygame.transform.scale(dachshund_image, (DOG_SIZE,DOG_SIZE))

retriever_image = pygame.image.load("retriever_right.png").convert_alpha()
retriever_image = pygame.transform.scale(retriever_image, (DOG_SIZE,DOG_SIZE))

dog_flee_image = pygame.image.load("chihuahua_left.png").convert_alpha()
dog_flee_image = pygame.transform.scale(dog_flee_image, (DOG_SIZE,DOG_SIZE))

dachshund_flee_image = pygame.image.load("dachshund_left.png").convert_alpha()
dachshund_flee_image = pygame.transform.scale(dachshund_flee_image, (DOG_SIZE+30,DOG_SIZE+30))

retriever_flee_image = pygame.image.load("retriever_left.png").convert_alpha()
retriever_flee_image = pygame.transform.scale(retriever_flee_image, (DOG_SIZE,DOG_SIZE))


cat_image = pygame.image.load("cat_image.png")
cat_image = pygame.transform.scale(cat_image, (CAT_SIZE, CAT_SIZE))

#colors RGB
GREEN = (70, 170, 70)
GRAY = (130, 130, 130)
BROWN =(140, 90, 40)
BLUE= (100, 100, 255)
DOG_BROWN = (150, 75, 0)

#space background
stars = []

for _ in range(180):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)

    radius = random.randint(1,3)
    brightness = random.randint(170,255)
    color = (brightness, brightness, brightness)

    stars.append([x,y, radius, color])


def draw_space_background():
    for y in range(HEIGHT):
        t = y /HEIGHT
        r= int(5* (1-t) +0 *t)
        g = int(5* (1-t) +10 *t)
        b = int(25* (1-t) +5 *t)

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    #stars
    for star in stars:
        pygame.draw.circle(screen, star[3], (star[0], star[1]), star[2])

# classes

class DogEnemy:
    def __init__(self, breed="chihuahua"):
        self.breed = breed
        self.x = -50
        self.y = ROAD_Y + ROAD_HEIGHT//2 - DOG_RADIUS
        if breed == "chihuahua":
            self.speed = 2.2
        elif breed == "dachshund":
            self.speed = 3.7
        elif breed == "retriever":
            self.speed = 4.7
        self.hp = 100
        self.radius = DOG_RADIUS
        self.fleeing = False

    def update(self):
        if self.fleeing:
            self.x -= self.speed*2
        else:
            self.x += self.speed

    def draw(self, surface):
        if self.breed == "chihuahua":
            if self.fleeing:
                surface.blit(dog_flee_image, (self.x, self.y))
            else:
                surface.blit(dog_image, (self.x, self.y))
        else:
            if self.breed == "dachshund":
                if self.fleeing:
                   surface.blit(dachshund_flee_image, (self.x, self.y))
                else:
                    surface.blit(dachshund_image, (self.x, self.y))
            elif self.breed == "retriever":
                if self.fleeing:
                   surface.blit(retriever_flee_image, (self.x, self.y))
                else:
                    surface.blit(retriever_image, (self.x, self.y))

        hp_text = font.render(str(self.hp), True, (255,255,255))
        surface.blit(hp_text, (self.x + DOG_RADIUS -10, self.y - 30))
        if self.fleeing:
            help_text = help_font.render("HELP !!!", True, (255, 0, 0))
            surface.blit(help_text, (self.x - 10, self.y - 50))
    

class CatTower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = CAT_RANGE
        self.show_range = FPS*2
        self.target = None
        self.cooldown= 0
    
    def update(self, enemies):
               
        if self.show_range > 0:
            self.show_range -= 1
        self.target = None

        if self.cooldown >0:
            self.cooldown -= 1
        for enemy in enemies:
            if enemy.fleeing:
                continue
            distance = math.hypot(enemy.x + DOG_RADIUS - self.x, enemy.y + DOG_RADIUS - self.y)
            if distance <= self.range:
                self.target = enemy
                if self.cooldown == 0:
                    projectiles.append(Projectile(self.x, self.y, self.target))
                    self.cooldown = 70
                break
    
    def draw(self, surface):
        #draw attack range
        if self.show_range >0:
            pygame.draw.circle(surface, (180,180,180), (self.x, self.y), self.range, 1)
        #draw tower
        surface.blit(cat_image, (self.x - CAT_RADIUS, self.y - CAT_RADIUS))




        

class Projectile:
   def __init__(self, x, y, target):
    self.x  = x
    self.y = y
    self.target = target
    self.speed= 6

   def update(self):
    if self.target is None:
        return
    dx = (self.target.x + DOG_RADIUS) -self.x
    dy = (self.target.y + DOG_RADIUS) -self.y

    distance = math.hypot(dx, dy)
    if distance <= self.target.radius:
        self.target.hp -= 25
        if self.target.hp < 0:
            self.target.hp = 0
        if self.target.hp == 0:
            self.target.fleeing = True


        return

    if distance > 0:
        self.x += dx / distance*self.speed
        self.y += dy / distance*self.speed
    
   def draw(self, surface):
    pygame.draw.circle(surface, (255,220,0), (int(self.x), int(self.y)), 6)


# game object lists

enemies = []
towers = []
projectiles = []


treats = 100
lives = 10
cat_count = 0
CAT_COST = 50

#click message
click_message = " "
click_message_pos = (0,0)
click_message_timer = 0

#level settings

MAX_ENEMIES = 15
spawned_enemies = 0
LEVEL_BONUS = 75
bonus_given = False

#timer enemy spawning

spawned_timer = 0

#level functions
def draw_home():
    screen.blit(home_image, (HOME_X, 0))

def draw_button(surface, rect, text, base_color):
    mouse_pos = pygame.mouse.get_pos()

    #hover effect
    if rect.collidepoint(mouse_pos):
        color=((min(base_color[0]+30,255)),
        min(base_color[1]+30, 255),
        min(base_color[2]+30, 255))
    else:
        color = base_color
    #shadow
    shadow_rect= rect.move(5,5)
    pygame.draw.rect(surface, (35,35,35), shadow_rect, border_radius=18)
    #button and shadows
    pygame.draw.rect(surface, color, rect, border_radius=18)
    pygame.draw.line(surface, (255,255,255), (rect.left +8, rect.top+5), (rect.right -8, rect.top +5), 2)
    pygame.draw.line(surface, (240,240,240), (rect.left +5, rect.top+8), (rect.left +5, rect.bottom -8), 2)
    pygame.draw.line(surface, (50,50,50), (rect.left +8, rect.bottom -4), (rect.right -8, rect.bottom-4), 2)
    pygame.draw.line(surface, (50,50,50), (rect.right -4, rect.top+8), (rect.right -4, rect.bottom-8), 2)
    #border
    pygame.draw.rect(surface, (20,20,20), rect, 2, border_radius= 18)
    #text
    text_surface= title_font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)



def start_level1():
    global current_level
    global MAX_ENEMIES, enemies, towers, projectiles
    global spawned_timer, spawned_enemies, bonus_given
    global lives, treats, cat_count, game_state

    enemies.clear()
    towers.clear()
    projectiles.clear()

    bonus_given = False
    spawned_timer = 0
    spawned_enemies = 0

    MAX_ENEMIES = 15
    lives = 7
    treats = 100
    cat_count = 0
    game_state = "level_1"
    current_level = 1
    bark_sound.play()

def start_level2():

    global current_level
    global MAX_ENEMIES,  enemies, towers, projectiles
    global spawned_timer, spawned_enemies, bonus_given
    global lives, treats, cat_count, game_state

    enemies.clear()
    towers.clear()
    projectiles.clear()

    bonus_given = False
    spawned_timer = 0
    spawned_enemies = 0

    MAX_ENEMIES = 25
    lives = 7
    cat_count = 0
    game_state = "level_2"
    current_level = 2
    bark_sound.play()

def start_level3():
    global current_level
    global MAX_ENEMIES,  enemies, towers, projectiles
    global spawned_timer, spawned_enemies, bonus_given
    global lives, cat_count, game_state

    enemies.clear()
    towers.clear()
    projectiles.clear()

    bonus_given = False
    spawned_timer = 0
    spawned_enemies = 0

    MAX_ENEMIES = 30
    lives = 7
    cat_count = 0
    game_state = "level_3"
    current_level = 3
    bark_sound.play()


#main loop
running = True
#game states:
#"start"
#"level1"
#"level_complete"
#"game_over"

game_state = "start"
current_level = 1

#start button
start_button = pygame.Rect(390, 420,220,70)
next_button = pygame.Rect(360, 380,240,70)
quit_button = pygame.Rect(360, 480,240,70)
restart_button = pygame.Rect(360,360,240,70)
buy_lives_button = pygame.Rect(360,460,240,70)
game_over_quit_button = pygame.Rect(360,560,240,70)

screen.blit(home_image, (HOME_X, 0))

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        #events(input)
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if game_state == "start":
                if start_button.collidepoint(event.pos):
                    start_level1()
                
            elif game_state in ("level_1","level_2", "level_3"):
                x, y = pygame.mouse.get_pos()
                #check click is on the road
                on_road= ROAD_Y <= y <= ROAD_Y + ROAD_HEIGHT
                #check if click is inside home area
                inside_home = x >= HOME_X
            #only allow towers elsewhere
                if not on_road and not inside_home:
                    if treats >= CAT_COST:
                        towers.append(CatTower(x, y))
                        meow_sound.play()
                        treats -= CAT_COST
                        cat_count += 1
                    else:
                        click_message= "Not enough (50) Treats!"
                        click_message_pos= (x,y)
                        click_message_timer= FPS

            elif game_state == "level_complete":
                if next_button.collidepoint(event.pos):
                    if current_level == 1:
                        start_level2()
                    elif current_level == 2:
                        start_level3()
                    elif current_level == 3:
                        game_state = "congratulations"
                elif quit_button.collidepoint(event.pos):
                    running = False

            elif game_state == "game_over":
                if restart_button.collidepoint(event.pos):
                    start_level1()
                elif buy_lives_button.collidepoint(event.pos):
                    if treats >= 200:
                        treats -= 200
                        lives += 3
                        game_state = f"level_{current_level}"
                        enemies.clear()
                        projectiles.clear()

                elif game_over_quit_button.collidepoint(event.pos):
                    running = False
            elif game_state == "congratulations":
                if quit_button.collidepoint(event.pos):
                    running = False
        if click_message_timer > 0:
            click_message_timer -= 1



    #ememies spawn over time
    if game_state in ("level_1","level_2", "level_3") :
        spawned_timer += 1

        
        if spawned_timer >= 120:
            if spawned_enemies < MAX_ENEMIES:
                if current_level == 1:
                    enemies.append(DogEnemy("chihuahua"))
                #level2
                elif current_level == 2:
                    if spawned_enemies < 3:
                        enemies.append(DogEnemy("chihuahua"))

                    elif spawned_enemies < 10:
                        if spawned_enemies % 2 == 0:
                            enemies.append(DogEnemy("dachshund"))
                        else:
                            enemies.append(DogEnemy("chihuahua"))
                    else:
                        enemies.append(DogEnemy("dachshund"))
                #level 3
                elif current_level == 3:
                    if spawned_enemies < 2:
                        enemies.append(DogEnemy("chihuahua"))
                    elif spawned_enemies < 10:
                        if spawned_enemies % 2 == 0:
                            enemies.append(DogEnemy("dachshund"))
                        else:
                            enemies.append(DogEnemy("chihuahua"))
                    elif spawned_enemies < 15:
                        if spawned_enemies % 2 == 0:
                            enemies.append(DogEnemy("retriever"))
                        else:
                            enemies.append(DogEnemy("dachshund"))
                    else:
                        enemies.append(DogEnemy("retriever"))
                        
                spawned_enemies += 1
            spawned_timer = 0

    
        for enemy in enemies[:]:
            enemy.update()

            if not enemy.fleeing and enemy.x >= HOME_X:
                enemies.remove(enemy)
                lives -= 1
            elif enemy.fleeing and enemy.x < -50:
                enemies.remove(enemy)
                treats += 10
        
        for tower in towers:
            tower.update(enemies)

        for projectile in projectiles[:]:

            old_x = projectile.x
            old_y = projectile.y
            projectile.update()

            # remove projectile if it target
            if projectile.x == old_x and projectile.y == old_y:
                projectiles.remove(projectile)
                continue
            #remove projectile if leaves screen
            if projectile.x > WIDTH:
                projectiles.remove(projectile)
        if (spawned_enemies == MAX_ENEMIES and len(enemies) == 0 and lives > 0):
            if not bonus_given:
                treats += LEVEL_BONUS
                bonus_given = True
            if current_level == 3:
                game_state = "congratulations"
            else:
                game_state = "level_complete"
            
        if lives <= 0:
            game_state = "game_over"
    #draw game


    if game_state == "start":
        draw_space_background()
        draw_home()
        
        title = title_extra_font.render("Kitty Defense!", True, (255,255,255))
        screen.blit(title, (360,120))
        welcome1= font.render("Protect the Cat Home from naughty dogs!", True, (255,255,255))
        welcome2= font.render("Place your cats near the street and you'll see!", True, (255,255,255))
        screen.blit(welcome1, (250,300))
        screen.blit(welcome2, (250,350))
        draw_button(screen, start_button, "START", (80,180,80))


    elif game_state in ("level_1", "level_2", "level_3"):
        screen.fill(GREEN)
        draw_home()
    #draw simple grass

        for x in range(0, WIDTH, 10):
            for y in range(0, HEIGHT, 10):
                #no grass on the road
                if ROAD_Y <= y <= ROAD_Y + ROAD_HEIGHT:
                    continue

                pygame.draw.line(screen,(50,140,50), (x, y), (x-2, y-5), 2 )
                pygame.draw.line(screen, (60,155,60), (x, y), (x+2, y -5), 2)
                pygame.draw.line(screen, (40,120,40), (x, y), (x, y -6), 2)

        pygame.draw.rect(screen, (105,105,105), (0, ROAD_Y, WIDTH, ROAD_HEIGHT)),

        STONE_W = 25
        STONE_H = 18

        for row in range(ROAD_HEIGHT//STONE_H +1):
            offset = 0
            if row % 2 == 1:
                offset = STONE_W // 2
            y = ROAD_Y + row* STONE_H

            for x in range(-offset, WIDTH, STONE_W):
                rect = pygame.Rect(x, y, STONE_W, STONE_H)

                pygame.draw.rect(screen, (169,169,169), rect)
                pygame.draw.rect(screen, (95,95,95), rect, 1)

        draw_home()
        level_text = title_font.render(f"LEVEL {current_level}", True, (255,255,255))
        screen.blit(level_text, (20,20))
        #draw home title
        title = title_font.render("CAT HOME", True, (255,255,255))
        screen.blit(title, (HOME_X+20, 20))


        #draw game stats on panel

        treats_text = font.render(f"Treats: {treats}", True, (0,0,0))
        lives_text = font.render(f"Lives: {lives}", True,  (0,0,0))
        cats_text = font.render(f"Cats: {cat_count}", True,  (0,0,0))

        panel_y = HOME_IMAGE_HEIGHT + 20
        panel_height = HEIGHT - HOME_IMAGE_HEIGHT
        #wooden background
        pygame.draw.rect(screen, (150,100,50), (HOME_X, panel_y, HOME_WIDTH, panel_height))

        #wooden border

        pygame.draw.rect(screen, (90,55,20), (HOME_X, panel_y, HOME_WIDTH, panel_height), 4)
        #horizontal wood lines
        for y in range(panel_y +15, HEIGHT, 18):
            pygame.draw.line(screen, (170,120,70), (HOME_X +5, y), (WIDTH-5, y), 2)

        screen.blit(treats_text, (HOME_X +20, panel_y+20))
        screen.blit(lives_text, (HOME_X +20, panel_y +60))
        screen.blit(cats_text, (HOME_X +20, panel_y + 100))
        
        for enemy in enemies:
            enemy.draw(screen)

        
        for tower in towers:
            tower.draw(screen)
        
        for projectile in projectiles:
            projectile.draw(screen)
        
        if click_message_timer > 0:
            text= font.render(click_message, True, (220,40,40))
            rect = text.get_rect(center= click_message_pos)
            screen.blit(text, rect)

    elif game_state == "level_complete": 
        draw_space_background()
        draw_home()

        title = title_extra_font.render(f"LEVEL {current_level} COMPLETE!", True, (255,255,255))
        screen.blit(title, (350, 120))

        bonus = font.render("Congrats !!! ", True, (255,255,255))
        screen.blit(bonus, (390,250))
        total = font.render(f"+++ {LEVEL_BONUS} Treats", True, (255,255,255))
        screen.blit(total, (390,300))
        nextlvl=str(int(current_level+1))
        draw_button(screen, next_button, nextlvl, (70,170,70))
        draw_button(screen, quit_button, "QUIT", (170,70,70))

    elif game_state == "game_over":
        draw_space_background()
        draw_home()
        title = title_extra_font.render("GAME OVER", True, (255,255,255))
        screen.blit(title, (430, 120))
        #restart button
        draw_button(screen, restart_button, "RESTART", (70,170,70))
        #buy lives button
        if treats >= 200:
            color = (70,170,70)
        else:
            color = (120,120,120)
        draw_button(screen, buy_lives_button, "3+ LIVES", color)
        if treats < 200:
            warning = small_font.render(f"Not enough Treats ({treats})", True, (220,30,30))
            screen.blit(warning, (400,505))
        #quit button
        draw_button(screen, game_over_quit_button, "QUIT", (170,70,70))
    

    elif game_state == "congratulations":#
        draw_space_background()
        draw_home()

        title = title_extra_font.render("CONGRATULATIONS", True, (40,40,40))
        screen.blit(title, (304, 104))
        title =  title_extra_font.render("CONGRATULATIONS", True, (255,215,0))
        screen.blit(title, (300, 100))
        pygame.draw.line(screen, (255,215,0), (260,180), (760,180), 3)
        text1= font.render("You have sucessfully defended the Cat Home!", True, (255,215,0))
        screen.blit(text1, (240,240))
        text2= font.render("The World is a saver place for cats thanks to you!", True, (255,215,0))
        screen.blit(text2, (355,290))

        thanks = font.render("Thank you for playing Kitty Defense!", True, (255,215,0))
        screen.blit(thanks, (360,370))

        draw_button(screen, quit_button, "QUIT", (170,70,70))
        
        

    pygame.display.flip()

pygame.quit() 
sys.exit()