import pygame

class Btn:
    def __init__(self, x, y, width, height, text=None, color=(73, 73, 73), hiColor= (189, 189, 189), function=None, params=None):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.color = color
        self.function = function
        self.params = params
        self.highlighted = False
    
    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False
    
    def draw(self, window):
        self.image.fill(self.color)
        if self.text:
            self.drawText(self.text)
        window.blit(self.image, self.pos)

    def drawText(self, text):
        font = pygame.font.SysFont("arial", 20, bold=1)
        text = font.render(text, False, (255,255,255))
        width, height = text.get_size()
        x = (self.width - width)//2 
        y = (self.height - height)//2
        self.image.blit(text, (x,y))