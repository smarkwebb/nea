import pygame


class HealthBar(pygame.sprite.Sprite):
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
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(topleft=(0, 0))

    def update(self, group_handler):
        if self.link_id == "player":
            if group_handler.players:
                for player in group_handler.players:
                    self.surf = pygame.Surface((player.health * 2, 50))
                    self.surf.fill((255, 0, 0))
                    self.rect = self.surf.get_rect(
                        topleft=(self.x, self.y))
        else:
            if group_handler.enemies:
                for enemy in group_handler.enemies:
                    if self.object_id == enemy.object_id:
                        self.surf = pygame.Surface((enemy.health / 1.5, 10))
                        self.surf.fill((255, 0, 0))
                        self.rect = self.surf.get_rect(
                            center=(int(enemy.rect.x)+15, int(enemy.rect.y)-20))
