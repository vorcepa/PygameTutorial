import pygame as pg
import utils

interact = None


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

        self.fontSize = self.rect.h
        self.text = utils.getFont(size=36, style='bold').render(text, False,
                                                                utils.BLACK)
        self.textRect = self.text.get_rect()

        while self.textRect.w > self.rect.w:
            self.fontSize -= 2
            self.text = utils.getFont(size=self.fontSize, style='bold').render(text, False, utils.BLACK)
            self.textRect = self.text.get_rect()

    def doClick(self):
        self.action()

    def draw(self, gameWindow):
        centerx = int((self.rect.w - self.textRect.w)/2)
        centery = int((self.rect.h - self.textRect.h)/2)
        self.image.blit(self.text, (centerx, centery))

        Button.draw(self, gameWindow)
