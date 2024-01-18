import pygame


class Key(pygame.sprite.Sprite):
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
            "./Assets/Sprites/Key.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

        self.collected = False

    def check_player(self, group_handler):
        if group_handler.players:
            if pygame.sprite.groupcollide(group_handler.keys, group_handler.players, False, False):
                for player in group_handler.players:
                    if self.rect.colliderect(player.rect):
                        self.collected = True
                        player.keys_collected += 1

    def follow_player(self, group_handler):
        for player in group_handler.players:
            self.rect.y = player.rect.y

            if player.direction == "right":
                self.rect.x = player.rect.x - 50
            if player.direction == "left":
                self.rect.x = player.rect.x + 50

    def update(self, group_handler, score_handler):
        self.check_player(group_handler)

        if self.collected:
            self.follow_player(group_handler)
