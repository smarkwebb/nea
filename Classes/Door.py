import pygame


class Door(pygame.sprite.Sprite):
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
        self.surf = pygame.image.load(
            "./Assets/Sprites/Door CLOSED.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomright=(int(self.x), int(self.y)))
        self.status = "closed"

    def close(self):
        self.surf = pygame.image.load(
            "./Assets/Sprites/Door CLOSED.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomright=(int(self.x), int(self.y)))
        self.status = "closed"

    def open(self):
        self.surf = pygame.image.load(
            "./Assets/Sprites/Door OPEN.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomright=(int(self.x), int(self.y)))
        self.status = "open"

    def update(self, group_handler):
        pass
