#Imports
import pygame, sys

#Constants
WIDTH, HEIGHT = 400, 400
TITLE = "Bouncing Ball"

#pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
alpha = 0.1
def lerp(start, end):
    global alpha
    return start + alpha * (end - start)

#Ball Class
class Ball:
   
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (255, 255, 255)
        self.velX = 0
        self.velY = 0
        self.acceleration = 0.5
        self.friction = 0.95
        self.gravity = 0.5
        self.bounce = 0.8
        self.max_speed = 15
        self.jump_power = 10
        self.is_jumping = False

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def update(self):
        #Apply acceleration and friction
        self.velX *= self.friction
        self.velY += self.gravity
        self.velY = min(self.velY, self.max_speed)
        self.velX = min(max(self.velX, -self.max_speed), self.max_speed)
        self.velY = min(max(self.velY, -self.max_speed), self.max_speed)

        #Update position
        targetX = self.x + self.velX
        targetY = self.y + self.velY
        self.x = lerp(self.x, targetX)
        self.y = lerp(self.y, targetY)

        #Check for collision with walls
        if self.x < self.radius:
            self.velX = abs(self.velX)
        elif self.x > WIDTH - self.radius:
            self.velX = -abs(self.velX)
        if self.y > HEIGHT - self.radius:
            self.velY = -self.velY * self.bounce
            self.y = HEIGHT - self.radius
            self.is_jumping = False

        #Jump
        if not self.is_jumping and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.is_jumping = True
            self.velY = -self.jump_power
        global alpha
        #Move left/right
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.velX -= self.acceleration
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.velX += self.acceleration
        

    def apply_force(self, force):
        self.velY -= force

#Ball Initialization
ball = Ball(WIDTH/2, HEIGHT/2)

#Main Loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                alpha += 0.01
            if event.key == pygame.K_DOWN:
                alpha -= 0.01

        pygame.display.set_caption(str(alpha))
    #Draw
    win.fill((12, 24, 36))
    ball.draw(win)

    #Update
    ball.update()

    pygame.display.flip()
    clock.tick(60)
