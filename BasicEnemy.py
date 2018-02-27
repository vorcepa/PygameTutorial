import pygame as pg
import utils
import math
import random
pg.init()

spawnCD = 0
spawnCDMax = 90


def spawn():
    global spawnCD, spawnCDMax
    spawnCD -= 1

    if spawnCD <= 0:
        newEnemy = Enemy()
        Enemy.enemies.add(newEnemy)
        newEnemy.rect.x = random.randrange(-100, -50)
        newEnemy.rect.y = random.randrange(-50, 650)

        spawnCD = spawnCDMax


class Enemy(pg.sprite.Sprite):

    enemies = pg.sprite.Group()

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((50, 50))
        self.image.fill(utils.RED)
        self.rect = self.image.get_rect()
        self.speed = 3
        self.cd = 30
        self.cdMax = 30

        Enemy.enemies.add(self)

        self.maxHP = 10
        self.HP = self.maxHP

        self.hbWidth = 40
        self.hbHeight = 8
        self.hbBase = pg.Surface((self.hbWidth, self.hbHeight))

    def stalkPlayer(self, player):
        xdiff = (player.rect.x +
                 player.rect.width/2) - self.rect.x + self.rect.width/3
        ydiff = (player.rect.y +
                 player.rect.height/2) - self.rect.y + self.rect.height/3

        magnitude = math.sqrt(float(xdiff ** 2 + ydiff ** 2))
        numFrames = int(magnitude / self.speed)

        xmove = xdiff/numFrames
        ymove = ydiff/numFrames

        self.rect.x += xmove
        self.rect.y += ymove

    def update(self, player):
        self.stalkPlayer(player)

    def drawHB(self):
        width = int((self.HP / self.maxHP) * self.hbWidth)

        hb = pg.Surface((width, self.hbHeight))
        hb.fill(utils.BLACK)
        self.hbBase.fill(utils.RED)

        self.hbBase.blit(hb, (0, 0))
        self.image.blit(self.hbBase, (5, 38))

    def takeDamage(self):
        self.HP -= 1
        self.drawHB()
        if self.HP <= 0:
            self.destroy()

    def destroy(self):
        self.kill()
        utils.ScoreBoard.enemiesKilled += 1
