import pygame
from math import sin, cos, radians, sqrt


RGB_BLUE = (0, 0, 225)
RGB_ORANGE = (225, 125, 0)
RGB_DARKGREY = (63, 63, 63)
RGB_LIGHTGREY = (155, 155, 155)
RGB_PED = (225, 31, 31)
RGB_LIGHTGREEN = (31, 225, 31)
RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)

screenWidth = 1200
screenHeight = 600
menuHeight = 100
radiusMissile = 30
widthWall = 50
pointsStart = screenWidth - 300
pointsWidth = 200
lockFps = 60
coefCllisionLossEnergy = 0.9

class Missile:
    def __init__(self, screen, type = 0, x = radiusMissile + 10, y = (screenHeight - menuHeight) / 2 + menuHeight, radius = radiusMissile):
        self.screen = screen
        self.type = type
        self.x = x
        self.y = y
        self.radius = radius
        self.insideR = radius * 0.6
        if type == 1:
            self.color = RGB_BLUE
        elif type == 2:
            self.color = RGB_ORANGE
        else:
            self.color = RGB_LIGHTGREY
        self.energy = 0
        self.ange = 0

    def setSpeedTange(self, energy, ange):
        self.energy = energy
        self.ange = ange

    def move(self):
        if self.energy:
            self.x += sqrt(2 * self.energy) * cos(radians(self.ange))
            self.y -= sqrt(2 * self.energy) * sin(radians(self.ange))
            self.energy -= 0.06
            if self.energy < 0:
                self.energy = 0
                self.ange = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, RGB_DARKGREY, (self.x, self.y), self.insideR)

def missilesMove():
    for missile in missiles:
        missile.move()

def missilesDraw():
    for missile in missiles:
        missile.draw()

def isMovement(): #T - move, F - calm
    for missile in missiles:
        if missile.energy:
            return True
    return False

def calcWallCollision():
    for missile in missiles:
        if missile.energy:
            if missile.ange > 0 and (missile.y < menuHeight + widthWall + radiusMissile): #Верхняя граница
                missile.ange *= -1
                missile.energy *= coefCllisionLossEnergy
            if missile.ange < 0 and (missile.y > screenHeight - widthWall - radiusMissile): #Нижняя граница
                missile.ange *= -1
                missile.energy *= coefCllisionLossEnergy
    pass

def calcMissileCollision():
    for missileI in missiles:
        if missileI.energy:

            for missileJ in missiles:
                if missileI == missileJ:
                    continue
                #TO DO collision missile

def sceneDraw():
    screen.fill(RGB_WHITE)

    pygame.draw.rect(screen, RGB_LIGHTGREY, (0, 0, screenWidth, menuHeight)) #Прямоугольник меню
    pygame.draw.rect(screen, RGB_DARKGREY, (0, menuHeight, screenWidth, widthWall)) #Верхняя граница
    pygame.draw.rect(screen, RGB_DARKGREY, (0, screenHeight - widthWall, screenWidth, widthWall))  #Нижняя граница
    pygame.draw.rect(screen, RGB_PED, (pointsStart, menuHeight + widthWall,
                                        pointsWidth, screenHeight - menuHeight - 2 * widthWall)) #Прямоугольник очков
    screen.blit(textPoint, (pointsStart + 25, menuHeight + widthWall + 80))

    missilesDraw()
    pass

def calcFps():
    countFps = clock.get_fps()
    textFps = font20.render(f"FPS: {int(countFps)}", True, RGB_LIGHTGREEN)
    screen.blit(textFps, (screenWidth - 120, 0))


#Инициализация
#Звпуск
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Карамболь")

font20 = pygame.font.Font("w3-ip.ttf", 20)
font155 = pygame.font.Font("w3-ip.ttf", 155)

textPoint = font155.render("+1", True, RGB_WHITE)

#ФПС
clock = pygame.time.Clock()
countFps = 0

#Круг
missiles = [
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2)
]
missiles[0].setSpeedTange(12.5, 5)
missiles[1].setSpeedTange(15, 0)
missiles[2].setSpeedTange(20, 35)
missiles[3].setSpeedTange(20, -35)
missiles[4].setSpeedTange(25, 25)

#Основной игровой цикл
running = True
while running:

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw & calc
    sceneDraw()
    missilesMove()
    calcWallCollision()
    calcMissileCollision()
    calcFps()

    #update
    pygame.display.flip()
    clock.tick(lockFps)  #Частота обновления экрана

pygame.quit()
