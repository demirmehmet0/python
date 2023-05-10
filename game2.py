import pygame
import matplotlib.pyplot as plt
import math
LERP_SPEED = 0.1
print(LERP_SPEED)
pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Game")

clock = pygame.time.Clock()

def lerp(start, end, alpha):
    return start + alpha * (end - start)
class TextInput:
    global LERP_SPEED
    def __init__(self, x, y, width, height, font, color=(0, 0, 0), max_length=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.color = color
        self.max_length = max_length
        self.text = ''
        self.surface = None
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.max_length is not None and len(self.text) >= self.max_length:
                    pass
                else:
                    self.text += event.unicode

    def update(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))

class Ball:
    global LERP_SPEED
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.time = 0
        self.positions = [(self.x, self.y)]

    def update(self, dt):
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.positions.append((self.x, self.y))
        self.vx = lerp(self.vx, self.ax, LERP_SPEED)
        self.vy = lerp(self.vy, self.ay, LERP_SPEED)
        self.x = lerp(self.x, self.x + self.vx * dt, LERP_SPEED)
        self.y = lerp(self.y, self.y + self.vy * dt, LERP_SPEED)

        self.positions.append((self.x, self.y))

        self.rect = pygame.Rect(int(self.x), int(self.y), 2 * self.radius, 2 * self.radius)

    def move_left(self):
        self.ax = -self.speed

    def move_right(self):
        self.ax = self.speed

    def move_up(self):
        self.ay = -self.speed

    def move_down(self):
        self.ay = self.speed

    def stop_x(self):
        self.ax = 0
        self.vx = 0

    def stop_y(self):
        self.ay = 0
        self.vy = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Graph:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('Arial', 20)
        self.data = []

    def add_data(self, point):
        self.data.append(point)

    def draw(self):
        if len(self.data) < 2:
            return

        x_data = [x for (x, y) in self.data]
        y_data = [y for (x, y) in self.data]
        x_min, x_max = min(x_data), max(x_data)
        y_min, y_max = min(y_data), max(y_data)
        x_range, y_range = x_max - x_min, y_max - y_min
        if x_range == 0:
            x_range = 1
        if y_range == 0:
            y_range = 1
        x_scale = self.width / x_range
        y_scale = self.height / y_range

        points = [(self.x + (x - x_min) * x_scale, self.y + self.height - (y - y_min) * y_scale) for (x, y) in self.data]

        if x_min < 0:
            points = points[-int(self.width / x_scale):]
        if x_max > self.width / x_scale:
            points = points[:int(self.width / x_scale)]
        if y_min < 0:
            points = [(x, y) for (x, y) in points if y >= self.y]
        if y_max > self.height / y_scale:
            points = [(x, y) for (x, y) in points if y <= self.y + self.height]

        pygame.draw.rect(screen, pygame.Color('white'), pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(self.x, self.y, self.width, self.height), 1)

        for i in range(len(points) - 1):
            pygame.draw.line(screen, pygame.Color('red'), points[i], points[i + 1], 2)

        x_label = self.font.render('Time', True, pygame.Color('black'))
        y_label = self.font.render('Speed', True, pygame.Color('black'))
        screen.blit(x_label, (self.x + self.width - x_label.get_width() - 5, self.y + self.height + 5))
        screen.blit(y_label, (self.x - y_label.get_width() - 5, self.y + 5))

def main():
    global LERP_SPEED
    ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 20, pygame.Color('blue'), 200)
    graph = Graph(100, 20, 500, 200)
    running = True
    font = pygame.font.SysFont('Arial', 20)
    
    while running:
        
        dt = clock.tick(FPS) / 1000.0
        lerp_speed_label = font.render(str(LERP_SPEED), True, pygame.Color('black'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ball.move_left()
                elif event.key == pygame.K_RIGHT:
                    ball.move_right()
                elif event.key == pygame.K_UP:
                    ball.move_up()
                elif event.key == pygame.K_DOWN:
                    ball.move_down()
                elif event.key == pygame.K_b:
                    print(LERP_SPEED)
                    #update the lerp speed
                    LERP_SPEED -= 0.001
                    LERP_SPEED = float("{:.3f}".format(LERP_SPEED))
                    print(LERP_SPEED)
                elif event.key == pygame.K_n:
                    LERP_SPEED += 0.001
                    LERP_SPEED = float("{:.3f}".format(LERP_SPEED))
                elif event.key == pygame.K_s:
                    plt.plot([x for (x, y) in graph.data], [y for (x, y) in graph.data])
                    plt.show()
                elif event.key == pygame.K_d:
                    graph.data = []
                    ball.time = 0
                elif event.key == pygame.K_r:
                    ball.x = SCREEN_WIDTH / 2
                    ball.y = SCREEN_HEIGHT / 2
                    ball.vx = 0
                    ball.vy = 0
                    ball.ax = 0
                    ball.ay = 0
                    ball.time = 0
                    graph.data = []
                    LERP_SPEED = 0.1
                #mouse wheel event
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #scroll up
                if event.button == 4:
                    LERP_SPEED -= 0.001
                    LERP_SPEED = float("{:.3f}".format(LERP_SPEED))
                #scroll down
                elif event.button == 5:
                    LERP_SPEED += 0.001
                    LERP_SPEED = float("{:.3f}".format(LERP_SPEED))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ball.stop_x()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ball.stop_y()

        ball.update(dt)
        graph.add_data((ball.time, math.sqrt(ball.vx ** 2 + ball.vy ** 2)))
        ball.time += dt

        screen.fill(pygame.Color('white'))
        ball.draw()
        graph.draw()
        screen.blit(lerp_speed_label, (0, 0))
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
