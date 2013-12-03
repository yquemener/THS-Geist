import os
from pyomxplayer import *

class BadgersScreen:
    def __init__(self, parent):
        self.parent=parent

    def OnEnter(self):
        try:
            self.omx = OMXPlayer('/home/pi/Badgers.mp4')
        except:
            pass
        return

    def OnDraw(self, screen):
        return
        
    def OnClick(self, event):
        os.system("sudo killall -9 omxplayer")
        os.system("sudo killall -9 omxplayer.bin")
        self.parent.ChangeScreen("MainScreen")
        return
    
    def OnFlip(self):
        return
        

