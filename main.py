#UTF-8 Будет здесь!
import pygame
import math
from math import sin, cos, radians, sqrt, hypot, atan2


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
coefLossCllisionEnergy = 0.97
coefLossMoveEnergy = 0.03

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
        #physics
        self.energy = 0
        self.ange = 0

        self.addEnergy = 0
        self.addAnge = 0

        self.countCollision = 0
        pass

    def setEnergyTange(self, energy = 0.0, ange = 0.0):
        self.energy = energy
        self.ange = ange

    def move(self):
        if self.energy:
            self.x += sqrt(2 * self.energy) * cos(radians(self.ange))
            self.y -= sqrt(2 * self.energy) * sin(radians(self.ange))
            self.energy -= coefLossMoveEnergy
            if self.energy <= 0:
                self.energy = 0
                self.ange = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, RGB_DARKGREY, (self.x, self.y), self.insideR)
    pass

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
            if missile.ange > 0 and (missile.y < menuHeight + widthWall + radiusMissile): #top line
                missile.ange *= -1
                missile.energy *= coefLossCllisionEnergy
            if missile.ange < 0 and (missile.y > screenHeight - widthWall - radiusMissile): #bottom line
                missile.ange *= -1
                missile.energy *= coefLossCllisionEnergy
    pass

# def calcMissileCollision(): #TO DO переписать или дописать функцию просчёта коллизии
#     for missileI in missiles: #Просчёт столкновения для каждого шара
#         if missileI.energy == 0:
#             continue
#         for missileJ in missiles: #Считаем столкновения
#             if missileI == missileJ:
#                 continue
#             distance = hypot((missileI.x - missileJ.x), (missileI.y - missileJ.y))
#             if distance < 2 * radiusMissile:
#                 missileI.countCollision += 1
#
#     for missileI in missiles:
#         pass
#
#     #TO DO collision missile
#
#     for missileI in missiles:
#         missileI.countCollision = 0
#     pass

def calcMissileCollision():
    for i, missileI in enumerate(missiles):
        for j, missileJ in enumerate(missiles):
            if i >= j:  #Избегаем повторной проверки и самопересечения
                continue
            #Расчет расстояния между камнями
            distance = hypot(missileI.x - missileJ.x, missileI.y - missileJ.y)
            if distance < 2 * radiusMissile:
                #Простейшая реакция на столкновение: обмен энергиями и углами
                missileI.energy, missileJ.energy = missileJ.energy * coefLossCllisionEnergy, missileI.energy * coefLossCllisionEnergy
                missileI.ange, missileJ.ange = missileJ.ange, missileI.ange

                #Отталкивание для предотвращения залипания
                overlay = (missileI.radius + missileJ.radius - distance) / 2
                # energy = (overlay * lockFps / 2) ** 2 / 2
                # if missileI.energy < energy: missileI.energy = energy
                # if missileJ.energy < energy: missileJ.energy = energy
                #
                # if missileI.ange == missileJ.ange: missileJ.ange = -missileI.ange

                direction = atan2(missileI.y - missileJ.y, missileI.x - missileJ.x)
                missileI.x += cos(direction) * overlay
                missileI.y += sin(direction) * overlay
                missileJ.x -= cos(direction) * overlay
                missileJ.y -= sin(direction) * overlay

def sceneDraw():
    screen.fill(RGB_WHITE)

    pygame.draw.rect(screen, RGB_LIGHTGREY, (0, 0, screenWidth, menuHeight)) #rect menu
    pygame.draw.rect(screen, RGB_DARKGREY, (0, menuHeight, screenWidth, widthWall)) #top wall
    pygame.draw.rect(screen, RGB_DARKGREY, (0, screenHeight - widthWall, screenWidth, widthWall))  #bottom wall
    pygame.draw.rect(screen, RGB_PED, (pointsStart, menuHeight + widthWall,
                                        pointsWidth, screenHeight - menuHeight - 2 * widthWall)) #rect points
    screen.blit(textPoint, (pointsStart + 25, menuHeight + widthWall + 80)) #"+1"

    missilesDraw()
    pass

def calcFps():
    countFps = clock.get_fps()
    textFps = font20.render(f"FPS: {int(countFps)}", True, RGB_LIGHTGREEN)
    screen.blit(textFps, (screenWidth - 120, 0))

def procEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False


#run & launch
#initialization
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Карамболь >\<")

font20 = pygame.font.Font("w3-ip.ttf", 20)
font155 = pygame.font.Font("w3-ip.ttf", 155)

textPoint = font155.render("+1", True, RGB_WHITE)

#fps
clock = pygame.time.Clock()
countFps = 0

#circle
missiles = [
Missile(screen, 1, 100, 200), Missile(screen, 2, 100, 400),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2)
]
missiles[0].setEnergyTange(12.5, -20)
missiles[1].setEnergyTange(15, 25)
missiles[2].setEnergyTange(20, 35)
missiles[3].setEnergyTange(20, -35)
missiles[4].setEnergyTange(25, 25)

missiles[5].setEnergyTange(5, 90)
missiles[6].setEnergyTange(5, 80)
missiles[7].setEnergyTange(5, 70)
missiles[8].setEnergyTange(5, 60)
missiles[9].setEnergyTange(5, 50)

#main cycle
running = True
while running:
    procEvents()

    #draw & calc
    sceneDraw()
    missilesMove()
    calcWallCollision()
    calcMissileCollision()
    calcFps()

    #update
    pygame.display.flip()
    clock.tick(lockFps)  #imput lag

pygame.quit()
