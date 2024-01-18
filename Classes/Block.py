import pygame


class Block(pygame.sprite.Sprite):
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
        self.surf = pygame.Surface((int(self.size), int(self.size)))
        self.surf.fill((0, 0, 0))
        self.size = self.size
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

        self.gravity = 0

    def apply_gravity(self):
        self.gravity -= 1
        self.rect.y -= self.gravity

        if self.rect.bottom >= 720:
            self.rect.bottom = 720
            self.gravity = 0

    def check_platform(self, group_handler):
        if group_handler.platforms:
            for platform in group_handler.platforms:
                if self.rect.colliderect(platform.rect):
                    self.rect.bottom = platform.rect.y
                    self.gravity = 0

    def hide(self):
        self.hidden = True
        self.surf = pygame.Surface((0, 0))

    def reset_position(self):
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

    def show(self):
        self.hidden = False
        self.surf = pygame.Surface((int(self.size), int(self.size)))

    def update(self, group_handler, score_handler):
        self.check_platform(group_handler)

        if self.hidden:
            self.hide()

        if not self.suspended:
            self.apply_gravity()
