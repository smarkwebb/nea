import pygame


class Button(pygame.sprite.Sprite):
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
            "./Assets/Sprites/Button.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

        self.last_pressed = pygame.time.get_ticks()

    def press(self, group_handler):
        if pygame.time.get_ticks() - self.last_pressed > 1000:
            self.last_pressed = pygame.time.get_ticks()

            if "block" in self.link_id:
                if group_handler.blocks:
                    for block in group_handler.blocks:
                        if self.link_id == block.object_id:
                            if self.function == "spawn":
                                block.suspended = False
                                block.show()

            if "door" in self.link_id:
                if group_handler.doors:
                    for door in group_handler.doors:
                        if self.link_id == door.object_id:
                            if self.function == "open":
                                door.open()

            if "moving_platform" in self.link_id:
                if group_handler.moving_platforms:
                    for platform in group_handler.moving_platforms:
                        if self.link_id == platform.object_id:
                            if self.function == "move":
                                platform.moving = True

            if "player" in self.link_id:
                if group_handler.players:
                    for player in group_handler.players:
                        if self.link_id == player.object_id:
                            if self.function == "scale_up":
                                new_scale = player.max_scale
                                player.change_scale(new_scale)
                            if self.function == "scale_down":
                                new_scale = player.min_scale
                                player.change_scale(new_scale)

    def update(self, group_handler):
        pass
