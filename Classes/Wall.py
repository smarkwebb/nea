import pygame


class Wall(pygame.sprite.Sprite):
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
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((self.rgb_r, self.rgb_g, self.rgb_g))
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

    def update(self, group_handler):
        pass
