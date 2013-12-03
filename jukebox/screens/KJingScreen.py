import os
import pexpect

class KJingScreen:
    def __init__(self, parent):
        self.parent=parent

    def OnEnter(self):
        self.kjing_process = pexpect.spawn("/usr/bin/python /home/pi/Geist/kjing-raspi/client.py")

    def OnDraw(self, screen):
        return
        
    def OnClick(self, event):
        if self.kjing_process!=None:
            self.kjing_process.kill(9)
        self.parent.ChangeScreen("MainScreen")
        return
    
    def OnFlip(self):
        return
        

