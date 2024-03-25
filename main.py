# UTF-8 Будет здесь!
import pygame
from math import sin, cos, sqrt, hypot, atan2
from math import pi, tau


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

        # physics
        self.energy = 0 # [0, 2 pi)
        self.rAnge = 0

        self.addEnergy = 0
        self.addRAnge = 0

        self.countCollision = 0
    pass

    def setEnergyRAnge(self, energy = 0.0, rAnge = 0.0):
        rAnge = rAnge % tau
        self.rAnge = rAnge
        self.energy = energy

    def move(self):
        if self.energy:
            cs = cos(self.rAnge)
            sn = sin(self.rAnge)
            self.x += sqrt(2 * self.energy) * cs
            self.y -= sqrt(2 * self.energy) * sn
            self.energy -= coefLossMoveEnergy
            if self.energy <= 0:
                self.energy = 0
                self.rAnge = 0
    pass

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

def isMovement(): # T - move, F - calm
    for missile in missiles:
        if missile.energy:
            return True
    return False

def calcWallCollision():
    for missile in missiles:
        if missile.energy:
            if missile.rAnge < pi and (missile.y < menuHeight + widthWall + radiusMissile): # top line
                missile.rAnge = (missile.rAnge * -1) % tau
                missile.energy *= coefLossCllisionEnergy
            if missile.rAnge > pi and (missile.y > screenHeight - widthWall - radiusMissile): # bottom line
                missile.rAnge = (missile.rAnge * -1) % tau
                missile.energy *= coefLossCllisionEnergy
pass

def calcMissileCollision():
    two_dimensional_array = [[0] * len(missiles) for _ in range(len(missiles))]

    for i, missileI in enumerate(missiles): # Просчёт было ли столкновение для каждого шара
        if missileI.energy == 0: continue
        for j, missileJ in enumerate(missiles): # Считаем столкновения с каждым
            if missileJ.energy == 0: continue
            if missileI == missileJ:
                continue

            distance = hypot((missileI.x - missileJ.x), (missileI.y - missileJ.y))
            if distance < 2 * radiusMissile:
                missileI.countCollision += 1

    # TODO collision missile
    for i, missileI in enumerate(missiles): # Просчёт распределения сил
        if missileI.energy == 0: continue
        for j, missileJ in enumerate(missiles):
            if missileJ.energy == 0: continue
            if missileI == missileJ:
                continue
            distance = hypot((missileI.x - missileJ.x), (missileI.y - missileJ.y))
            if distance < 2 * radiusMissile:
                pass
            pass

    for missileI in missiles:
        missileI.countCollision = 0
pass

# def calcMissileCollision():
#     for i, missileI in enumerate(missiles):
#         for j, missileJ in enumerate(missiles):
#             if i >= j:  # Избегаем повторной проверки и самопересечения
#                 continue
#             if missileI.energy == 0 or missileJ.energy == 0: # Просчёт коллизии только если есть энергия
#                 continue
#
#             # Расчет расстояния между камнями
#             distance = hypot(missileI.x - missileJ.x, missileI.y - missileJ.y)
#             if distance < 2 * radiusMissile:
#                 # Простейшая реакция на столкновение: обмен энергиями и углами
#                 missileI.energy, missileJ.energy = missileJ.energy * coefLossCllisionEnergy, missileI.energy * coefLossCllisionEnergy
#                 missileI.rAnge, missileJ.rAnge = missileJ.rAnge, missileI.rAnge
#
#                 # Отталкивание для предотвращения залипания
#                 overlay = (missileI.radius + missileJ.radius - distance) / 2
#                 energy = (overlay ** 2) / 2
#                 if missileI.energy < energy: missileI.energy = energy
#                 if missileJ.energy < energy: missileJ.energy = energy
#
#                 # if missileI.ange == missileJ.ange: missileJ.ange = -missileI.ange

def sceneDraw():
    screen.fill(RGB_WHITE)

    pygame.draw.rect(screen, RGB_LIGHTGREY, (0, 0, screenWidth, menuHeight)) # rect menu
    pygame.draw.rect(screen, RGB_DARKGREY, (0, menuHeight, screenWidth, widthWall)) #t op wall
    pygame.draw.rect(screen, RGB_DARKGREY, (0, screenHeight - widthWall, screenWidth, widthWall))  # bottom wall
    pygame.draw.rect(screen, RGB_PED, (pointsStart, menuHeight + widthWall,
                                        pointsWidth, screenHeight - menuHeight - 2 * widthWall)) # rect points
    screen.blit(textPoint, (pointsStart + 25, menuHeight + widthWall + 80)) # "+1"

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


# run & launch
# initialization
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Карамболь >\<")

font20 = pygame.font.Font("w3-ip.ttf", 20)
font155 = pygame.font.Font("w3-ip.ttf", 155)

textPoint = font155.render("+1", True, RGB_WHITE)

# fps
clock = pygame.time.Clock()
countFps = 0

# circle
missiles = [
Missile(screen, 1, 200, 200), Missile(screen, 2, 200, 400),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2)
]
missiles[0].setEnergyRAnge(12.5, -0.5)
missiles[1].setEnergyRAnge(15, 0.5)
# missiles[2].setEnergyRAnge(20, 0.6)
# missiles[3].setEnergyRAnge(20, -0.6)
# missiles[4].setEnergyRAnge(25, 0.6)
#
# missiles[5].setEnergyRAnge(5, 3.14 / 2 - 0.0)
# missiles[6].setEnergyRAnge(5, 3.14 / 2 - 0.1)
# missiles[7].setEnergyRAnge(5, 3.14 / 2 - 0.2)
# missiles[8].setEnergyRAnge(5, 3.14 / 2 - 0.3)
# missiles[9].setEnergyRAnge(5, 3.14 / 2 - 0.4)

# main cycle
running = True
while running:
    procEvents()

    # draw & calc
    sceneDraw()
    missilesMove()
    calcWallCollision()
    calcMissileCollision()
    calcFps()

    # update
    pygame.display.flip()
    clock.tick(lockFps)  # imput lag

pygame.quit()
