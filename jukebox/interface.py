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
    text = font.render("Tokyo HackerSpace Entertainment System", 1, context['header_text_color'])
    textpos = text.get_rect(centerx=screen.get_width()/2, centery=100)
    screen.blit(text, textpos)

    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN:
            running=False
        elif event.type == MOUSEBUTTONDOWN:
            OnClick(event)

    pygame.display.flip()
