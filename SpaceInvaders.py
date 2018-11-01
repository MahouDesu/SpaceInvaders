import pygame
import random

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
scoreFont = pygame.font.SysFont('Arial', 26, True)

clock = pygame.time.Clock()
backgroundImg = pygame.image.load("si-background.gif")
playerImg = pygame.image.load("si-player.gif")
enemyImg = pygame.image.load("kappa.png")
bulletImg = pygame.image.load("si-bullet.gif")
enemyBulletImg = pygame.image.load("si-bullet.gif")

laserSound = pygame.mixer.Sound('hadouken.wav')
explosionSound = pygame.mixer.Sound('invaderKilled.wav')

def isCollision(a, b):
    return a.xcor + a.width > b.xcor and a.xcor < b.xcor + b.width \
    and a.ycor + a.height > b.ycor and a.ycor < b.ycor + b.height
    
class GameObject:
    def __init__(self, xcor, ycor, image, speed):
        self.xcor = xcor
        self.ycor = ycor
        self.img = image
        self.speed = speed
        self.width = image.get_width()
        self.height = image.get_height()
    def show(self):
        gameDisplay.blit(self.img, (self.xcor, self.ycor))


# Player Abilities
class Player(GameObject):
    def __init__(self, xcor, ycor, image, speed):
        super(). __init__(xcor, ycor, image, speed)
        self.direction = 0
        self.score = 0
        self.level = 0
        self.isAlive = True
    def stopMoving(self):
        self.direction = 0
    def show(self):
        newx = self.xcor + self.direction * self.speed
        if newx < wallLeft or newx > windowWidth - gameSideMargin - gameBorderWidth - playerImg.get_width():
            self.xcor = self.xcor
        else:
            self.xcor = newx
        super().show()
        gameDisplay.blit(playerImg, (self.xcor, self.ycor)) 
    def moveRight(self):
        self.direction = 1
    def moveLeft(self):
        self.direction = -1
    def shoot(self):
        laserSound.play()
        newBullet = Bullet(self.xcor + player.width / 2 - bulletImg.get_width() / 2, self.ycor, bulletImg, 10)
        bullets.append(newBullet)

class Enemy(GameObject):
    def __init__(self, xcor, ycor, image, speed):
        super().__init__(xcor, ycor, image, speed)
        self.direction = 1
    def show(self):
        gameDisplay.blit(enemyImg, (self.xcor, self.ycor))
    def moveOver(self):
        self.xcor += self.direction * self.speed
    def moveDown(self):
        self.ycor += enemyImg.get_height() / 2
    def changeDirection(self):
        self.direction *= -1
    def shoot(self):
        newBullet = Bullet(self.xcor + self.width / 2, self.ycor, bulletImg, -2)
        enemyBullets.append(newBullet)
    @staticmethod
    def createEnemies(level):
        newEnemies = []
        for x in range(0, 5):
            for y in range(0, level.enemyRowCount):
                newEnemy = Enemy(wallLeft + 1 + enemyImg.get_width() * x, wallTop + enemyImg.get_height() * y, enemyImg, level.enemySpeed)
                newEnemies.append(newEnemy)
        return newEnemies

class Bullet(GameObject):
    def __init__(self, x, y, image, speed):
        super().__init__(x,y, image, speed)
    def move(self):
        self.ycor -= self.speed

class Level:
    def __init__(self, number, enemyRowCount, enemyColumnCount, enemySpeed):
        self.number = number
        self.enemyRowCount = enemyRowCount
        self.enemyColumnCount = enemyColumnCount
        self.enemySpeed = enemySpeed

pygame.mixer.music.load('Hat.mp3')
pygame.mixer.music.play(-1)

player = Player(windowWidth / 2 - playerImg.get_width() / 2, wallBottom - playerImg.get_height(), playerImg, 5)

bullets = []
enemyBullets = []
levels = []
enemies = []

levels.append(Level(1, 3, 5, 1))
levels.append(Level(2, 5, 6, 2))
levels.append(Level(3, 5, 8, 3))

pointPerEnemy = 100
enemyShotDelay = 0

leftIsDown = False
rightIsDown = False
lastKeyLeft = False
#Player movement.

while player.isAlive:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            player.isAlive == False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                leftIsDown = True
                lastKeyLeft = True
                
            elif event.key == pygame.K_RIGHT:
                rightIsDown = True
                lastKeyLeft = False
                
            elif event.key == pygame.K_SPACE:
                player.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftIsDown = False
                lastKeyLeft = False
            elif event.key == pygame.K_RIGHT:
                rightIsDown = False
                lastKeyLeft = True
            player.stopMoving()

        if rightIsDown or leftIsDown:
            if lastKeyLeft:
                player.moveLeft()
            else:
                player.moveRight()

    for enemy in enemies:
        if isCollision(enemy, player):
            player.isAlive = False
        if enemy.xcor + enemyImg.get_width() >= wallRight or enemy.xcor <= wallLeft:
            for e in enemies:
                e.changeDirection()
                e.moveDown()
            break

    if len(enemies) == 0:
        player.level += 1
        enemies = Enemy.createEnemies(levels[player.level - 1])

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
                    explosionSound.play()
                    player.score += pointPerEnemy
                except ValueError:
                    pass
                try:    
                    bullets.remove(bullet)
                except ValueError:
                    pass
                continue

    for bullet in enemyBullets:
        if bullet.ycor < wallTop > wallBottom:
            try:
                enemyBullets.remove(bullet)
            except ValueError:
                pass
        if isCollision(player, bullet):
            player.isAlive = False
    
    enemyShotDelay += 1    
    for enemy in enemies:
        if (enemyShotDelay > 100 and random.randint(1, len(enemies) + 1) == 1):
            enemy.shoot()
            enemyShotDelay = 0
        enemy.moveOver()

    for bullet in bullets:
        bullet.move()
    
    for bullet in enemyBullets:
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

    for bullet in enemyBullets:
        bullet.show()

    for enemy in enemies:
        enemy.show()

    for bullet in bullets:
        bullet.show()

    player.show()

    titleText = titleFont.render('SPACE INVADERS', False, green)
    scoreText = scoreFont.render('SCORE:' + str(player.score), False, white)
    gameDisplay.blit(titleText, (windowWidth / 2 - titleText.get_width() / 2, 0))
    gameDisplay.blit(scoreText, (wallLeft, wallBottom + gameBorderWidth))
    pygame.display.update()
    clock.tick(60)

showEndScreen = True
while showEndScreen:

    for event in pygame.event.get():
        #print(str(event))
        if event.type == pygame.QUIT:
            showEndScreen = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                showEndScreen = False

    gameDisplay.blit(gameDisplay, (0, 0))
    gameDisplay.fill(black)

    gameWidth = wallRight - wallLeft
    gameHeight = wallBottom - wallTop

    # Draw a white rectangle with the background image just inside of it to create the game border
    pygame.draw.rect(gameDisplay, white, (gameSideMargin, gameTopMargin, windowWidth - gameSideMargin * 2, windowHeight - gameBottomMargin - gameTopMargin))                                 
    gameDisplay.blit(backgroundImg, (wallLeft, wallTop), (0, 0, gameWidth, gameHeight))
    
    titleText = titleFont.render('SPACE INVADERS', False, blue)
    scoreText = scoreFont.render('SCORE: ' + str(player.score), False, white)
    gameDisplay.blit(titleText, (windowWidth / 2 - titleText.get_width() / 2, 0))
    gameDisplay.blit(scoreText, (windowWidth / 2 - scoreText.get_width() / 2, 300))

    pygame.display.update()

    clock.tick(60)
    
pygame.quit()
