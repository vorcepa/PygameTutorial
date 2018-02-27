import pygame as pg
import utils

pg.init()
gameWindow = pg.display.set_mode((800, 600))
pg.display.set_caption("Button example")
clock = pg.time.Clock()
FPS = 30
interact = None

def getFont(name='Courier New', size=20, style=''):
    return pg.font.SysFont(name, size, style)


class ClickableRect():
    def __init__(self, pos, size):
        self.rect = pg.Rect((0, 0), size)
        self.rect.center = pos

        self.hasClicked = False

    def isMouseOver(self):
        cur = pg.mouse.get_pos()

        if self.rect.left < cur[0] < self.rect.right and self.rect.top < cur[1] < self.rect.bottom:
            return True
        else:
            return False

    def doMouseOver(self):
        pass

    def isClicked(self):
        global interact
        mouse = pg.mouse.get_pressed()

        if self.isMouseOver():
            if mouse[0] and not self.hasClicked and not interact:
                self.hasClicked = True
                interact = self
                return True
        if not mouse[0] and self.hasClicked:
            self.hasClicked = False
            interact = None

        return False

    def doClick(self):
        print("You clicked a rect.")

    def isLeftMouseDown(self):
        return self.hasClicked

    def doLeftMouseDown(self):
        pass

    def update(self, gameWindow):
        if self.isMouseOver():
            self.doMouseOver()
        if self.isLeftMouseDown():
            self.doLeftMouseDown()
        if self.isClicked():
            self.doClick()


class Button(ClickableRect):
    def __init__(self, pos, size, color, action):
        ClickableRect.__init__(self, pos, size)

        self.color = color
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.action = action

    def doMouseOver(self):
        overlay = pg.Surface(self.rect.size)
        overlay.set_alpha(60)
        overlay.fill(utils.BLACK)
        self.image.blit(overlay, (0, 0))

    def doLeftMouseDown(self):
        self.image.fill(utils.BLUE)

    def draw(self, gameWindow):
        gameWindow.blit(self.image, self.rect)

    def doClick(self):
        self.action()

    def update(self, gameWindow):
        self.image.fill(self.color)
        ClickableRect.update(self, gameWindow)
        self.draw(gameWindow)


class TextButton(Button):
    def __init__(self, pos, size, color, text, action):
        Button.__init__(self, pos, size, color, action)
        self.text = getFont(size=36, style='bold').render(text, False,
                                                          utils.BLACK)

    def doClick(self):
        self.action()

    def draw(self, gameWindow):
        self.image.blit(self.text, (10, 10))
        Button.draw(self, gameWindow)


def printButton():
    print("Hello, I am a button.")


def playGame():
    print("Your game has started.")


# Variables
rect = ClickableRect((gameWindow.get_rect().centerx,
                      gameWindow.get_rect().centery - 200), (200, 80))
button = TextButton((gameWindow.get_rect().centerx,
                     gameWindow.get_rect().centery),
                    (200, 80), utils.RED, "Quit", printButton)
txtButton = TextButton((gameWindow.get_rect().centerx,
                        gameWindow.get_rect().centery + 100), (200, 80),
                       utils.GREEN, "Play", playGame)

# Game loop
gameActive = True

while gameActive:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameActive = False

    gameWindow.fill(utils.WHITE)
    rect.update(gameWindow)
    button.update(gameWindow)
    txtButton.update(gameWindow)

    pg.display.update()
    clock.tick(FPS)

pg.quit()
quit()
