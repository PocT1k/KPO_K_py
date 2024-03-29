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
pointsRect = pygame.Rect(pointsStart, menuHeight + widthWall, 200, screenHeight - menuHeight - 2 * widthWall)
start = [200, (screenHeight - menuHeight) / 2 + menuHeight]
lockFps = 60
countMoves = 8
coefLossCllisionEnergy = 0.97
coefLossMoveEnergy = 0.07
restartRect = pygame.Rect(screenWidth - 110, 30, 70, 50)


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
    def __init__(self, screen, type = 0, x = start[0], y = start[1], radius = radiusMissile):
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
    max = 0.0
    for missile in missiles:
        if not ((missile.x < 0 - radiusMissile - 100) or (missile.x > screenWidth + radiusMissile + 100)):
            if missile.energy > max:
                    max =  missile.energy
    return max

def getParameters():
    global running
    idDefine = True
    end = (start[0] - 100, start[1])
    while (idDefine and running):
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return
            elif event.type == pygame.MOUSEMOTION:  # Движение мышкой
                end = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие ЛКМ
                idDefine = False
        if running == False: break

        # draw
        sceneDraw()
        missilesDraw()
        pygame.draw.line(screen, RGB_BLACK, start, end, 5)

        # update & fps
        calcFps()
        pygame.display.flip()
        clock.tick(lockFps)
    ange = atan2(end[1] - start[1], start[0] - end[0]) % tau
    energy = hypot(start[0] - end[0], start[1] - end[1]) / 10
    if energy > 20: energy = 20
    return ange, energy


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
    global points1, points2

    # Прямоугльники
    screen.blit(textPlayer1, (10, 5))  # Игрок 1
    screen.blit(textPlayer2, (10, 55))  # Игрок 2
    pygame.draw.rect(screen, RGB_WHITE, (160 + 100, 5, 80, 30))
    pygame.draw.rect(screen, RGB_WHITE, (160 + 100, 55, 80, 30))

    # Очки
    textPoints1 = font30.render(str(points1), True, RGB_BLACK)
    textPoints2 = font30.render(str(points2), True, RGB_BLACK)
    screen.blit(textPoints1, (160 + 110, 2))  # очки 1
    screen.blit(textPoints2, (160 + 110, 52))  # очки 2
pass

def sceneDraw():
    screen.fill(RGB_WHITE)

    pygame.draw.rect(screen, RGB_LIGHTGREY, (0, 0, screenWidth, menuHeight)) # rect menu
    pygame.draw.rect(screen, RGB_DARKGREY, (0, menuHeight, screenWidth, widthWall)) #t op wall
    pygame.draw.rect(screen, RGB_DARKGREY, (0, screenHeight - widthWall, screenWidth, widthWall))  # bottom wall
    pygame.draw.rect(screen, RGB_PED, pointsRect) # rect points
    screen.blit(textPoint, (pointsStart + 25, menuHeight + widthWall + 80)) # "+1"
    pygame.draw.rect(screen, RGB_WHITE, (restartRect[0], restartRect[1], restartRect[2], restartRect[3])) # bottom restart
    screen.blit(textRestart, (restartRect[0] + 6, restartRect[1] + 2))  # "r"

    pointsDraw() # Очки
pass

def calcFps():
    global step
    # fps
    countFps = clock.get_fps()
    textFps = font20.render(f"FPS: {int(countFps)}", True, RGB_LIGHTGREEN)
    screen.blit(textFps, (screenWidth - 120, 0))

    # energy
    textE = font12.render(str(isMovement()), True, RGB_LIGHTGREEN)
    screen.blit(textE, (screenWidth - 140, 83))

    # step
    textStep = font70.render(str(step + 1), True, RGB_BLACK)
    screen.blit(textStep, (screenWidth - 200, 7))

def procBasicEvents():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                return


def runMotions():
    global running, points1, points2, step
    points1, points2 = 0, 0
    missiles.clear()
    countMissiles = -1
    pygame.display.flip()

    for motion in range(countMoves):
        step = motion
        if running == False: continue
        missiles.append(Missile(screen, motion % 2 + 1))
        countMissiles += 1
        rAnge, energy = getParameters()
        if running == False: continue
        missiles[countMissiles].setRAngeEnergy(rAnge, energy)

        while(isMovement() and running):
            # events
            procBasicEvents()
            if running == False: break

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

        # Подсчёт очков
        cont1 = 0
        cont2 = 0
        for missile in missiles: # Перебор
            if missile.type == 1:
                if pointsRect.collidepoint(missile.x, missile.y):
                    cont1 += 1
            if missile.type == 2:
                if pointsRect.collidepoint(missile.x, missile.y):
                    cont2 += 1
        # Новые значения
        points1 = cont1
        points2 = cont2

        sceneDraw()
        missilesDraw()
        pygame.display.flip()
    pass # for
pass


# global initialization
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Карамболь >\<")

font12 = pygame.font.Font("w3-ip.ttf", 12)
font20 = pygame.font.Font("w3-ip.ttf", 20)
font30 = pygame.font.Font("w3-ip.ttf", 30)
font70 = pygame.font.Font("w3-ip.ttf", 70)
font155 = pygame.font.Font("w3-ip.ttf", 155)

textPoint = font155.render("+1", True, RGB_WHITE)
textRestart = font30.render("res", True, RGB_BLACK)
textPlayer1 = font30.render("Игрок 1", True, RGB_BLACK)
textPlayer2 = font30.render("Игрок 2", True, RGB_BLACK)

# fps
clock = pygame.time.Clock()
countFps = 0

# circle
missiles = []
points1, points2 = 0, 0
step = -1
running = True

def run():
    global running
    while running:
        # draw & calc
        runMotions()

        isWait = True
        while (isWait):
            if running == False: break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        return
                    if event.key == pygame.K_r:
                        isWait = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restartRect.collidepoint(event.pos):
                        isWait = False
            pass # for
        pass # while stop
    pass  # while main
    pygame.quit()
pass

if __name__ == '__main__':
    run()

# pyinstaller --onefile --add-data "C:\\Users\\novik\\PycharmProjects\\KPO_K_py\\w3-ip.ttf;." main.py -w
