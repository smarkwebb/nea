from Classes.Platform import Platform
import pygame


class MovingPlatform(Platform):
    def __init__(self, **kwargs):
        Platform.__init__(self, **kwargs)

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

        if self.axis == "x":
            self.direction = "right"
        if self.axis == "y":
            self.direction = "up"

        # Default config
        self.surf = pygame.Surface((self.length, self.width))
        self.surf.fill((self.rgb_r, self.rgb_g, self.rgb_b))
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

    def move(self):
        if self.axis == "x":
            if self.direction == "left":
                if self.rect.left <= self.start:
                    self.direction = "right"
                else:
                    self.rect.x -= self.movement_speed
            if self.direction == "right":
                if self.rect.left >= self.end:
                    self.direction = "left"
                else:
                    self.rect.x += self.movement_speed
        if self.axis == "y":
            if self.direction == "up":
                if self.rect.top <= self.end:
                    self.direction = "down"
                else:
                    self.rect.y -= self.movement_speed
            if self.direction == "down":
                if self.rect.bottom >= self.start:
                    self.direction = "up"
                else:
                    self.rect.y += self.movement_speed

    def update(self, group_handler, score_handler):
        if self.moving:
            self.move()
