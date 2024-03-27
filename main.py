# UTF-8 Будет здесь!
import pygame
from math import sin, cos, sqrt, hypot, atan2, fabs
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


def sumVectors(ang_1, len_1, ang_2, len_2):
    x = len_1 * cos(ang_1) + len_2 * cos(ang_2)
    y = len_1 * sin(ang_1) + len_2 * sin(ang_2)
    return atan2(y, x) % tau, hypot(x, y)

def addAnge(for_1, for_2):
    return (for_1 + for_2) % tau

def subAnge(for_1, for_2):
    return (for_1 - for_2) % tau

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
        self.rAnge = 0
        self.energy = 0 # [0, 2 pi)

        self.addRAnge = 0
        self.addEnergy = 0

        self.countCollision = 0
    pass

    def setRAngeEnergy(self, rAnge = 0.0, energy = 0.0):
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
                #self.rAnge = 0
    pass

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, RGB_DARKGREY, (self.x, self.y), self.insideR)

    def recalcEnergy(self, missile):
        zeroRAnge = self.rAnge + atan2(self.y - missile.y, missile.x - self.x) % tau
        incidentRAnge = (zeroRAnge - self.rAnge) % tau
        energy = fabs(cos(incidentRAnge) / self.countCollision) * coefLossCllisionEnergy
        missile.addRAnge, missile.addEnergy = sumVectors(missile.addRAnge, missile.addEnergy, zeroRAnge, energy)

        energy = fabs(sin(incidentRAnge) / self.countCollision) * coefLossCllisionEnergy
        if incidentRAnge > pi: rotatRAnge = (zeroRAnge + pi / 2) % tau
        else: rotatRAnge = (zeroRAnge - pi / 2) % tau
        self.addRAnge, self.addEnergy = sumVectors(self.addRAnge, self.addEnergy, rotatRAnge, energy)
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
    #matrCollis = [[0] * len(missiles) for _ in range(len(missiles))]

    for i, missileI in enumerate(missiles): # Просчёт было ли столкновение для каждого шара
        if missileI.energy == 0: continue
        for j, missileJ in enumerate(missiles): # Считаем столкновения с каждым
            if missileI == missileJ: continue

            distance = hypot((missileI.x - missileJ.x), (missileI.y - missileJ.y))
            if distance < 2 * radiusMissile:
                missileI.countCollision += 1

    for i, missileI in enumerate(missiles): # Просчёт и распределения сил
        if missileI.energy == 0: continue
        for j, missileJ in enumerate(missiles):
            if missileI == missileJ: continue

            distance = hypot((missileI.x - missileJ.x), (missileI.y - missileJ.y))
            if distance < 2 * radiusMissile:
                missileI.recalcEnergy(missileJ)
        if missileI.countCollision:
            missileI.countCollision = 0
            missileI.energy = 0

    for missile in missiles:
        missile.rAnge, missile.energy = sumVectors(missile.rAnge, missile.energy, missile.addRAnge, missile.addEnergy)
        missile.addRAnge, missile.addEnergy = 0, 0

    pass

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
Missile(screen, 1, 200, 300), Missile(screen, 2, 500, 290),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2),
Missile(screen, 1), Missile(screen, 2)
]
# missiles[0].setRAngeEnergy(-0.5, 13.5)
# missiles[1].setRAngeEnergy(0.5, 14.5)

missiles[0].setRAngeEnergy(0.2, 100) # TODO плохое отталкивание даже при большой инергии

missiles[2].setRAngeEnergy(0.6, 20)
missiles[3].setRAngeEnergy(-0.6, 20)
missiles[4].setRAngeEnergy(0.6, 25)

missiles[5].setRAngeEnergy(3.14 / 2 - 0.0, 5)
missiles[6].setRAngeEnergy(3.14 / 2 - 0.1, 5)
missiles[7].setRAngeEnergy(3.14 / 2 - 0.2, 5)
missiles[8].setRAngeEnergy(3.14 / 2 - 0.3, 5)
missiles[9].setRAngeEnergy(3.14 / 2 - 0.4, 5)

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
