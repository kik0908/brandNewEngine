import pygame
from engine.initialize_engine import width, height
from random import randint


def load_image(path):
    return pygame.image.load(path).convert_alpha()


class Label:
    def __init__(self, pos, size, text, front_color, path_font, name):
        self.pos = pos
        self.size = size
        self.text = text
        self.font_color = front_color
        self.name = name

        self.font = pygame.font.Font(path_font, size)

    def render(self, surface):
        rendered_text = self.font.render(self.text, 1, self.font_color)
        rendered_rect = rendered_text.get_rect(center=self.pos)
        surface.blit(rendered_text, rendered_rect)


class Button:
    def __init__(self, pos, image_states, text, font_path, text_color, text_size, name, func=lambda: None):
        self.normal_image = load_image(image_states['normal'])
        self.hover_image = load_image(image_states['hovered'])
        self.click_image = load_image(image_states['clicked'])

        self.text = text
        self.font = pygame.font.Font(font_path, text_size)
        self.text_color = pygame.Color(text_color)

        self.pos = pos

        self.image = self.normal_image

        self.name = name
        self.func = func

        self.states = {
            'hovered': False,
            'clicked': False,
            'after_click': False
        }

    def update(self, *args):
        if self.states['clicked']:
            self.states['clicked'] = False
            self.image = self.click_image
            self.states['after_click'] = True
        elif self.states['after_click']:
            if self.states['hovered']:
                self.image = self.click_image
            else:
                self.states['after_click'] = False

        elif self.states['hovered']:
            self.image = self.hover_image

        else:
            self.image = self.normal_image

    def render(self, surface):
        surface.blit(self.image, self.image.get_rect(center=self.pos))
        text = self.font.render(self.text, 4, self.text_color)
        surface.blit(text, text.get_rect(center=self.pos))

    def apply_event(self, event):
        self.states['hovered'] = self.image.get_rect(center=self.pos).collidepoint(*pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.states['hovered']:
                    self.states['clicked'] = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.states['hovered'] and self.states['after_click']:
                    self.states['after_click'] = False
                    self.func()


class Image:
    def __init__(self, pos, image, name):
        self.image = image

        self.name = name
        self.size = self.image.get_size()
        self.rect = pygame.Rect(pos[0], pos[1], self.size[0], self.size[1])
        self.rect = self.image.get_rect(center=pos)
        self.const_rect = self.rect.copy()
        self.const_rect.x = -self.size[0]

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, x, y):
        self.rect[0] += x
        self.rect[1] += y

    def get_pos(self):
        return self.rect[0], self.rect[1]

    def set_const_pos(self):
        self.const_rect.y = randint(0, height - self.size[1])
        self.rect = self.const_rect.copy()


class GUI:
    elements = []

    @staticmethod
    def add_element(element):
        if all(map(lambda elem: elem.name != element.name, GUI.elements)):
            GUI.elements.append(element)
            return element

    @staticmethod
    def get_element(name):
        for elem in GUI.elements:
            if elem.name == name:
                return elem

    @staticmethod
    def render():
        for element in GUI.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(pygame.display.get_surface())

    @staticmethod
    def update():
        for element in GUI.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    @staticmethod
    def apply_event(event):
        for element in GUI.elements:
            get_event = getattr(element, "apply_event", None)
            if callable(get_event):
                element.apply_event(event)

    @staticmethod
    def del_element(name):
        for element in GUI.elements:
            if element.name == name:
                GUI.elements.remove(element)

    @staticmethod
    def clear():
        GUI.elements = []
