import pygame

windowWidth = 500
windowHeight = 600
gameSideMargin = 10
gameTopMargin = 40
gameBottomMargin = gameTopMargin
gameBorderWidth = 3
wallLeft = gameSideMargin + gameBorderWidth
wallRight = windowWidth - gameSideMargin - gameBorderWidth
wallTop = gameTopMargin + gameBorderWidth
wallBottom = windowHeight - gameBottomMargin - gameBorderWidth

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

pygame.init()

gameDisplay  = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Space Invaders')

titleFont = pygame.font.SysFont('Arial', 40, True)

clock = pygame.time.Clock()
backgroundImg = pygame.image.load("si-background.gif")
playerImg = pygame.image.load("si-player.gif")
enemyImg = pygame.image.load("kappa.png")
bulletImg = pygame.image.load("si-bullet.gif")

def isCollision(a, b):
    if a.xcor + a.width > b.xcor and a.xcor < b.xcor + b.width \
    and a.ycor + a.height > b.ycor and a.ycor < b.ycor + b.height:
        return True
    else:
        return False




# Player Abilities
class Player:
    xcor = 60
    ycor = wallBottom - playerImg.get_height()
    width = playerImg.get_width()
    height = playerImg.get_height()
    speed = 5
    direction = 0
    def stopMoving(self):
        self.direction = 0
    def show(self):
        movementAmount = self.direction * self.speed
        newx = self.xcor + movementAmount

        if newx < wallLeft or newx > windowWidth - gameSideMargin - gameBorderWidth - playerImg.get_width():
            self.xcor = self.xcor
        else:
            self.xcor = newx
        
        gameDisplay.blit(playerImg, (self.xcor, self.ycor)) 
    def moveRight(self):
        self.direction = 1
    def moveLeft(self):
        self.direction = -1

class Enemy:
    xcor = 0
    ycor = 0
    width = enemyImg.get_width()
    height = enemyImg.get_height()
    speed = 1
    direction = 1
    def show(self):
        gameDisplay.blit(enemyImg, (self.xcor, self.ycor))
    def moveOver(self):
        self.xcor += self.direction * self.speed
    def moveDown(self):
        self.ycor += enemyImg.get_height() / 2
    def changeDirection(self):
        self.direction *= -1
    @staticmethod
    def createEnemies():
        newEnemies = []
        for x in range(0, 5):
            for y in range(0, 3):
                newEnemy = Enemy()
                newEnemy.xcor = wallLeft + 1 + enemyImg.get_width() * x
                newEnemy.ycor = wallTop + enemyImg.get_height() * y
                newEnemies.append(newEnemy)
        return newEnemies

class Bullet:
    xcor = 0
    ycor = 0
    width = bulletImg.get_width()
    height = bulletImg.get_height()
    speed = 10
    def __init__(self, x, y):
        self.xcor = x
        self.ycor = y
    def show(self):
        gameDisplay.blit(bulletImg, (self.xcor, self.ycor))
    def move(self):
        self.ycor -= self.speed



pygame.mixer.music.load('Hat.mp3')
pygame.mixer.music.play(-1)

player = Player()
enemies = Enemy.createEnemies()
bullets = []

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
            elif event.key == pygame.K_SPACE:
                newBullet = Bullet(player.xcor, player.ycor)
                bullets.append(newBullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stopMoving()

    for enemy in enemies:
        if isCollision(enemy, player):
            isAlive = False
        if enemy.xcor + enemyImg.get_width() >= wallRight or enemy.xcor <= wallLeft:
            for e in enemies:
                e.changeDirection()
                e.moveDown()
            break

    for bullet in bullets:
        if bullet.ycor < wallTop:
            try:
                bullets.remove(bullet)
            except ValueError:
                pass
            break
        for enemy in enemies:
            if isCollision(enemy, bullet):
                try:
                    enemies.remove(enemy)
                except ValueError:
                    pass
                try:    
                    bullets.remove(bullet)
                except ValueError:
                    pass
                break

    for enemy in enemies:
        enemy.moveOver()

    for bullet in bullets:
        bullet.move()
    

    
    gameDisplay.blit(gameDisplay, (0, 0))
    gameDisplay.fill(black)

    gameDisplay.blit(backgroundImg, (gameSideMargin, gameTopMargin))

    gameDisplay.blit(gameDisplay, (0, 0))
    gameDisplay.fill(black)

    gameWidth = wallRight - wallLeft
    gameHeight = wallBottom - wallTop

    # Draw a white rectangle with the background image just inside of it to create the game border
    pygame.draw.rect(gameDisplay, white, (gameSideMargin, gameTopMargin, windowWidth - gameSideMargin * 2, windowHeight - gameBottomMargin - gameTopMargin))                                 
    gameDisplay.blit(backgroundImg, (wallLeft, wallTop), (0, 0, gameWidth, gameHeight))

    for enemy in enemies:
        enemy.show()

    for bullet in bullets:
        bullet.show()

    player.show()

    titleText = titleFont.render('SPACE INVADERS', False, green)
    gameDisplay.blit(titleText, (windowWidth / 2 - titleText.get_width() / 2, 0))

    pygame.display.update()
    clock.tick(60)
