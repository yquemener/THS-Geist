import pygame


class Button():
    def __init__(self, parent, x,y,w,h, text="", handler=None):
        self.pos = (x,y)
        self.size=(w,h)
        self.OnClick = handler
        self.text=text
        self.bgcolor=(5,5,5)
        self.fgcolor=(0,0,255)
        self.parent = parent

    def draw(self, screen):
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.bgcolor, rect, 0)
        pygame.draw.rect(screen, self.fgcolor, rect, 1)
        rect.inflate(-2,-2)
        pygame.draw.rect(screen, self.fgcolor, rect, 1)
        ts = self.parent.font.render(self.text, 1, self.fgcolor)
        xy=[0,0]
        xy[0]=ts.get_rect(centerx=rect.x+rect.width/2)[0]
        xy[1] = rect.y + rect.height/2
        screen.blit(ts, xy)

    def testClick(self, event):
        x = event[0]
        y = event[1]
        if x>self.pos[0] and x<self.pos[0]+self.size[0] and y>self.pos[1] and y<self.pos[1]+self.size[1]:
            self.OnClick(event)
            print self.text +" clicked"
            return True
        return False

