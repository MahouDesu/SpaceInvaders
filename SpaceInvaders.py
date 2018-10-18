import pygame

windowWidth = 500
windowHeight = 600
gameSideMargin = 10
gameTopMargin = 40
gameBottomMargin = gameTopMargin
gameBorderWidth = 3

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

pygame.init()

gameDisplay  = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Space Invaders')

clock = pygame.time.Clock()
backgroundImg = pygame.image.load("si-background.gif")
playerImg = pygame.image.load("si-player.gif")

# Player Abilities
class Player:
    xcor = 60
    ycor = windowHeight - gameBottomMargin - gameBorderWidth - playerImg.get_height()
    speed = 5
    direction = 0
    def stopMoving(self):
        self.direction = 0
    def show(self):
        movementAmount = self.direction * self.speed
        newx = self.xcor + movementAmount

        if newx < gameSideMargin + gameBorderWidth or newx > windowWidth - gameSideMargin - gameBorderWidth - playerImg.get_width():
            self.xcor = self.xcor
        else:
            self.xcor = newx
        
        gameDisplay.blit(playerImg, (self.xcor, self.ycor)) 
    def moveRight(self):
        self.direction = 1
    def moveLeft(self):
        self.direction = -1

player = Player()

#Player movement.
isAlive = True
while isAlive:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isAlive == False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moveLeft()
            elif event.key == pygame.K_RIGHT:
                player.moveRight()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stopMoving()



    
    gameDisplay.blit(gameDisplay, (0, 0))
    gameDisplay.fill(black)

    gameDisplay.blit(backgroundImg, (gameSideMargin, gameTopMargin))

    gameDisplay.blit(gameDisplay, (0, 0))
    gameDisplay.fill(black)

    gameWidth = windowWidth - (gameSideMargin * 2) - (gameBorderWidth * 2)
    gameHeight = windowHeight - gameTopMargin - gameBottomMargin - (gameBorderWidth * 2)

    # Draw a white rectangle with the background image just inside of it to create the game border
    pygame.draw.rect(gameDisplay, white, (gameSideMargin, gameTopMargin, windowWidth - gameSideMargin * 2, windowHeight - gameBottomMargin - gameTopMargin))                                 
    gameDisplay.blit(backgroundImg, (gameSideMargin + gameBorderWidth, gameTopMargin + gameBorderWidth), (0, 0, gameWidth, gameHeight))

    player.show()

    pygame.display.update()
    clock.tick(60)