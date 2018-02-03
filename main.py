import engine.initialize_engine

import pygame
import sys

from engine.game_objects import GameObject
from engine.base_components import ImageComponent
from user_components import ControllerComponent, ShooterComponent, AnimationHuman
from engine.scene_manager import scene_manager
from engine.input_manager import input_manager

scene_manager.rename_scene('default_scene', 'scene1')
scene = scene_manager.current_scene
input_manager.add_axis('Rotation', {
    pygame.K_q: -1,
    pygame.K_e: 1,
})

player = GameObject()
player.add_component(ControllerComponent(15, player))
player.add_component(ShooterComponent(50, 3, 0.15, player))
player.add_component(ImageComponent('images/player1.png', False, player))
player.add_component(AnimationHuman([['images/player1.png', 'images/player4.png'],
                                     ['images/player2.png', 'images/player3.png'],
                                     ['images/player1.png']], 10, player))#[Анимация состояния покоя, ходьбы, стрельбы], скорость



for y in range(-8, 8):
    for x in range(-8, 8):
        bg = GameObject(x * 512, y * 512)
        bg.add_component(ImageComponent('images/bg.png', True, bg))

        scene.add_object(bg)

scene.add_object(player)
scene.add_object(stena)



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