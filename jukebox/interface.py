#!/usr/bin/python

import pygame
import os
import sys
from pyomxplayer import *

from pygame.locals import *

# Init
fullscreen = True

if len(sys.argv)>1 and sys.argv[1]=="nofs":
    fullscreen=False

pygame.init()
if fullscreen:
    screen = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((1280, 1024))

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 50)
font.set_bold(False)

# Handlers

def RenderText(screen, text, xy=[0,0], style={}):
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
            xy[0]=ts.get_rect(centerx=screen.get_width()/2)[0]
        else:
            xy[0] = 0
        screen.blit(ts, xy)
        xy[1] += ts.get_height()
    return xy
def OnClick(event):
    context['header_text_color'][0] = 255-context['header_text_color'][0] 
    try:
        omx = OMXPlayer('/home/pi/Badgers.mp4')
    except:
	pass
    return 

# Mainloop

context = {
        'header_text_color':[255,255,255]
        }

title = """Tokyo HackerSpace Entertainment System"""
 
message="""My IP address is 192.168.1.20
I am a MPD daemon. Yeah baby }:) 
You can access it through the default port (6600) with clients like gmpc.
 
You can ssh me as user 'pi' with the password 'raspberry'.
To make me play a video, ssh me and use the command line "omxplayer <mp4 file>". 
There are some files in Videos/ you are welcomed to add more.
 
Touch this screen if you need some badger support."""
running = True
while running:
    clock.tick(60)
    pos = RenderText(screen,title, [0,200], {'align-center':"",'bold':"",'font':font_big})
    RenderText(screen,message, [pos[0],pos[1]+200])


    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN:
            running=False
        elif event.type == MOUSEBUTTONDOWN:
            OnClick(event)

    pygame.display.flip()
