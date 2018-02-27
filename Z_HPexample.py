import pygame as pg
import utils

pg.init()
gameWindow = pg.display.set_mode((800, 600))
pg.display.set_caption("Health bar example")
clock = pg.time.Clock()
FPS = 30


class Box(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((100, 100))
        self.image.fill(utils.BLUE)
        self.rect = self.image.get_rect()

        self.rect.x = 250
        self.rect.y = 250

        self.maxHP = 10
        self.HP = self.maxHP

        self.hasClicked = False

        self.hbWidth = 80
        self.hbHeight = 15
        self.hbBase = pg.Surface((self.hbWidth, self.hbHeight))

    def drawHB(self):
        width = int((self.HP / self.maxHP) * self.hbWidth)

        hb = pg.Surface((width, self.hbHeight))
        hb.fill(utils.BLACK)
        self.hbBase.fill(utils.RED)

        self.hbBase.blit(hb, (0, 0))
        self.image.blit(self.hbBase, (10, 80))

    def takeDamage(self):
        self.HP -= 1
        self.drawHB()

        if self.HP <= 0:
            self.kill()

    def update(self):
        cur = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()

        if click[0] and not self.hasClicked:
            self.hasClicked = True
            if self.rect.left < cur[0] < self.rect.right and self.rect.top < cur[1] < self.rect.bottom:
                self.takeDamage()
        elif not click[0]:
            self.hasClicked = False


allSprites = pg.sprite.Group()
allSprites.add(Box())

gameActive = True
while gameActive:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameActive = False

    gameWindow.fill(utils.WHITE)
    allSprites.update()
    allSprites.draw(gameWindow)

    pg.display.update()
    clock.tick(FPS)

pg.quit()
quit()
