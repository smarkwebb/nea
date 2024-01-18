import pygame


class Switch(pygame.sprite.Sprite):
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
            "./Assets/Sprites/Switch OFF.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

        self.last_pressed = pygame.time.get_ticks()
        self.state = 0

    def flip(self, group_handler):
        if pygame.time.get_ticks() - self.last_pressed > 1000:
            self.toggle_state()
            self.last_pressed = pygame.time.get_ticks()

            if "door" in self.link_id:
                if group_handler.doors:
                    for door in group_handler.doors:
                        if self.link_id == door.object_id:
                            if self.state == 1:
                                door.open()
                            else:
                                door.close()

    def toggle_state(self):
        if self.state == 0:
            self.state = 1
            self.surf = pygame.image.load(
                "./Assets/Sprites/Switch ON.png").convert_alpha()
        else:
            self.state = 0
            self.surf = pygame.image.load(
                "./Assets/Sprites/Switch OFF.png").convert_alpha()

    def update(self, group_handler, score_handler):
        pass
