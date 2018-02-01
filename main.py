import engine.initialize_engine

from engine.scene_manager import scene_manager
from engine.input_manager import input_manager

import pygame
import sys

from engine.game_objects import GameObject
from engine.base_components import ImageComponent
from user_components import ControllerComponent, ShooterComponent, RigidBody

scene = scene_manager.current_scene

player = GameObject()
player.add_component(RigidBody(player))
player.add_component(ControllerComponent(15, player))
player.add_component(ShooterComponent(50, 3, 0.15, player))
player.add_component(ImageComponent('images/player.png', player))

wall = GameObject(500, 500)
wall.add_component(RigidBody(wall))
wall.add_component(ImageComponent('images/wall.png', wall))
obj = GameObject()
obj.add_component(ControllerComponent(15, obj))
obj.add_component(ShooterComponent(50, 3, 0.15, obj))
obj.add_component(ImageComponent('images/player.png', obj))

for y in range(-8, 8):
    for x in range(-8, 8):
        bg = GameObject(x * 512, y * 512)
        bg.add_component(ImageComponent('images/bg.png', bg))

        scene.add_object(bg)

scene.add_object(player)
scene.add_object(wall)

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    input_manager.update()

    for event in input_manager.get_events():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    scene.update()
    scene.render()

    pygame.display.flip()
