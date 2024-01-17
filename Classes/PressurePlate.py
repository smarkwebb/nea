import pygame


class PressurePlate(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()

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
            "./Assets/Sprites/Pressure Plate UP.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

        self.state = 0

    def check_entities(self, group_handler):
        if group_handler.blocks:
            if pygame.sprite.groupcollide(group_handler.pressure_plates, group_handler.blocks, False, False):
                for block in group_handler.blocks:
                    if self.rect.colliderect(block.rect):
                        self.state = 1
                        self.surf = pygame.image.load(
                            "./Assets/Sprites/Pressure Plate DOWN.png").convert_alpha()
                        self.rect = self.surf.get_rect(
                            bottomleft=(self.x, self.y))
            else:
                if group_handler.players:
                    if pygame.sprite.groupcollide(group_handler.pressure_plates, group_handler.players, False, False):
                        for player in group_handler.players:
                            if self.rect.colliderect(player.rect):
                                self.state = 1
                                self.surf = pygame.image.load(
                                    "./Assets/Sprites/Pressure Plate DOWN.png").convert_alpha()
                                self.rect = self.surf.get_rect(
                                    bottomleft=(self.x, self.y))
                    else:
                        self.state = 0
                        self.surf = pygame.image.load(
                            "./Assets/Sprites/Pressure Plate UP.png").convert_alpha()
                        self.rect = self.surf.get_rect(
                            bottomleft=(self.x, self.y))

    def interact(self, group_handler):
        if "block" in self.link_id:
            if group_handler.blocks:
                for block in group_handler.blocks:
                    if self.link_id == block.object_id:
                        if self.function == "spawn":
                            if self.state == 1:
                                block.suspended = False
                                block.show()

        if "door" in self.link_id:
            if group_handler.doors:
                for door in group_handler.doors:
                    if self.link_id == door.object_id:
                        if self.function == "open":
                            if self.state == 1:
                                door.open()
                            else:
                                door.close()

    def update(self, group_handler):
        self.check_entities(group_handler)
        self.interact(group_handler)
