import pygame as pg
import utils
from GenericPlayer import PlayerActive, Objective
import BasicEnemy
from ClickableRect import TextButton
from BackgroundMap import GameMap


class Tutorial_Game():
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        pg.display.set_caption("Pygame Tutorial")
        self.clock = pg.time.Clock()
        self.FPS = 30

        self.enemies = BasicEnemy.Enemy.enemies
        self.player = PlayerActive()
        self.objv = Objective()
        self.scoreB = utils.ScoreBoard(gameWindow)
        self.map = GameMap()

    def quitGame(self):
        pg.quit()
        raise SystemExit(0)

    def gotoMenu(self):
        rect = self.gameWindow.get_rect()

        def startPlay():
            self.menu = False

        playB = TextButton((rect.centerx, rect.centery - 100), (200, 80),
                           utils.GREEN, "Play", startPlay)
        quitB = TextButton((rect.centerx, rect.centery + 50), (200, 80),
                           utils.RED, "Quit", self.quitGame)

        self.menu = True
        while self.menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                        self.quitGame()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.menu = False

            self.gameWindow.fill(utils.WHITE)
            text = utils.getFont(size=82,
                                 style='bold').render("Tutorial Game",
                                                      True, utils.BLACK)
            textRect = text.get_rect()
            textRect.center = self.gameWindow.get_rect().center
            textRect.y -= 250
            self.gameWindow.blit(text, textRect)
            playB.update(self.gameWindow)
            quitB.update(self.gameWindow)

            pg.display.update()
            self.clock.tick(self.FPS)

    def pause(self):
        pause = True
        while pause:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quitGame()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        print("Game unpaused.")
                        pause = False

                text = utils.getFont(size=96,
                                     style='bold').render("PAUSED",
                                                          True, utils.BLACK)
                textRect = text.get_rect()
                textRect.center = self.gameWindow.get_rect().center

                self.gameWindow.blit(text, textRect)
                pg.display.update()
                self.clock.tick(self.FPS)

    def playGame(self):
        self.gotoMenu()

        gameActive = True
        while gameActive:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameActive = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        print("Game Paused.")
                        self.pause()

            activeKey = pg.key.get_pressed()
            if activeKey[pg.K_RIGHT]:
                self.player.move(1, 0)
            if activeKey[pg.K_LEFT]:
                self.player.move(-1, 0)
            if activeKey[pg.K_UP]:
                self.player.move(0, -1)
            if activeKey[pg.K_DOWN]:
                self.player.move(0, 1)
            if activeKey[pg.K_SPACE]:
                self.player.doObjective(self.objv)

            playerCollision = pg.sprite.spritecollide(self.player,
                                                      self.enemies, False)
            for enemy in playerCollision:
                enemy.destroy()
                self.player.takeDamage()

            bulletCollision = pg.sprite.groupcollide(self.enemies,
                                                     self.player.bullets,
                                                     False, True)
            for enemy in bulletCollision:
                enemy.takeDamage()

            objvCollision = pg.sprite.spritecollide(self.objv,
                                                    self.player.bullets, False)
            for bullet in objvCollision:
                tempLetter = self.objv.winMessage[len(self.objv.displayMessage)]
                if tempLetter.upper() == bullet.name:
                    self.objv.displayMessage += tempLetter
                    self.objv.redraw()
                    bullet.destroy()
                    if self.objv.winMessage[len(self.objv.displayMessage)] == " ":
                        self.objv.displayMessage += " "
                        print(self.objv.displayMessage)

            self.gameWindow.fill(utils.WHITE)
            self.map.resetMap()

            self.player.update(self.map.activeMap)
            self.enemies.update(self.player)
            self.objv.update(self.map.activeMap)
            self.enemies.draw(self.map.activeMap)
            self.player.moveAmmo()
            self.objv.redraw()

            BasicEnemy.spawn()

            cur = pg.mouse.get_pos()
            mouse = pg.mouse.get_pressed()
            if mouse[0]:
                self.player.shoot((cur[0] - self.map.offsetX,
                                   cur[1] - self.map.offsetY))

            self.map.update(self.gameWindow, self.player.rect)
            self.scoreB.update(self.gameWindow)
            pg.display.update()
            self.clock.tick(self.FPS)

        self.quitGame()


if __name__ == "__main__":
    pg.init()
    gameWindow = pg.display.set_mode((800, 600))
    game = Tutorial_Game(gameWindow)
    game.playGame()
