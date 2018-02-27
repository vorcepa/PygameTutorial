import pygame as pg
pg.init()


def getFont(name="Courier New", size=20, style=''):
    return pg.font.SysFont(name, size, style)


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)


class ScoreBoard():

    enemiesKilled = 0
    playerAmmo = 0
    playerLives = 0

    def __init__(self, gameWindow):
        self.surf = pg.Surface((200, 150))
        self.image = gameWindow.subsurface(600, 0, 200, 150)

        self.rect = self.image.get_rect()
        self.rect.x = 600

    def drawEnemiesKilled(self):
        text = getFont(style='bold').render(
                      ("Killed: " + str(ScoreBoard.enemiesKilled)),
                      False, WHITE)
        self.image.blit(text, (5, 10))

    def drawPlayerAmmo(self):
        text = getFont(style='bold').render(
                      ("Ammo: " + str(ScoreBoard.playerAmmo)), False, WHITE)
        self.image.blit(text, (5, 35))

    def drawPlayerLives(self):
        text = getFont(style='bold').render(
                      ("Lives: " + str(ScoreBoard.playerLives)), False, WHITE)
        self.image.blit(text, (5, 60))

    def update(self, gw):
        self.drawEnemiesKilled()
        self.drawPlayerAmmo()
        self.drawPlayerLives()

        self.surf.blit(self.image, (0, 0))
        gw.blit(self.surf, self.rect)
