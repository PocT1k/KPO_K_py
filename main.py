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
spawnX = 200
spawnY = (screenHeight - menuHeight) / 2 + menuHeight
lockFps = 60
countMoves = 8
coefLossCllisionEnergy = 0.97
coefLossMoveEnergy = 0.03


def addAnges(ang_1, ang_2):
    return (ang_1 + ang_2) % tau

def subAnges(ang_1, ang_2):
    return (ang_1 - ang_2) % tau

def sumVectors(ang_1, len_1, ang_2, len_2):
    x = len_1 * cos(ang_1) + len_2 * cos(ang_2)
    y = len_1 * sin(ang_1) + len_2 * sin(ang_2)
    return atan2(y, x) % tau, hypot(x, y)

def compAngles(ang_1, ang_2): # 1 - первый отложен от второго, 2 - второй отложен от первого
    ang_1 = ang_1 % tau
    ang_2 = ang_2 % tau
    diffAnge = ang_1 - ang_2

    if diffAnge > 0: return 1
    elif diffAnge < 0: return 2
    else: return 0

class Missile:
    def __init__(self, screen, type = 0, x = spawnX, y = spawnY, radius = radiusMissile):
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
        self.rAnge = rAnge % tau
        self.energy = energy

    def move(self):
        if self.energy:
            self.x += sqrt(2 * self.energy) * cos(self.rAnge)
            self.y -= sqrt(2 * self.energy) * sin(self.rAnge)
            self.energy -= coefLossMoveEnergy
            if self.energy <= 0:
                self.energy = 0
                #self.rAnge = 0
    pass

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, RGB_DARKGREY, (self.x, self.y), self.insideR)

    def recalcEnergy(self, missile):
        zeroRAnge = atan2(self.y - missile.y, missile.x - self.x) % tau
        rAnge = fabs((zeroRAnge - self.rAnge)) % (pi / 2)
        energy = cos(rAnge) / self.countCollision * self.energy * coefLossCllisionEnergy
        missile.addRAnge, missile.addEnergy = sumVectors(missile.addRAnge, missile.addEnergy, zeroRAnge, energy)

        energy = sin(rAnge) / self.countCollision * self.energy * coefLossCllisionEnergy

        newRAnge = -zeroRAnge
        match compAngles(zeroRAnge, self.rAnge):
            case 1: newRAnge = (zeroRAnge - pi / 2) % tau
            case 2: newRAnge = (zeroRAnge + pi / 2) % tau
        self.addRAnge, self.addEnergy = sumVectors(self.addRAnge, self.addEnergy, newRAnge, energy)
    pass
pass # Missile

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

    # Просчёт было ли столкновение для каждого шара
    for i, missileI in enumerate(missiles):
        if missileI.energy == 0: continue
        for j, missileJ in enumerate(missiles): # Считаем столкновения с каждым
            if missileI == missileJ: continue

            distance = hypot((missileI.x - missileJ.x), (missileI.y - missileJ.y))
            if distance < 2 * radiusMissile:
                missileI.countCollision += 1

    # Просчёт и распределения сил
    for i, missileI in enumerate(missiles):
        if missileI.energy == 0: continue
        for j, missileJ in enumerate(missiles):
            if missileI == missileJ: continue

            distance = hypot((missileI.x - missileJ.x), (missileI.y - missileJ.y))
            if distance < 2 * radiusMissile:
                missileI.recalcEnergy(missileJ)

        if missileI.countCollision:
            missileI.countCollision = 0
            missileI.energy = 0

    # Обнуление сил после просчёта
    for missile in missiles:
        missile.rAnge, missile.energy = sumVectors(missile.rAnge, missile.energy, missile.addRAnge, missile.addEnergy)
        missile.addRAnge, missile.addEnergy = 0, 0

    # # Отталкивание для предотвращения залипания
    # for i, missileI in enumerate(missiles):
    #     for j, missileJ in enumerate(missiles):
    #
    #         distance = hypot((missileI.x - missileJ.x), (missileI.y - missileJ.y))
    #         if distance < 2 * radiusMissile:
    #             overlay = (missileI.radius + missileJ.radius - distance) / 2
    #             energy = (overlay ** 2) / 2
    #             if missileI.energy + missileJ.energy < 2 * energy:
    #                 missileI.energy = energy
    #                 missileJ.energy = energy
    #             # if missileI.ange == missileJ.ange: missileJ.ange = -missileI.ange
    pass
pass # calcMissileCollision

def pointsDraw():
    screen.blit(textPlayer1, (10, 5))  # Игрок 1
    screen.blit(textPlayer2, (10, 55))  # Игрок 2

    len1 = (countMoves + 1) // 2
    for i in range(len1):
        pygame.draw.rect(screen, RGB_WHITE, (160 + 100 * i, 5, 80, 30))

    len2 = countMoves // 2
    for i in range(len2):
        pygame.draw.rect(screen, RGB_WHITE, (160 + 100 * i, 55, 80, 30))
pass

def sceneDraw():
    screen.fill(RGB_WHITE)

    pygame.draw.rect(screen, RGB_LIGHTGREY, (0, 0, screenWidth, menuHeight)) # rect menu
    pygame.draw.rect(screen, RGB_DARKGREY, (0, menuHeight, screenWidth, widthWall)) #t op wall
    pygame.draw.rect(screen, RGB_DARKGREY, (0, screenHeight - widthWall, screenWidth, widthWall))  # bottom wall
    pygame.draw.rect(screen, RGB_PED, (pointsStart, menuHeight + widthWall,
                                        pointsWidth, screenHeight - menuHeight - 2 * widthWall)) # rect points
    screen.blit(textPoint, (pointsStart + 25, menuHeight + widthWall + 80)) # "+1"

    pointsDraw() # Очки
pass

def calcFps():
    countFps = clock.get_fps()
    textFps = font20.render(f"FPS: {int(countFps)}", True, RGB_LIGHTGREEN)
    screen.blit(textFps, (screenWidth - 120, 0))

def procBasicEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False


def runMotions():
    missiles.clear()
    countMissiles = -1
    points1 = [None] * ((countMoves + 1) // 2)
    points2 = [None] * (countMoves // 2)

    for motion in range(countMoves):
        if running == False: continue
        missiles.append(Missile(screen, motion % 2 + 1))
        countMissiles += 1
        missiles[countMissiles].setRAngeEnergy(0, 4) # TODO Начальные условия

        while(isMovement() and running):
            # events
            procBasicEvents()
            # draw
            sceneDraw()
            missilesDraw()
            # physics
            missilesMove()
            calcWallCollision()
            calcMissileCollision()
            # update & fps
            calcFps()
            pygame.display.flip()
            clock.tick(lockFps)
        pass # while
        if running == False: continue
    pass # for
pass


# global initialization
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Карамболь >\<")

font20 = pygame.font.Font("w3-ip.ttf", 20)
font30 = pygame.font.Font("w3-ip.ttf", 30)
font155 = pygame.font.Font("w3-ip.ttf", 155)

textPoint = font155.render("+1", True, RGB_WHITE)
textPlayer1 = font30.render("Игрок 1", True, RGB_BLACK)
textPlayer2 = font30.render("Игрок 2", True, RGB_BLACK)

# fps
clock = pygame.time.Clock()
countFps = 0

# circle
missiles = []
# points
points1 = []
points2 = []


# run
running = True

def run():
    # main cycle
    # missiles.append(Missile(screen, 0 % 2 + 1))
    # missiles[0].setRAngeEnergy(0, 30)
    # missiles.append(Missile(screen, 1 % 2 + 1, 500, 300))
    # missiles[1].setRAngeEnergy(0, 0)

    while running:
        # draw & calc
        runMotions()

    pygame.quit()
pass

if __name__ == '__main__':
    run()
