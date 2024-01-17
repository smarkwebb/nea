from Classes.PressurePlate import PressurePlate
import pygame


class BigPressurePlate(PressurePlate):
    def __init__(self, **kwargs):
        PressurePlate.__init__(self, **kwargs)

        # Custom config
        for arg, par in kwargs.items():
            try:
                setattr(self, arg, float(par))
            except:
                if par == "True":
                    setattr(self, arg, True)
                if par == "False":
                    setattr(self, arg, False)
                else:
                    setattr(self, arg, par)

        # Default config
        self.surf = pygame.image.load(
            "./Assets/Sprites/Big Pressure Plate UP.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

        self.state = 0

    def check_entities(self, group_handler):
        if group_handler.blocks:
            if pygame.sprite.groupcollide(group_handler.big_pressure_plates, group_handler.blocks, False, False):
                for block in group_handler.blocks:
                    if self.rect.colliderect(block.rect):
                        if block.size > 50:
                            self.state = 1
                            self.surf = pygame.image.load(
                                "./Assets/Sprites/Big Pressure Plate DOWN.png").convert_alpha()
                            self.rect = self.surf.get_rect(
                                bottomleft=(self.x, self.y))
            else:
                self.state = 0
                self.surf = pygame.image.load(
                    "./Assets/Sprites/Big Pressure Plate UP.png").convert_alpha()
                self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))
