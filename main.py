import pygame
from math import sin, cos


RGB_BLUE = (0, 0, 255)
RGB_ORANGE = (255, 165, 0)
RGB_DARKGREY = (63, 63, 63)
RGB_LIGHTGREY = (155, 155, 155)

screenWidth = 1000
screenHeight = 600
menuHeight = 100

class Circle:
    def __init__(self, screen, color=RGB_LIGHTGREY, x=50, y=(screenHeight-menuHeight)/2, radius=40):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.inside = radius * 0.6
        self.moving = False

    def setSpeedTange(self, speed, ange):
        self.speed = speed
        self.ange = ange
        self.moving = True

    def move(self):
        if (self.moving):
            self.x += self.speed * cos(self.ange)
            self.y += self.speed * sin(self.ange)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(self.screen, RGB_DARKGREY, (self.x, self.y), self.radius)


#Звпуск
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Карамболь")

# Параметры круга
circle_radius = 50
circle_x = screenWidth // 2
circle_y = screenHeight // 2
speed = 5

# Переменные для подсчета FPS
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
fps = 0

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, RGB_LIGHTGREY, (0, 0, screenWidth, menuHeight))

    # Движение круга
    circle_x += speed
    if circle_x > screenWidth:
        circle_x = -circle_radius

    # Отрисовка круга
    pygame.draw.circle(screen, RGB_BLUE, (circle_x, circle_y), circle_radius)

    # Подсчет FPS
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)  # Установка частоты обновления экрана

pygame.quit()
