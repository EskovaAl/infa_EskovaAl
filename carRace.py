import pygame
import random
import sys

pygame.init()
clock = pygame.time.Clock()
musicBack = pygame.mixer.music.load("sounds/backMus.mp3")
crush = pygame.mixer.Sound("sounds/crush.mp3")

width = 1052
height = 836
road_height = 260
up_line = int(height*0.66)
down_line = int(height*0.83)
screen =  pygame.display.set_mode((width, height))
pygame.display.set_caption("The Best car racing")
font_style = pygame.font.SysFont(None, 30)
objects = []

def text(text, font):
    texts = font.render(text, True, (255, 255, 255))
    return texts, texts.get_rect()

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        font = pygame.font.SysFont('Arial', 40)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#82cf4d',
            'hover': '#da87d5',
            'pressed': '#982b97',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

    def startFunc():
        gameLoop()
    def quitFunc():
        sys.exit()


def start_menu():
    game_close = False
    menuBG = pygame.image.load("img/menu2.jpg")
    menuBG = pygame.transform.scale(menuBG, (width, height))
    screen.blit(menuBG, (0, 0))
    pygame.display.flip()
    while game_close == False:
        for object in objects:
            object.process()
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_close = True
                    sys.exit()
                if event.key == pygame.K_c:
                    gameLoop()

def score_window(score):
    s_font = pygame.font.SysFont(None, 35)
    score = s_font.render("СЧЕТ:" + str(score), True, (0, 0, 0))
    screen.blit(score, (900, 40))

def auto_models():
    temp = random.randint(0, 3)
    if temp==0:
        non_player_car = pygame.image.load("img/car_non_player2.png")
        return non_player_car
    if temp==1:
        non_player_car = pygame.image.load("img/car_non_player3.png")
        return non_player_car
    if temp==2:
        non_player_car = pygame.image.load("img/car_non_player4.png")
        return non_player_car
    if temp==3:
        non_player_car = pygame.image.load("img/car_non_player1.png")
        return non_player_car

def gameLoop():
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1, 0.0)
    background = pygame.image.load("img/road.jpg")
    gameoverBK = pygame.image.load("img/game_over.jpg")
    background = pygame.transform.scale(background, (width, height))

    #Начальные координаты расположения 2 машин
    player_car = pygame.image.load("img/car_player1.png")
    player_car_loc = player_car.get_rect()
    player_car_loc.center = width/6, down_line

    non_player_car = auto_models()
    non_player_car_loc = non_player_car.get_rect()
    non_player_car_loc.center = 1000, up_line

    score = 0
    speed = 1
    counter = 0

    gameOver = False
    gameClose = False
    while not gameOver:
        #Счетчик времени
        counter += 1
        non_player_car_loc[0] -= speed
        if non_player_car_loc[0] < -300:
            non_player_car_loc[0] = 1500
            #Есть машина прошла за пределы эрана, то счет +1
            score += 1
            if random.randint(0, 101) %2 == 0:
                non_player_car = auto_models()
                non_player_car_loc.center = 1400, up_line
            if random.randint(0, 101) %2 == 1:
                non_player_car = auto_models()
                non_player_car_loc.center = 1400, down_line
                #повышаем уровень по прошествию времени
        if counter == 1000:
                speed += 1
                counter = 0
                                    
        if player_car_loc.colliderect(non_player_car_loc):
            crush.play()
            pygame.mixer.music.set_volume(0.2)
            gameClose = True

        while gameClose == True:
            gameoverBK = pygame.transform.scale(gameoverBK, (width, height))
            screen.blit(gameoverBK, (0, 0))
            score_window(score)
            for object in objects:
                object.process()
                pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameClose = False
                        gameOver = True
                        quit()
                    if event.key == pygame.K_c:
                        gameClose = False
                        gameLoop()
            pygame.display.flip()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    if player_car_loc[1] == 651:
                        player_car_loc = player_car_loc.move([0, -int(road_height/2)])
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    if player_car_loc[1] == 521:
                        player_car_loc = player_car_loc.move([0, int(road_height/2)])

        screen.blit(background, (0, 0))
        screen.blit(player_car, player_car_loc)
        screen.blit(non_player_car, non_player_car_loc)
        score_window(score)
        pygame.display.flip()
        clock.tick(150)
    pygame.quit()
    sys.exit()

Button(408, 225, 242, 80, 'Старт', Button.startFunc, True)
Button(408, 433, 242, 80, 'Выход', Button.quitFunc, True)

start_menu()
sys.exit()
