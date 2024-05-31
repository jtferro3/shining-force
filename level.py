#!/usr/bin/env python
import sys
import os
from sprites import *

class Level:
    def __init__(self):
        self.dir = os.path.dirname(__file__)
        # load spritesheet image
        self.spritesheet = Spritesheet(os.path.join(self.dir, 'assets', 'characters', SPRITESHEET))
