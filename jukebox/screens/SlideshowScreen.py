import os
from pyomxplayer import *

class SlideshowScreen:
    def __init__(self, parent):
        self.parent=parent

    def OnEnter(self):
        os.system("fbi -T1 -t10 -a -u /home/pi/Pictures/*/*/* /home/pi/Pictures/*/*")

    def OnDraw(self, screen):
        return
        
    def OnClick(self, event):
        os.system("killall fbi")
        self.parent.ChangeScreen("MainScreen")
        return
    
    def OnFlip(self):
        return
        

