import pygame as pg
import utils
pg.init()


class GameMap():
    def __init__(self):
        self.mapImage = None
        self.createMap()
        self.activeMap = None
        self.offsetX = 0
        self.offsetY = 0

        self.scrollSpeed = 5

    def createMap(self):
        self.mapImage = pg.Surface((2100, 2100))

        lightTile = pg.Surface((100, 100))
        lightTile.fill((160, 160, 160))
        darkTile = pg.Surface((100, 100))
        darkTile.fill((50, 50, 50))
        toggle = True

        for y in range(0, 21):
            for x in range(0, 21):
                if toggle:
                    self.mapImage.blit(lightTile, (x*100, y*100))
                    toggle = not toggle
                else:
                    self.mapImage.blit(darkTile, (x*100, y*100))
                    toggle = not toggle

    def resetMap(self):
        self.activeMap = self.mapImage.copy()

    def update(self, gameWindow, playerRect):
        rect = gameWindow.get_rect()

        # map scroll
        if playerRect.centerx > rect.centerx - self.offsetX + 25:
            self.offsetX -= self.scrollSpeed
        elif playerRect.centerx < rect.centerx - self.offsetX - 25:
            self.offsetX += self.scrollSpeed

        if playerRect.centery > rect.centery - self.offsetY + 25:
            self.offsetY -= self.scrollSpeed
        elif playerRect.centery < rect.centery - self.offsetY - 25:
            self.offsetY += self.scrollSpeed

        if playerRect.left < 0:
            playerRect.left = 0
        elif playerRect.right > 2100:
            playerRect.right = 2100

        if playerRect.top < 0:
            playerRect.top = 0
        elif playerRect.bottom > 2100:
            playerRect.bottom = 2100

        if self.offsetX > 0:
            self.offsetX = 0
        elif self.offsetX < rect.width - 2100:
            self.offsetX = rect.width - 2100

        if self.offsetY > 0:
            self.offsetY = 0
        elif self.offsetY < rect.height - 2100:
            self.offsetY = rect.height - 2100

        gameWindow.blit(self.activeMap, (self.offsetX, self.offsetY))
