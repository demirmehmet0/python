"""Smooth Movement in pygame"""

#Imports
import pygame, sys

#Constants
WIDTH, HEIGHT = 400, 400
TITLE = "Smooth Movement"

#pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
def lerp(start, end, alpha):
        return start + alpha * (end - start)
#Player Class
class Player:
    def __init__(self, x, y, lerp_speed=0.1):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.targetX = self.x
        self.targetY = self.y
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4
        self.lerp_speed = lerp_speed
    
    

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def update(self):
        self.velX = 0
        self.velY = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
        if self.up_pressed and not self.down_pressed:
            self.velY = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.velY = self.speed
        
        self.targetX += self.velX
        self.targetY += self.velY
        
        self.x = lerp(self.x, self.targetX, self.lerp_speed)
        self.y = lerp(self.y, self.targetY, self.lerp_speed)


        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

#Player Initialization
player = Player(WIDTH/2, HEIGHT/2)

#Main Loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.left_pressed = True
            if event.key == pygame.K_RIGHT:
                player.right_pressed = True
            if event.key == pygame.K_UP:
                player.up_pressed = True
            if event.key == pygame.K_DOWN:
                player.down_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.left_pressed = False
            if event.key == pygame.K_RIGHT:
                player.right_pressed = False
            if event.key == pygame.K_UP:
                player.up_pressed = False
            if event.key == pygame.K_DOWN:
                player.down_pressed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if scroll wheel up
            if event.button == 4:
                player.lerp_speed += 0.01
            #if scroll wheel down
            if event.button == 5:
                player.lerp_speed -= 0.01
    #Draw
    win.fill((12, 24, 36))  
    player.draw(win)

    #update
    player.update()
    pygame.display.flip()

    #lerp_speed
    lerp_speed = player.lerp_speed
    #show lerp_speed
    pygame.display.set_caption(f"(LERP_SPEED: {lerp_speed})")


    clock.tick(120)