import pygame
import sys
pygame.init()


colours = {
    "black":(0,0,0),
    "red":(255,0,0),
    "green":(0,255,0),
    "blue":(0,0,255),
    "yellow":(255,255,0), #Set a dict of colours
    "violet":(255,0,255),
    "cyan":(0,255,255),
    "white":(255,255,255)
}
pressed_keys = []

#Сreation of classes
class Button():
    def __init__(self, width, height, surface, x_button, y_button, text, color_text):
        self.width = width
        self.height = height
        self.surface = surface
        self.x_button = x_button
        self.y_button = y_button
        self.color = colours["violet"]
        self.text = text
        self.text_color = color_text
        self.hitbox = (self.x_button, self.y_button, self.width, self.height)
        self.clicked = False

    #Func for drawing the button
    def draw(self, screen):
        pygame.draw.rect(self.surface, colours["black"], self.hitbox)
        self.font = pygame.font.SysFont("serif", 20)
        self.final = self.font.render(self.text, True, self.text_color)
        screen.blit(self.final, (self.x_button+17, self.y_button+15))

    #Func for mouse click checks
    def mouse_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= self.x_button and mouse_pos[0] <= self.x_button + self.width and mouse_pos[1] >= self.y_button and mouse_pos[1] <= self.x_button + self.height:
            self.clicked = True
        return self.clicked

class Wall():
    def __init__(self, width, height, surface, x, y):
        self.width = width
        self.height = height
        self.surface = surface
        self.x = x
        self.y = y
        self.color = colours["cyan"]
        self.wall_hitbox = None

    #Func for drawing the wall
    def draw(self):
        self.wall = pygame.Surface((self.width, self.height))
        self.wall.fill(colours["red"])
        self.wall_hitbox = self.wall.get_rect(x=self.x, y=self.y)
        self.surface.blit(self.wall, self.wall_hitbox)

    #Func for returning hitbox of wall
    def return_hitbox(self):
        return self.wall_hitbox

class Trigger():
    def __init__(self, width, height, surface, x, y, wall_width, wall_height, wall_color, wall_x, wall_y):
        self.width = width
        self.height = height
        self.surface = surface
        self.x = x
        self.y = y
        self.color = colours["green"]
        self.wall_width = wall_width
        self.wall_height = wall_height
        self.wall_color = wall_color
        self.wall_x = wall_x
        self.wall_y = wall_y
        self.activate = False

    #Func for drawing platform of trigger
    def draw_plat(self):
        self.plat = pygame.Surface((self.width, self.height))
        self.plat.fill(self.color)
        self.plat_hitbox = (self.x, self.y, self.width, self.height)
        self.surface.blit(self.plat, self.plat_hitbox)

    #Func for drawing wall of trigger
    def draw_wall(self):
        self.wall = pygame.Surface((self.wall_width, self.wall_height))
        if self.activate:
            self.wall_color = colours["white"]
        self.wall.fill(self.wall_color)
        self.wall_hitbox = (self.wall_x, self.wall_y, self.wall_width, self.wall_height)
        self.surface.blit(self.wall, self.wall_hitbox)

    #Func for checks collision of wall with player
    def collision_with_player(self, player):
        if not self.activate:
            if player.get_hitbox().colliderect(self.wall_hitbox):
                if player.y < self.wall_hitbox[1]:
                    player.y = self.wall_hitbox[1] - player.height
                elif player.x < self.wall_hitbox[0]:
                    player.x = self.wall_hitbox[0] - player.width
                elif player.y + player.height > self.wall_hitbox[1] + self.wall_hitbox[3]:
                    player.y = self.wall_hitbox[1] + self.wall_hitbox[3]
                elif player.x + player.width > self.wall_hitbox[0] + self.wall_hitbox[2]:
                    player.x = self.wall_hitbox[0] + self.wall_hitbox[2]

    #Func for detection of push of platform by player
    def collision(self, player):
        if player.get_hitbox().colliderect(self.plat_hitbox):
            self.activate = True

class Win_platform():
    def __init__(self, width, height, surface, x, y):
        self.width = width
        self.height = height
        self.color = colours["yellow"]
        self.surface = surface
        self.x = x
        self.y = y

    def draw(self):
        self.platform = pygame.Surface((self.width, self.height))
        self.platform.fill(self.color)
        self.platform_hitbox = (self.x, self.y, self.width, self.height)
        self.surface.blit(self.platform, self.platform_hitbox)

    def win_collision(self, player):
        global win
        if player.get_hitbox().colliderect(self.platform_hitbox):
            win = True

class Player():
    def __init__(self, width, height, surface, style, start_x, start_y):
        self.width = width
        self.height = height
        self.surface = surface
        self.style = style
        self.start_x = start_x
        self.start_y = start_y
        self.x = self.start_x
        self.y = self.start_y
        self.speed = 0
        self.player = None
        self.player_hitbox = None
        self.img = None

    def draw(self):
        self.player = pygame.Surface((self.width, self.height))
        self.img = pygame.image.load(self.style).convert_alpha()
        self.img.set_colorkey((255, 255, 255))
        self.img_hitbox = self.img.get_rect(x=self.x, y=self.y)
        self.surface.blit(self.img, self.img_hitbox)
        self.player_hitbox = self.player.get_rect(x=self.x,y=self.y)
        #self.surface.blit(self.player, self.player_hitbox)

    def move(self, speed):
        global pressed_keys
        self.speed = speed
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self.y -= self.speed
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.x -= self.speed
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.y += self.speed
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.x += self.speed

    def collision_with_walls(self, list_of_walls):
        for element in list_of_walls:
            if self.img_hitbox.colliderect(element.return_hitbox()):
                self.x, self.y = self.start_x, self.start_y


    def collision_with_window(self, screen_size):
        if self.x < 0:
            self.x = 0
        elif self.x > screen_size[0] - self.player_hitbox.width:
            self.x = screen_size[0] - self.player_hitbox.width
        if self.y < 0:
            self.y = 0
        elif self.y > screen_size[1] - self.player_hitbox.height:
            self.y = screen_size[1] - self.player_hitbox.height

    def stop(self):
        self.speed = 0

    def get_hitbox(self):
        return self.player_hitbox

def stop_game():
    global activate, win
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            activate = False
            win = False
            pygame.quit()
            sys.exit()

def open_window(screen, surface, hitbox):
    global start, change
    font_first = pygame.font.SysFont("serif", 40)
    font_second = pygame.font.SysFont("serif", 25)
    screen.blit(surface, hitbox)
    pygame.draw.rect(start_menu, colours["yellow"], (0, 0, 400, 400), 15)
    pygame.draw.rect(screen, colours["yellow"], (75, 100, 240, 50))
    screen.blit(font_first.render("The RUN Out", True, colours["black"]), (80, 100))
    screen.blit(font_second.render("Press SPACE to start", True, colours["black"]), (90, 250))
    pygame.display.update()
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        start, change = False, True
def change_window(screen, surface, hitbox, button):
    global change, test
    screen.blit(surface, hitbox)
    button.draw(screen)
    pygame.display.update()
    if pygame.mouse.get_pressed()[0] and button.mouse_clicked():
        change, test = False, True

def pause_window(screen, surface, hitbox):
    global pause
    font_pause_1 = pygame.font.SysFont('serif', 40)
    font_pause_2 = pygame.font.SysFont('serif', 25)
    screen.blit(surface, hitbox)
    screen.blit(font_pause_1.render('PAUSE', True, colours["black"]), (140, 80))
    screen.blit(font_pause_2.render('Press SPACE for continue', True, colours["black"]), (70, 220))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_SPACE]:
            pause = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def level_window(screen, surface, hitbox, player, walls, trigger, win_plat):
    global pause
    screen.blit(surface, hitbox)
    for element in walls:
        element.draw()
    trigger.draw_plat()
    trigger.draw_wall()
    win_plat.draw()
    player.draw()
    pygame.display.update()
    player.move(5)
    win_plat.win_collision(player)
    trigger.collision(player)
    trigger.collision_with_player(player)
    player.collision_with_walls(list_of_walls)
    player.collision_with_window(screen_size)
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pause = True

def final_window(screen, surface, hitbox, font, list_of_text, color):
    screen.blit(surface, hitbox)
    y = 150
    for element in list_of_text:
        text = font.render(element, True, color)
        screen.blit(text, (70, y))
        y += 30
    pygame.draw.rect(surface, colours["black"], (55, 135, 295, 110), 3)
    pygame.display.update()

font = pygame.font.SysFont('serif', 20)
#Сцены
start = True
start_menu = pygame.Surface((400, 400)) #Входная менюшка
start_menu.fill(colours["red"])

change = False
test = False
change_level = pygame.Surface((400, 400)) #Выбор уровня
change_level.fill(colours["red"])

test_level = pygame.Surface((400, 400)) #Тестовый уровень
test_level.fill(colours["white"])

pause = False
pause_level = pygame.Surface((400, 400)) #Пауза в уровне
pause_level.fill(colours["white"])

final = pygame.Surface((400, 400))
final.fill(colours["yellow"])
list_of_text = ['Вы прошли тестовый уровень!', 'Нажмите на любую кнопку,', 'чтобы закрыть программу.']

activate = True
win = False
screen_size = (400, 400)
screen = pygame.display.set_mode(screen_size)
screen.blit(start_menu, start_menu.get_rect())
pygame.display.set_caption('The RUN Out')
icon = pygame.image.load('images/player.bmp').convert_alpha()
icon.set_colorkey(colours["white"])
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
fps = 30

list_of_walls = [
    wall1 := Wall(50, 337, test_level, 0, 0),
    wall2 := Wall(215, 1, test_level, 0, 0),
    wall3 := Wall(50, 360, test_level, 100, 40),
    wall4 := Wall(20, 110, test_level, 195, 0),
    wall5 := Wall(105, 205, test_level, 195, 150),
    wall6 := Wall(30, 100, test_level, 270, 50),
    wall7 := Wall(185, 50, test_level, 215, 0),
    wall8 := Wall(300, 1, test_level, 100, 399),
    wall9 := Wall(45, 50, test_level, 300, 305),
    wall10 := Wall(50, 50, test_level, 350, 220),
    wall11 := Wall(50, 75, test_level, 300, 110),
    wall12 := Wall(1, 400, test_level, 399, 0)
]

player = Player(33, 33, screen, 'images/player.bmp', 10, 357)
trigger = Trigger(45, 45, screen, 220, 55, 50, 100, colours["green"], 220, 355)
win_platform = Win_platform(45, 45, test_level, 305, 58.5)
button_on_testlevel = Button(200, 50, change_level, 100, 100, "Тестовый уровень", colours["white"])

while activate:

    if not win:
        stop_game()
        if start:
            open_window(screen, start_menu, start_menu.get_rect())
            continue

        if change:
            change_window(screen, change_level, change_level.get_rect(), button_on_testlevel)
            continue

        if pause:
            pause_window(screen, pause_level, pause_level.get_rect())
            continue

        if test:
            pressed_keys = pygame.key.get_pressed()
            level_window(screen, test_level, test_level.get_rect(), player, list_of_walls, trigger, win_platform)
        clock.tick(fps)
    else:
        final_window(screen, final, final.get_rect(), font, list_of_text, colours["black"])
        pygame.time.delay(100)
        stop_game()
        for key in pygame.key.get_pressed():
            if key:
                activate = False
                win = False
                pygame.quit()
                sys.exit()