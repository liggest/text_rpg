from __future__ import annotations

from text_rpg.util import Singleton
from text_rpg.event import MultipleEvent

class Game(Singleton):

    def __init__(self):
        self.on_init = MultipleEvent()
        self.on_exit = MultipleEvent()

    def init(self):
        self.on_init()

    def exit(self):
        self.on_exit()
