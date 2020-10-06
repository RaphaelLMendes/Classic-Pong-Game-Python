import pygame
import os
import random as r

pygame.init()

#Defining clock
clock = pygame.time.Clock()

#defining window size
winX = 800
winY = 500

#creating window surface
win = pygame.display.set_mode((winX, winY))
pygame.display.set_caption('Ping Pong')

#creating Score variables
score_player1 = 0
score_player2 = 0



#------------------------------------------------------------

class boundary:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self,win):
        pygame.draw.rect(win,(0,0,0),(self.x, self.y, self.width, self.height))

class projectile:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rad = 10
        self.color1 = (23,170,170)      #inside color
        self.color2 = (0,0,0)           #outside color
        self.xMax = winX
        self.yMax = winY
        self.acel = 1
        self.hitbox = (self.x-self.rad,self.y-self.rad,self.rad*2,self.rad*2)

        #setting limits (x1,x2,y1,y2)
        self.limits = (self.x-self.rad,self.x+self.rad,self.y-self.rad,self.y+self.rad)

        #setting random angle of start
        ix = r.randint(0,2)
        if ix == 0:
            self.Vx = 1
        else:
            self.Vx = -1

        iy = r.randint(0, 2)
        if iy == 0:
            self.Vy = 1
        else:
            self.Vy = -1

    def draw(self,win):
        self.move()
        pygame.draw.circle(win,self.color1,(self.x, self.y),self.rad)
        pygame.draw.circle(win, self.color2, (self.x, self.y), self.rad,2)

        self.hitbox = (self.x - self.rad, self.y - self.rad, self.rad * 2, self.rad * 2)
        # pygame.draw.rect(win,(255,0,0), self.hitbox,1)

    def move(self):
        if self.x >= winX-15-10-self.rad:
            self.Vx = -1
        elif self.x <= 0 + 15 + 10 + self.rad:
            self.Vx = +1

        if self.y >= winY-15-10-self.rad:
            self.Vy = -1
        elif self.y <= 0 + 15 + 10 + self.rad:
            self.Vy = 1

        self.x = int(self.x + self.Vx*self.acel)
        self.y = int(self.y + self.Vy*self.acel)
        self.acel +=0.01

    def goal(self,goal):
        goalLimits = (goal.x, goal.x + goal.width, goal.y, goal.y + goal.height)
        self.limits = (self.x - self.rad, self.x + self.rad, self.y - self.rad, self.y + self.rad)

        # limits (x1,x2,y1,y2)

        if self.limits[1] > goalLimits[0] and self.limits[0] < goalLimits[1]:
            if self.limits[3] > goalLimits[2] and self.limits[2] < goalLimits[3]:
                ran = [1,-1]
                if self.x > winX / 2:
                    print('Player 1 GOAL')
                    self.x = winX/2
                    self.y = winY/2
                    self.acel = 1
                    global score_player1
                    score_player1 += 1
                    print(score_player1)
                else:
                    print('Player 2 GOAL')
                    self.x = winX / 2
                    self.y = winY / 2
                    self.acel = 1
                    global score_player2
                    score_player2 += 1
                    print(score_player2)

                self.Vx = ran[r.randint(0, 1)]
                self.Vy = ran[r.randint(0, 1)]

    def hitPaddle(self, paddle):
        paddleLimits = (paddle.x, paddle.x+paddle.width,paddle.y, paddle.y+paddle.height)
        self.limits = (self.x - self.rad, self.x + self.rad, self.y - self.rad, self.y + self.rad)
        # limits (x1,x2,y1,y2)

        if self.limits[1] > paddleLimits[0] and self.limits[0] < paddleLimits[1]:
            if self.limits[3] > paddleLimits[2] and self.limits[2] < paddleLimits[3]:
                if self.x > winX/2:
                    self.Vx = -1
                else:
                    self.Vx = 1

class paddle:

    def __init__(self, x, y, color, upButton, downButton):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 100
        self.upButton = upButton
        self.downButton = downButton
        self.vel = 5
        self.color = color
        self.outline = (0,0,0)

    def draw(self,win):
        self.move()
        pygame.draw.rect(win,self.color,(self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, self.outline, (self.x, self.y, self.width, self.height),2)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self.upButton] and self.y > 0+15+10+self.vel:
            self.y -= self.vel
        if keys[self.downButton] and self.y+self.height < winY - 15 - 10 - self.vel:
            self.y += self.vel

class goalPost:

    def __init__(self, x):
        self.x = x
        self.width = 11
        self.height = 200
        self.y = (winY/2) - self.height / 2
        self.color = (255,255,255)

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x, int(self.y), self.width, self.height))


#------------------------------------------------------------

def draw(win):
    '''Draw funcion'''

    #Setting backround white
    win.fill((255,255,255))

    #drawing Boundries
    for boundary in boundaryList:
        boundary.draw(win)

    #draw players and goal location
    player1.draw(win)
    player2.draw(win)
    goal1.draw(win)
    goal2.draw(win)

    #drawing Score board
    font = pygame.font.SysFont('comicsans', 50, 1)
    score1 = font.render(str(score_player1),1,(0,0,0))
    score2 = font.render(str(score_player2), 1, (0, 0, 0))

    win.blit(score1,(15+10+20,15+10+20))
    win.blit(score2, (winX - 15 - 10 - 20 - score2.get_width(), 15 + 10 + 20))

    #Projectile draw and check for colision
    ball.draw(win)
    ball.hitPaddle(player1)
    ball.hitPaddle(player2)
    ball.goal(goal1)
    ball.goal(goal2)

    # Updates display
    pygame.display.update()

def mainLoop():
    '''Main loop Function'''

    run = True
    while run:

        #Defining FPS
        clock.tick(30)

        #Checking for x out of screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #checking for ESC
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run = False

        #calling draw funcions that draws everything on the display
        draw(win)

    pygame.quit()

#------------------------------------------------------------

#Defining boudarys
topBoundary = boundary(15,15,winX-30,10)
bottomBoundary = boundary(15,winY-10-15,winX-30,10)
leftBoundary = boundary(15,15,10,winY-30)
rightBoundary = boundary(winX-10-15,15,10,winY-30)
boundaryList = [topBoundary,bottomBoundary,leftBoundary,rightBoundary]

#defining ball
ball = projectile(int(winX/2), int(winY/2))

#defining paddle
# player1 = paddle(15+10+15, 200, (0,255,0),pygame.K_w, pygame.K_s)
player1 = paddle(15+10+15, 200, (0,255,0),pygame.K_w, pygame.K_s)
player2 = paddle(winX-15-10-15-10, 200, (0,255,0),pygame.K_UP, pygame.K_DOWN)

#defining goals
goal1 = goalPost(15)
goal2 = goalPost(winX-11-15)

mainLoop()