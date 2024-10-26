import pygame


class Enemy(pygame.sprite.Sprite):
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
            "./Assets/Sprites/Enemy LEFT.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

        self.direction = "left"
        self.gravity = 0
        self.invincible = False
        self.last_damaged = pygame.time.get_ticks()
        self.on_platform = False

    def apply_gravity(self):
        self.gravity -= 1
        self.rect.y -= self.gravity

        if self.rect.bottom >= 720:
            self.rect.bottom = 720
            self.gravity = 0

    def attack(self, target):
        if target.invincible == False:
            target.health -= self.attack_damage
            target.last_damaged = pygame.time.get_ticks()
            target.invincible = True

    def check_health(self, group_handler):
        if self.health <= 0:
            self.kill()
            if group_handler.health_bars:
                for health_bar in group_handler.health_bars:
                    if self.object_id == health_bar.object_id:
                        health_bar.kill()

    def check_invincibility(self):
        if self.invincible == True:
            if pygame.time.get_ticks() - self.last_damaged > 1000:
                self.invincible = False

    def check_platform(self, group_handler):
        if group_handler.enemies and group_handler.platforms:
            if pygame.sprite.groupcollide(group_handler.enemies, group_handler.platforms, False, False):
                for platform in group_handler.platforms:
                    if self.rect.colliderect(platform.rect):
                        self.rect.bottom = platform.rect.y
                        self.gravity = 0
                        self.on_platform = True
            else:
                self.on_platform = False

    def check_player(self, group_handler):
        if group_handler.enemies and group_handler.players:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.enemies, False, False):
                for player in group_handler.players:
                    if self.rect.colliderect(player.rect):
                        self.attack(player)

    def move(self):
        if self.direction == "left":
            if self.rect.left <= 0:
                self.direction = "right"
                self.surf = pygame.image.load("./Assets/Sprites/Enemy RIGHT.png")
            else:
                self.rect.x -= self.movement_speed
        if self.direction == "right":
            if self.rect.right >= 1280:
                self.direction = "left"
                self.surf = pygame.image.load("./Assets/Sprites/Enemy LEFT.png")
            else:
                self.rect.x += self.movement_speed

    def update(self, group_handler, score_handler):
        self.move()
        self.apply_gravity()
        self.check_health(group_handler)
        self.check_invincibility()
        self.check_platform(group_handler)
        self.check_player(group_handler)
