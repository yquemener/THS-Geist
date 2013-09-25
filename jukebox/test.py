#!/usr/bin/python

import subprocess
import sys
from pyomxplayer import *

try:
  omx = OMXPlayer('/home/pi/Badgers.mp4')
except:
  pass
