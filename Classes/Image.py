import pygame


class Image(pygame.sprite.Sprite):
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
        self.surf = pygame.Surface((0, 0))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

    def show(self):
        self.surf = pygame.image.load(self.path).convert_alpha()
        self.surf = pygame.transform.scale_by(self.surf, float(self.scale))
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

    def hide(self):
        self.surf = pygame.Surface((0, 0))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

    def update(self, group_handler, score_handler):
        pass
