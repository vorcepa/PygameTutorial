import pygame as pg
import random as rnd
import utils
import math
pg.init()


class PlayerActive(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((100, 100))
        self.image.fill(utils.BLUE)
        self.rect = self.image.get_rect()

        self.rect.x = 350
        self.rect.y = 250
        self.speed = 5
        self.lives = 30000          # Change later
        utils.ScoreBoard.playerLives = self.lives

        self.spawnDelay = 0
        self.spawnDelayMax = 15
        self.ammo = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        self.cooldown = 10
        self.cooldownMax = 10
        self.isAlive = True

        self.objvCounter = 0
        self.objvCounterMax = 15

    def move(self, xdir, ydir):
        self.rect.x += xdir*self.speed
        self.rect.y += ydir*self.speed

    def spawnAmmo(self):
        self.ammo.add(Bullet())
        utils.ScoreBoard.playerAmmo = len(self.ammo)

    def moveAmmo(self):
        self.image.fill(utils.BLUE)
        for obj in self.ammo:
            if obj.rect.x + obj.rect.width >= self.rect.width:
                obj.xmove *= -1
            if obj.rect.y + obj.rect.height >= self.rect.height + 8:
                obj.ymove *= -1
            if obj.rect.x <= 0:
                obj.xmove *= -1
            if obj.rect.y <= 0 - 8:
                obj.ymove *= -1

            obj.rect.x += obj.xmove
            obj.rect.y += obj.ymove
            self.image.blit(obj.image, obj.rect)

    def shoot(self, target):
        if self.cooldown <= 0 and self.ammo:
            self.cooldown = self.cooldownMax
            bullet = self.ammo.sprites()[0]
            self.ammo.remove(bullet)

            bullet.rect.x = (self.rect.x + self.rect.width/2 -
                             bullet.rect.width/2)
            bullet.rect.y = (self.rect.y + self.rect.height/2 -
                             bullet.rect.height/2)

            bullet.setTarg(target)
            self.bullets.add(bullet)

    def doObjective(self, objv):
        if self.objvCounter < -30:
            objv.charPos = len(objv.displayMessage)

        if self.objvCounter <= 0 and objv.displayMessage != objv.winMessage:
            self.objvCounter = self.objvCounterMax
            tempLetter = objv.winMessage[objv.charPos]

            if tempLetter == " ":
                objv.charPos += 1
                return
            for shot in self.ammo:
                if shot.name == tempLetter.upper():
                    self.ammo.remove(shot)
                    shot.rect.x = self.rect.x + 25
                    shot.rect.y = self.rect.y + 25
                    setTargX = objv.rect.x + objv.rect.width/2
                    setTargY = objv.rect.y + objv.rect.height/2
                    shot.setTarg((setTargX, setTargY))

                    self.bullets.add(shot)
                    objv.charPos += 1
                    return

    def takeDamage(self):
        self.lives -= 1
        utils.ScoreBoard.playerLives = self.lives

        if self.lives <= 0:
            self.destroy()

    def destroy(self):
        self.isAlive = False

    def update(self, gw):
        if self.isAlive:
            self.cooldown -= 1
            self.spawnDelay -= 1
            if self.spawnDelay <= 0:
                self.spawnAmmo()
                self.spawnDelay = self.spawnDelayMax

            gw.blit(self.image, self.rect)

            self.moveAmmo()

            self.bullets.update()
            self.bullets.draw(gw)

            self.objvCounter -= 1


#charList = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
charList = "I F T H S P E L D N Y O U W".split()


class Bullet(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.name = rnd.choice(charList)
        self.image = utils.getFont(size=30,
                                   style='bold').render(self.name,
                                                        True, utils.BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = rnd.randint(5, 75)
        self.rect.y = rnd.randint(5, 75)

        self.xmove = rnd.choice([-2, -1, 1, 2])
        self.ymove = rnd.choice([-2, -1, 1, 2, 1])
        self.speed = 20.0

    def setTarg(self, target):
        xdiff = target[0] - self.rect.x - self.rect.width/3
        ydiff = target[1] - self.rect.y - self.rect.height/3

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
        numFrames = int(magnitude / self.speed)

        self.xmove = xdiff/numFrames
        self.ymove = ydiff/numFrames

        xtravel = self.xmove * numFrames
        ytravel = self.ymove * numFrames

        self.rect.x += xdiff - xtravel
        self.rect.y += ydiff - ytravel

    def destroy(self):
        self.kill()

    def checkDist(self):
        if self.rect.x < -100 or self.rect.x > 2200:
            self.destroy()
        if self.rect.y < -100 or self.rect.y > 2200:
            self.destroy()

    def update(self):
        self.checkDist()
        self.rect.x += self.xmove
        self.rect.y += self.ymove


class Objective():
    def __init__(self):
        self.winMessage = "If this is spelled then you win"
        self.displayMessage = ""
        self.image = pg.Surface((600, 100))
        self.charPos = 0
        self.redraw()
        self.rect.x = 100
        self.rect.y = 600

    def redraw(self):
        self.image.fill(utils.GREEN)

        self.ghostText = utils.getFont(size=24,
                                       style='bold').render(self.winMessage,
                                                            True, utils.GREY)
        self.image.blit(self.ghostText, (25, 25))

        self.text = utils.getFont(size=24,
                                  style='bold').render(self.displayMessage,
                                                       True, utils.BLACK)
        self.image.blit(self.text, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 500

    def update(self, gw):
        gw.blit(self.image, self.rect)
