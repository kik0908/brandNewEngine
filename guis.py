from engine.gui import GUI, load_image, Label, Image
from engine.initialize_engine import Config
from engine.save_manager import SaveManager

from scene_loader import load_scene
from gui_misc import CloudsController, MedievalButton, MedievalCheckbox

from pygame import Color
import pygame
import sys


class MainMenuGUI:
    @staticmethod
    def start_game():
        load_scene('scenes/scene1.json')
        SaveManager.add_profile('village1', {'seen_tardis': False})
        GUI.clear()
        GameGUI.init()

    @staticmethod
    def load_settings():
        GUI.clear()
        SettingsGUI.init()

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def init():
        clouds_controller = CloudsController('Con', [1, 0])
        CloudsController.generate_clouds(15, clouds_controller)

        GUI.add_element(Image((Config.get_width() // 2, Config.get_height() // 2), pygame.transform.scale(
            load_image('images/main_menu/sky.png'), (Config.get_width(), Config.get_height())
        ), 'sky'))
        GUI.add_element(clouds_controller)

        GUI.add_element(Image((Config.get_width() // 2, 75), load_image('images/main_menu/title_bg.png'), 'title'))
        GUI.add_element(Label(
            (Config.get_width() // 2, 159), 53, 'Untitled game',
            Color('white'), 'fonts/Dot.ttf', 'title_text'
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2, Config.get_height() // 2),
            'Start game', 35, 'start_game', MainMenuGUI.start_game
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2, Config.get_height() // 2 + 75),
            'Settings', 35, 'settings', MainMenuGUI.load_settings
        ))

        GUI.add_element(MedievalButton(
            (Config.get_width() // 2, Config.get_height() // 2 + 150),
            'Exit', 35, 'exit', MainMenuGUI.exit
        ))


class SettingsGUI:
    @staticmethod
    def exit():
        GUI.clear()
        MainMenuGUI.init()

    @staticmethod
    def init():
        GUI.clear()
        GUI.add_element(MedievalCheckbox(
            'checkbox', (Config.get_width() // 2 + 200, Config.get_height() // 2 - 200),
            'Toggle Fullscreen', 29, func=lambda val: Config.set_fullscreen(val)
        ))
        GUI.add_element(MedievalButton(
            (Config.get_width() // 2, Config.get_height() // 2),
            'Exit', 29, 'exit_menu', SettingsGUI.exit
        ))


class GameGUI:
    pause_menu_elements = set()

    @staticmethod
    def exit_in_menu():
        GUI.clear()
        load_scene('scenes/main_menu.json')
        MainMenuGUI.init()

    @staticmethod
    def pause_menu_clear():
        for _ in GameGUI.pause_menu_elements:
            GUI.del_element(_)

        GameGUI.pause_menu_elements.clear()
        GUI.get_element('game_menu').func = GameGUI.create_menu

    @staticmethod
    def create_menu():
        GUI.get_element('game_menu').func = GameGUI.pause_menu_clear

        GUI.add_element(Image((Config.get_width() // 2, Config.get_height() // 2), load_image("images/game_menu_gui/menu.png"), 'background'))
        GameGUI.pause_menu_elements.add('background')

        GUI.add_element(MedievalButton((Config.get_width() // 2, Config.get_height() // 2 - 50), 'Resume', 35, 'resume', GameGUI.pause_menu_clear))
        GameGUI.pause_menu_elements.add('resume')

        GUI.add_element(MedievalButton((Config.get_width() // 2, Config.get_height() // 2 + 20), 'Exit in menu', 33, 'exit', GameGUI.exit_in_menu))
        GameGUI.pause_menu_elements.add('exit')

        GUI.add_element(MedievalButton((Config.get_width() // 2, Config.get_height() // 2 + 90), 'Exit in desktop', 29, 'exit_in_desktop', MainMenuGUI.exit))
        GameGUI.pause_menu_elements.add('exit_in_desktop')

    @staticmethod
    def init():
        GUI.add_element(MedievalButton((Config.get_width() // 2, Config.get_height() - 35), 'Menu', 35, 'game_menu', GameGUI.create_menu))
