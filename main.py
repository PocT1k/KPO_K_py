import pygame
from math import sin, cos, radians, sqrt


RGB_BLUE = (0, 0, 225)
RGB_ORANGE = (225, 125, 0)
RGB_DARKGREY = (63, 63, 63)
RGB_LIGHTGREY = (155, 155, 155)
RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)

screenWidth = 1000
screenHeight = 600
menuHeight = 100

class Missile:
    def __init__(self, screen, type = 0, x = 50, y = (screenHeight - menuHeight) / 2 + menuHeight, radius=40):
        self.screen = screen
        self.type = type
        self.x = x
        self.y = y
        self.radius = radius
        self.insideR = radius * 0.6
        if type==1:
            self.color = RGB_BLUE
        elif type==2:
            self.color = RGB_ORANGE
        else:
            self.color = RGB_LIGHTGREY

    def setSpeedTange(self, energy, ange):
        self.energy = energy
        self.ange = ange

    def move(self):
        if (self.energy):
            self.x += sqrt(2 * self.energy) * cos(radians(self.ange))
            self.y += sqrt(2 * self.energy) * sin(radians(self.ange))
            self.energy -= 0.06
            if self.energy < 0:
                self.energy = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, RGB_DARKGREY, (self.x, self.y), self.insideR)


#Звпуск
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Карамболь")

#ФПС
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
fps = 0

#Круг
missile = Missile(screen, 2)
missile.setSpeedTange(12.5, 5)

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(RGB_WHITE)
    pygame.draw.rect(screen, RGB_LIGHTGREY, (0, 0, screenWidth, menuHeight))

    missile.move()
    missile.draw()

    # Подсчет FPS
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, RGB_BLACK)
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)  # Установка частоты обновления экрана

pygame.quit()
