#!/usr/bin/env python3
import os
import sys
import pygame

# allow running as script (python main.py) or module (python -m chess.main)
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    __package__ = "chess"
from .engine import GameState
from .gui import PygameGUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Chess with AI")

    state = GameState()
    gui = PygameGUI(screen, state)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                gui.handle_event(event)

        gui.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
