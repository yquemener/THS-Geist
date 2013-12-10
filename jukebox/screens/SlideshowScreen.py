import os
import pexpect

class SlideshowScreen:
    def __init__(self, parent):
        self.parent=parent

    def OnEnter(self):
        self.bg_process = pexpect.spawn("/bin/bash /home/pi/Geist/jukebox/slideshow")

    def OnDraw(self, screen):
        return
        
    def OnClick(self, event):
        if self.bg_process!=None:
            self.bg_process.kill(9)
        #os.system("killall fbi")
        self.parent.ChangeScreen("MainScreen")
        return
    
    def OnFlip(self):
        return
        

