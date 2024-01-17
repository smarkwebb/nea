import pygame
import sys


class ClickButton(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()

        # Custom config
        for arg, par in kwargs.items():
            try:
                setattr(self, arg, float(par))
            except:
                if par == "True":
                    setattr(self, arg, True)
                elif par == "False":
                    setattr(self, arg, False)
                else:
                    setattr(self, arg, par)

        # Default config
        self.surf = pygame.Surface((int(self.height), int(self.width)))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

    def check_pressed(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def interact(self):
        pass

    def update(self, group_handler):
        pass
