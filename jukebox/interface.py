#!/usr/bin/python

import pygame
import os
import sys
from pyomxplayer import *
import pygame
from pygame.locals import *
import random
import pexpect

SHOW_MOUSE=False
INVERT_MOUSE=True

# Debug settings:
"""SHOW_MOUSE=True
INVERT_MOUSE=False"""


class Button():
    def __init__(self, x,y,w,h, text="", handler=None):
        self.pos = (x,y)
        self.size=(w,h)
        self.OnClick = handler
        self.text=text
        self.bgcolor=(5,5,5)
        self.fgcolor=(0,0,255)

    def draw(self, screen):
        rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, self.bgcolor, rect, 0)
        pygame.draw.rect(screen, self.fgcolor, rect, 1)
        rect.inflate(-2,-2)
        """rect.x += 2
        rect.y += 2
        rect.width -= 2
        rect.height -= 2"""
        pygame.draw.rect(screen, self.fgcolor, rect, 1)
        ts = font.render(self.text, 1, self.fgcolor)
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

def NmapParser(s):
    hosts={}
    host=None
    for l in s.split("\n"):
        if l.startswith("Nmap scan report"):
            host = l.split(" ")[-1].rstrip(")").lstrip("(")
            hosts[host]=dict()

        if l.startswith("MAC Address"):
            mac = l.split(" ")[2]
            brand = " ".join(l.split(" ")[3:]).rstrip(")").lstrip("(")
            hosts[host]["mac"] = mac
            hosts[host]["brand"] = brand
    for h in hosts.keys():
        for k in net_knowledge:
            if k[0]=='ip':
                if k[1]==h:
                    hosts[h]['id_name']=k[2]
                    hosts[h]['id_text']=k[3]
            if k[0]=='mac' and hosts[h].has_key("mac"):
                if k[1]==hosts[h]["mac"]:
                    hosts[h]['id_name']=k[2]
                    hosts[h]['id_text']=k[3]
    with open("log2","w") as l:
        l.write(str(net_knowledge))
        l.write('\n')
        l.write(str(hosts))
    return hosts

def InitFramebuffer():
    screen = None;

    "Ininitializes a new pygame screen using the framebuffer"
    # Based on "Python GUI in Linux frame buffer"
    # http://www.karoltomala.com/blog/?p=679
    disp_no = os.getenv("DISPLAY")
    if disp_no:
        print "I'm running under X display = {0}".format(disp_no)

    # Check which frame buffer drivers are available
    # Start with fbcon since directfb hangs with composite output
    drivers = ['fbcon', 'directfb', 'svgalib']
    found = False
    for driver in drivers:
        # Make sure that SDL_VIDEODRIVER is set
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        try:
            pygame.display.init()
        except pygame.error:
            print 'Driver: {0} failed.'.format(driver)
            continue
        found = True
        break

    if not found:
        raise Exception('No suitable video driver found!')

    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print "Framebuffer size: %d x %d" % (size[0], size[1])
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    return screen


def RenderText(screen, text, xy=[0,0], style={}):
    _xy=xy
    if "font" in style.keys():
        _font = style["font"]
    else:
        _font = font
    if "bold" in style.keys():
        _font.set_bold(True)
    else:
        _font.set_bold(False)

    for l in text.split("\n"):
        ts = _font.render(l, 1, (255,255,255))
        if 'align-center' in style.keys():
            _xy[0]=ts.get_rect(centerx=screen.get_width()/2)[0]
        else:
            _xy[0] = xy[0]
        screen.blit(ts, xy)
        _xy[1] += ts.get_height()
    return _xy

# Init
fullscreen = True

if len(sys.argv)>1 and sys.argv[1]=="nofs":
    fullscreen=False

pygame.init()
if fullscreen:
    screen = InitFramebuffer()
    #screen = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((1280, 1024))

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 50)
font.set_bold(False)
pygame.mouse.set_visible(SHOW_MOUSE)
#pygame.event.set_grab(True)
buttons=[]
net_knowledge=[]
kjing_process = None

with open("knownmachines","r") as f:
    for l in f:
        print l
        arr=l.split(";")
        print arr
        net_knowledge.append((arr[0].rstrip().lstrip(), arr[1].rstrip().lstrip(), arr[2].rstrip().lstrip(),arr[3].rstrip().lstrip()))
        

# Handlers

def OnClickMainScreen(event):
    found=False
    print event.pos
    if(INVERT_MOUSE):
        newx = int((1024.0-event.pos[0])*1280.0/1024.0)
        newy = int((768.0-event.pos[1])*1024.0/768.0)
    else:
        newx = event.pos[0]
        newy = event.pos[1]
    epos = (newx, newy)
    print epos
    for b in buttons:
        found = found or b.testClick(epos)
    if not found:
        os.system("killall -9 omxplayer.bin")
        os.system("killall -9 omxplayer")

def OnClickBadger(evt):
    try:
        os.system("killall -9 omxplayer.bin")
        omx = OMXPlayer('/home/pi/Badgers.mp4')
    except:
        pass
    return 

def OnClickKJing(evt):
    global kjing_process
    print "CLICK KJING"
    
    if(context["current_screen"]["name"]=="kjing"):
        context["current_screen"]["name"]="main"
        context['current_screen']['OnClick']=OnClickMainScreen
        context['current_screen']['OnDraw']=DrawMainScreen
        context['current_screen']['OnFlip']=pygame.display.flip
        #os.system("sudo killall ./kjing")
        if kjing_process!=None:
            kjing_process.kill(9)
        return
    #os.system("./kjing &")
    context['current_screen']['name']="kjing"
    context['current_screen']['OnClick']=OnClickKJing
    context['current_screen']['OnDraw']=lambda x:0
    context['current_screen']['OnFlip']=lambda:0
    kjing_process = pexpect.spawn("/usr/bin/python /home/pi/Geist/kjing-raspi/client.py")
    return

def OnClickNMAP(evt):
    print "CLICK NMAP"
    if(context["current_screen"]["name"]=="nmap"):
        context["current_screen"]["name"]="main"
        context['current_screen']['OnClick']=OnClickMainScreen
        context['current_screen']['OnDraw']=DrawMainScreen
        context['current_screen']['OnFlip']=pygame.display.flip
        os.system("sudo killall nmap")
        os.system("sudo rm log")
        return
    context['current_screen']['name']="nmap"
    context['current_screen']['OnClick']=OnClickNMAP
    context['current_screen']['OnDraw']=DrawNMAP
    context['current_screen']['OnFlip']=pygame.display.flip
    return

def DrawNMAP(screen):
    screen.fill((0,0,0))
    pos = RenderText(screen,"NMAP results", [0,200], {'align-center':"",'bold':"",'font':font_big})
    try:
        o=open("logdone","r")
        d=NmapParser(o.read())
        message=""
        # print d
        lst = d.keys()
        lst.sort(key=lambda x:int(x.split(".")[-1]))
        
        for host in lst:
            message+=host+"   "
            if d[host].has_key("id_text") and len(d[host]["id_text"])>0:
                message+=d[host]["id_text"]
            elif d[host].has_key("id_name"):
                #message+=random.choice(("smells like ","feels like ", "looks like ", ""))+d[host]["id_name"]
                message+=d[host]["id_name"]
            elif d[host].has_key("brand"):
                message+=d[host]['brand']
            else:
                message += "unknown"
            message+="\n"
        RenderText(screen, message, [150,pos[1]+50])
    except IOError:
        pass
    try:
        o=open("log","r")
    except:
        print "Resuming scanning"
        os.system("touch log")
        os.system("sudo ./scan_net &")
    return

def DrawMainScreen(screen):
    screen.fill((0,0,0))
    pos = RenderText(screen,title, [0,200], {'align-center':"",'bold':"",'font':font_big})
    RenderText(screen,message, [150,pos[1]+50])
    for b in buttons:
        b.draw(screen)
    return

# Mainloop
context = {
        'header_text_color':[255,255,255],
        'current_screen':{'OnDraw':None, 'OnClick':None, 'name':"init"}
        }

title = """Tokyo HackerSpace Entertainment System"""
 
message="""My IP address is 192.168.1.20
I am a MPD daemon. Yeah baby }:) 
You can access it through the default port (6600) with clients like gmpc.
 
You can ssh me as user 'pi' with the password 'raspberry'.
To make me play a video, ssh me and use the command line "omxplayer <mp4 file>". 
There are some files in Videos/ you are welcomed to add more."""
running = True

buttons.append(Button(20,800,400,200, text="Badger help", handler=OnClickBadger))
buttons.append(Button(480,800,400,200, text="Network scanning", handler=OnClickNMAP))
buttons.append(Button(480,550,400,200, text="KJing", handler=OnClickKJing))

context['current_screen']['OnClick']=OnClickMainScreen
context['current_screen']['OnDraw']=DrawMainScreen
context['current_screen']['OnFlip']=pygame.display.flip
context['current_screen']['name']="main"
dbg = 10



while running:
    clock.tick(60)
    dbg = (dbg+10)%256
    context['current_screen']['OnDraw'](screen)
    event = pygame.event.poll()
    if event.type == QUIT or event.type == KEYDOWN:
        running=False
    elif event.type == MOUSEBUTTONDOWN:
        context['current_screen']['OnClick'](event)
    pygame.draw.rect(screen, (dbg,dbg,dbg), Rect(0,0,100,10),0)
    context['current_screen']['OnFlip']()






