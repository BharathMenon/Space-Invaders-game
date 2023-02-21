import pygame
from pygame import mixer

import random
import math
pygame.init()
#Initialize the pygame - required for all programs.

screen = pygame.display.set_mode((800,600))
# Created a screen for the game - two parameters are width and height. (width = 800 pixels,height = 600 pixels)
#or (x,y) with x being distance from left to right and y being the distance from top to bottom.(The units being pixels)
# Hence, (0,0) represents the top left point.
#screen variable represents the window of the game. 
# while True:
#     pass
#This by itself, creates a window that can't even be crossed out. This is because we have not added any 
# functionality for quitting.

#Title and Icon
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Background image
bgimg = pygame.image.load('background.png')
bgimg = pygame.transform.scale(bgimg,(800,600))
#Background sound
mixer.music.load('background.wav')
mixer.music.play(-1) #If '-1' is added inside the function, then the sound will be played on a loop till the game stops.

#Player
playerimg = pygame.image.load('ufo.png')
playerimg = pygame.transform.scale(playerimg,(65,65))
x_pl = 370
y_pl = 480
plxchange = 0
#score in game:
score_val = 0
textx = 15
texty = 19
font1 = pygame.font.Font('VarsityTeam-Bold.otf',32)
def show_score(x,y):
    #Before blitting text onto screen, we have to render it first.
    score = font1.render("Score : "+str(score_val),True,(255,255,255))#Arguments of render =>(<String to be entered>,<True>,<RGB value of the color>)
    screen.blit(score,(x,y))
#Game over text
ofont = pygame.font.Font('Championship.ttf',84)
def game_over_text():
    got = ofont.render("GAME OVER",True,(255,255,255))
    screen.blit(got,(200,250))
#Continue to play text
cfont = pygame.font.Font('VarsityTeam-Bold.otf',32) 
def continue_text():
    conf = font1.render("Press any button to play again...",True,(255,255,255))  
    screen.blit(conf,(140,350)) 
def player(x,y):
    screen.blit(playerimg,(x,y)) #Used to draw - here it will be used to draw the player onto the game area.
#Enemies
enemyimg = []
x_en = []
y_en = []
enxchange = []
enychange = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('alien.png'))
    x_en.append(random.randint(0,736))
    y_en.append(random.randint(50,150))
    enxchange.append(3)
    enychange.append(40)
#Bullet
#Bullet state : Ready - We can't see the bullet on the screen.
#               Fire -  The bullet is in action i.e. currently moving.
 
bltimg = pygame.image.load('bullet.png')
x_bl = 0
y_bl = y_pl
blychange = 4
blstate = "ready"
def enemy(x,y):
    screen.blit(enemyimg[i],(x,y))#Used to draw enemy.
def bullet_fire(x,y):
    global blstate
    blstate = "fire"
    screen.blit(bltimg,(x + 16,y + 10))
def iscollision(x_en,y_en,x_bl,y_bl):    
    distance = math.sqrt((math.pow(x_bl-x_en,2))+(math.pow(y_bl-y_en,2)))
    if distance <27:
        return True
    else:
        return False
cind = 0    #Indicator for game to start again.
#Game Loop - Any thing that we need to be perisistent i the game i.e. the game window, has to go inside the 
#game loop.
running = True
while running:
    screen.fill((0,0,0)) #Put in RGB values - First fill the screen, then do everything else.
    #Background image 
    screen.blit(bgimg,(0,0))
    #y_pl+=0.18
    #print(x_pl)
    for event in pygame.event.get():
        #pygame.event.get() is an iterable that basically has information on all the events that are happening now
        #in the game window.
        #So, whatever is happening in the game window is going to be stored in the event variable.     

        if event.type==pygame.QUIT:
            running = False
        # So, crossing out the game window is, according to pygame, an event whose type attribute is equal to 
        # pygame.QUIT 
        #If keystroke is pressed, check whether the keey pressed is left or right.
        if event.type == pygame.KEYDOWN:
            #If the event is a keydown event(A key has been pressed), then the event also has a key attribute.
            if cind==1:
                for j in range(no_of_enemies):
                    y_en[j]=(random.randint(50,150))
                cind = 0    
            if event.key == pygame.K_LEFT:
                plxchange = -5.18
            if event.key == pygame.K_RIGHT:
               plxchange = 5.18
            if event.key == pygame.K_SPACE:
                if blstate == "ready": #Next bullet can only be fired after life of first bullet gets over.
                    bl_sound = mixer.Sound('laser.wav')#Playing sound when bullet is fired!
                    bl_sound.play() 
                    x_bl = x_pl #Making sure that x-coordinate of bullet doesn't change with changing player.
                    bullet_fire(x_pl,y_bl)   
        if event.type == pygame.KEYUP:   
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                plxchange=0      

   #Movements for players:  
    x_pl+=plxchange
    if x_pl<=0: #Left boundary
        x_pl=0
    elif x_pl>=735: #Right boundary
        x_pl=735
    #Movements for enemies: 
    for i in range(no_of_enemies):
        if y_en[i]> 400:
            for j in range(no_of_enemies):
                y_en[j] = 2000
            game_over_text()
            continue_text()
            score_val = 0
            cind = 1
            break

        x_en[i]+=enxchange[i]
        if x_en[i]<=0:
            enxchange[i] = 3
            y_en[i]+=enychange[i]
        elif x_en[i]>=736:
            enxchange[i] = -3
            y_en[i]+=enychange[i]
        #collision    
        collision = iscollision(x_en[i],y_en[i],x_bl,y_bl)
        if collision:
            col_sound = mixer.Sound('explosion.wav')
            col_sound.play()
            y_bl = 480
            blstate = "ready"   
            score_val += 1
            #print(score)
            x_en[i] = random.randint(0,736)
            y_en[i] = random.randint(50,150)  
        enemy(x_en[i],y_en[i]) #Movements of enemy      
   #Setting boundaries for enemy..
    if y_bl <= -32:
        blstate = "ready"
        y_bl = 480
    if blstate == "fire":
        bullet_fire(x_bl,y_bl)             
        y_bl -= blychange 
    
    
    player(x_pl,y_pl) #Will be called after screen.fill(), otherwise screen will be filled over player.
    show_score(textx,texty)
    pygame.display.update()#After fixing any changeable attribute of game window, you have to update it to bring it
    #into acion. 
