#!/usr/bin/python

import pygame
import os
from pyomxplayer import *

from pygame.locals import *

# Init
fullscreen = False

pygame.init()
if fullscreen:
    screen = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((1280, 1024))

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


# Handlers

def TextRendering(screen, text, xy=[0,0]):
    for l in text.split("\n"):
        ts = font.render(l, 1, (255,255,255))
        screen.blit(text, xy)
        xy[1] += ts.get_height()

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

running = True
while running:
    clock.tick(60)
    RenderText(screen,"Tokyo HackerSpace Entertainment System\nDon't try this at home: this is what the hackerspace is for!")

    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN:
            running=False
        elif event.type == MOUSEBUTTONDOWN:
            OnClick(event)

    pygame.display.flip()
