#!/usr/bin/python

import pygame
import os
import sys
from pyomxplayer import *
import pygame
from pygame.locals import *
import random
from screens.RenderText import RenderText
from screens.Button import Button
from screens import *
import screens




class App:
    def __init__(self):

        self.SHOW_MOUSE=False
        self.INVERT_MOUSE=True


        self.SHOW_MOUSE=True
        self.INVERT_MOUSE=False



        # Init
        self.fullscreen = True

        if len(sys.argv)>1 and sys.argv[1]=="nofs":
            self.fullscreen=False

        pygame.init()
        if self.fullscreen:
            self.screen = self.InitFramebuffer()
            #screen = pygame.display.set_mode((1280, 1024), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1280, 1024))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_big = pygame.font.Font(None, 50)
        self.font.set_bold(False)
        pygame.mouse.set_visible(self.SHOW_MOUSE)
        #pygame.event.set_grab(True)
        self.buttons=[]
        self.kjing_process = None
        self.qrpass_surface = pygame.image.load("thspass.png")

        self.all_screens=dict()
        for s in screens.__all__:
            self.all_screens[s]=eval(s+"."+s+"(self)")
            print s
        self.current_screen=self.all_screens["MainScreen"]

    def InitFramebuffer(self):
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

    def ChangeScreen(self, newscreen):
        self.current_screen = self.all_screens[newscreen]
        self.current_screen.OnEnter()
        return

    def MainLoop(self):
        running = True
        dbg = 10

        while running:
            self.clock.tick(60)
            dbg = (dbg+10)%256
            self.current_screen.OnDraw(self.screen)
            event = pygame.event.poll()
            if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                running=False
            elif event.type == MOUSEBUTTONDOWN:
                self.current_screen.OnClick(event)
            pygame.draw.rect(self.screen, (dbg,dbg,dbg), Rect(0,0,100,10),0)
            self.current_screen.OnFlip()





App().MainLoop()
