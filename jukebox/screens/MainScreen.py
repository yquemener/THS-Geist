import os
from Button import Button
from RenderText import RenderText
import pygame

class MainScreen:
    def __init__(self, parent):
        self.buttons=[]
        self.buttons.append(Button(self, 20,800,400,200, text="Badger help", handler=self.OnClickBadger))
        self.buttons.append(Button(self, 20,550,400,200, text="Shut that music!", handler=self.OnClickShutMusic))
        self.buttons.append(Button(self, 480,800,400,200, text="Network scanning", handler=self.OnClickNMAP))
        self.buttons.append(Button(self, 480,550,400,200, text="KJing", handler=self.OnClickKJing))
        self.buttons.append(Button(self, 920,550,200,450, text="Slideshow", handler=self.OnClickSlideshow))
        self.title = """Tokyo HackerSpace Entertainment System"""
        self.message="""To connect to wifi, use the 'THS' network. 
The password is 38717383
You can also get it by scanning the QR code on the corner.

Once you are connected, you can go to http://192.168.1.42/ to have information
about what's on the network"""
        self.qrpass_surface = pygame.image.load("thspass.png")
        self.parent = parent
        self.font = parent.font
        
    def OnEnter(self):
        return
        
    def OnClick(self, event):
        found=False
        print event.pos
        if(self.parent.INVERT_MOUSE):
            newx = int((1024.0-event.pos[0])*1280.0/1024.0)
            newy = int((768.0-event.pos[1])*1024.0/768.0)
        else:
            newx = event.pos[0]
            newy = event.pos[1]
        epos = (newx, newy)
        print epos
        os.system("killall -9 omxplayer.bin")
        os.system("killall -9 omxplayer")    
        os.system("sudo killall -9 fbi")    

        for b in self.buttons:
            found = found or b.testClick(epos)
        return
        
    def OnDraw(self, screen):
        screen.fill((0,0,0))
        pos = RenderText(screen,self.title, [0,200], {'align-center':"",'bold':"",'font':self.parent.font_big})
        RenderText(screen,self.message, [150,pos[1]+50], {'font':self.parent.font})
        for b in self.buttons:
            b.draw(screen)
        screen.blit(self.qrpass_surface, pygame.Rect(1100,80,87,87))
        return
        
    def OnClickBadger(self, evt):
        try:
            os.system("killall -9 omxplayer.bin")
        except:
            pass
        self.parent.ChangeScreen("BadgersScreen")        
        return 

    def OnClickKJing(self, evt):
        self.parent.ChangeScreen("KJingScreen")        

    def OnClickNMAP(self, evt):
        self.parent.ChangeScreen("NMAPScreen")
    
    def OnClickShutMusic(self,evt):
        os.system("mpc pause")

    def OnClickSlideshow(self,evt):
        self.parent.ChangeScreen("SlideshowScreen")

    def OnFlip(self):
        pygame.display.flip()
       

