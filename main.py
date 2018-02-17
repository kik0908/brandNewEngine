import engine.initialize_engine
from engine.scene_manager import scene_manager

import pygame
import sys

from scene_loader import load_scene
from engine.input_manager import input_manager
from engine.gui import gui, Button


load_scene('scenes/scene1.json')

gui.add_element(
    Button((200, 50), {
        'normal': 'images/normal.png',
        'hovered':'images/hovered.png',
        'clicked': 'images/clicked.png'
    }, 'but1', lambda: print('Pressed button'))
)

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    input_manager.update()

    for event in input_manager.get_events():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

        gui.apply_event(event)

    scene_manager.current_scene.update()
    scene_manager.current_scene.render()

    gui.update()
    gui.render()

    pygame.display.flip()
