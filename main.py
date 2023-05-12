import math     #to use pow function
import random   
import pygame    #other libraries that can be used are pyglet or python ogre
from pygame import mixer   # module to load and import music files / basically to handle that stuff we use mixer 

# Intialize the pygame
pygame.init()    #this returna=s a tuple of modules that have been initailizaed successfully and those other modules that have failed to initialize.

# create the screen
screen = pygame.display.set_mode((800, 600))     #this 800 and 600 are the specified width and height of our game window.
                                                  #Here there is a hierarchy of imports.
# Background
background = pygame.image.load('background.png')  

# Sound..
mixer.music.load("background.wav")
mixer.music.play(-1)            # this is to play the music in an infinte loop

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370    #these are the coordinates of the player(spaceship)
playerY = 480
playerX_change = 0   #No change in the X direction of the player as of now.

# Enemy..
enemyImg = []    
enemyX = []     #list of coordinates in the x direction  
enemyY = []     #list of coordinates in the y direction
enemyX_change = []    #list of coordinate change in the x direction
enemyY_change = []    #list of coordinate change  in the y direction
num_of_enemies = 6

for i in range(num_of_enemies):   
    enemyImg.append(pygame.image.load('enemy.png'))   #it adds/loads the enemy.png at the end of the enemyImg list 
    enemyX.append(random.randint(0, 736))  #random.randint generates a random interger between 0 and 736 (both inclusive) :- This gives us the x-coordinate of the enemey[i].
    enemyY.append(random.randint(50, 150))  
    enemyX_change.append(4)   #thus the enemey will move 4 pixels per frame in wither left or right direction (x-axis).
    enemyY_change.append(40)   #thus the enemey will move 40 pixels per frame in either left or right direction (x-axis).

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480   #the same as the player 
bulletX_change = 0  #thus when the bullet will be fired there will be no change in the x direction only in the y direction
bulletY_change = 10
bullet_state = "ready"    # Ready - You can't see the bullet on the screen

# Score

score_value = 0     
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
#Nidhi--------------X

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))   #so the blit copies the pixels of one image onto the other image
                                 #(x,y)  is the positional coordinates passed onto the blit for displaying the score at the speciifed poistion

def game_over_text():  
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))  #True so that the text appears in a smooth or jagged way.
    screen.blit(over_text, (200, 250))  


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state  
    bullet_state = "fire"   
    screen.blit(bulletImg, (x + 16, y + 10))   


def isCollision(enemyX, enemyY, bulletX, bulletY):  # this function as the name suggests is used to tell whether the bullte and enemy have overlapped  or not.
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))  
    if distance < 27:
        return True   #then the collision has taken place 
    else:
        return False  


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))  
    # Background Image
    screen.blit(background, (0, 0))  # 0,0 is for the top left corner .
    for event in pygame.event.get():    # the main module for dealing eith user input is module.event. Pygame will register all events from the user into an event queue which can be received with the code pygame.event.get().
        if event.type == pygame.QUIT:  #Each returned event has a type that tells me what generated this event.
            running = False     
       #some event types in pygame are QUIT, KEYUP OR KEYDOWN.
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5   #in the left direction 
            if event.key == pygame.K_RIGHT:
                playerX_change = 5    #in the right direction.
            if event.key == pygame.K_SPACE:     # to fire the bullet we will press the K_SPACE
                if bullet_state is "ready":     
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0   #whatever key that I have pressed means that my spaceship cannot move at that point.

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:   #we have reached the far left edge of the screen
        playerX = 0
    elif playerX >= 736:   # We have reached the right edge of the screen
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000   #to remove them from the screen (all of the enemies)
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]   #These define the movements of the enemy
        if enemyX[i] <= 0:    #these are for the left edge.
            enemyX_change[i] = 4      
            enemyY[i] += enemyY_change[i] 
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480   #the same as before
            bullet_state = "ready"
            score_value += 1  
            enemyX[i] = random.randint(0, 736)   #here again the enemy"i" is relocated to some other place .
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
