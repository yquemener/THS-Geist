import os
from pyomxplayer import *
import pexpect
from pymouse import PyMouseEvent


class ClickInterceptor(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
	self.stop()
	return

class BadgersScreen:
    def __init__(self, parent):
        self.parent=parent

    def OnEnter(self):
        try:
            self.mplayer_process = pexpect.spawn("/usr/bin/mplayer -fs /home/hacker/Videos/Badgers.mp4")
        except:
            pass
	c = ClickInterceptor()
	c.run()
        return

    def OnDraw(self, screen):
        return
        
    def OnClick(self, event):
        os.system("killall -9 mplayer")
        self.parent.ChangeScreen("MainScreen")
        return
    
    def OnFlip(self):
        return
        

