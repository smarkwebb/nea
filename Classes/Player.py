import pygame


class Player(pygame.sprite.Sprite):
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
        file = open("./Data/Players/CurrentCharacter.txt", "r")
        character = file.readlines()
        character = str(character[0])
        self.surf = pygame.image.load(
            f"./Assets/Sprites/{character}.png").convert_alpha()
        self.rect = self.surf.get_rect(bottomleft=(self.x, self.y))

        self.default_size = self.size
        self.direction = "right"
        self.gravity = 0
        self.keys_collected = 0
        self.last_damaged = pygame.time.get_ticks()
        self.on_block = False
        self.on_platform = False

    def apply_gravity(self):
        self.gravity -= 1
        self.rect.y -= self.gravity

    def change_scale(self, new_scale):
        if new_scale > self.scale:
            if new_scale <= self.max_scale:
                self.scale = new_scale
                self.size = self.default_size * new_scale
                pygame.transform.smoothscale_by(self.surf, new_scale)
                self.rect = self.surf.get_rect(
                    bottomleft=(self.rect.bottomleft))
                self.jump_height = self.jump_height / (new_scale / 1.5)
        if new_scale < self.scale:
            if new_scale >= self.min_scale:
                self.scale = new_scale
                self.size = self.default_size * new_scale
                pygame.transform.smoothscale_by(self.surf, new_scale)
                self.rect = self.surf.get_rect(
                    bottomleft=(self.rect.bottomleft))
                self.jump_height = self.jump_height / new_scale

    def check_block(self, group_handler):
        if group_handler.blocks:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.blocks, False, False):
                for block in group_handler.blocks:
                    print(self.rect.bottom, block.object_id, block.rect.top)
                    if self.rect.colliderect(block.rect):
                        # Check if player is on top of block
                        if self.rect.bottom <= block.rect.top + 20:
                            self.rect.bottom = block.rect.top
                            self.gravity = 0
                            self.on_block = True
                        else:
                            # Check if player can push block
                            if self.size >= block.size:
                                if self.direction == "right":
                                    block.rect.left = self.rect.right
                                if self.direction == "left":
                                    block.rect.right = self.rect.left
                            else:
                                if self.rect.right > block.rect.left and self.direction == "right":
                                    self.rect.right = block.rect.left
                                elif self.rect.left < block.rect.right and self.direction == "left":
                                    self.rect.left = block.rect.right
            else:
                self.on_block = False

    def check_doors(self, group_handler):
        if group_handler.doors:
            for door in group_handler.doors:
                if self.rect.colliderect(door.rect):
                    if door.status == "closed":
                        if self.rect.right > door.rect.left and self.direction == "right":
                            self.rect.right = door.rect.left
                        elif self.rect.left < door.rect.right and self.direction == "left":
                            self.rect.left = door.rect.right

    def check_invincibility(self):
        if self.invincible == True:
            if pygame.time.get_ticks() - self.last_damaged > 1000:
                self.invincible = False

    def check_platform(self, group_handler):
        if group_handler.platforms:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.platforms, False, False):
                for platform in group_handler.platforms:
                    if self.rect.colliderect(platform.rect):
                        self.rect.bottom = platform.rect.y
                        self.gravity = 0
                        self.on_platform = True
            else:
                self.on_platform = False

    def check_moving_platform(self, group_handler):
        if group_handler.moving_platforms:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.moving_platforms, False, False):
                for platform in group_handler.moving_platforms:
                    if self.rect.colliderect(platform.rect):
                        self.rect.bottom = platform.rect.y
                        self.gravity = 0
                        self.on_platform = True

                        if platform.direction == "left":
                            self.rect.x -= platform.movement_speed
                        if platform.direction == "right":
                            self.rect.x += platform.movement_speed
            else:
                self.on_platform = False

    def check_walls(self, group_handler):
        if group_handler.walls:
            for wall in group_handler.walls:
                if self.rect.colliderect(wall.rect):
                    if self.rect.right > wall.rect.left and self.direction == "right":
                        self.rect.right = wall.rect.left
                    elif self.rect.left < wall.rect.right and self.direction == "left":
                        self.rect.left = wall.rect.right

    def destroy(self):
        self.kill()

    def get_input(self, group_handler):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = "left"
            self.move()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.move()
        if keys[pygame.K_e]:
            self.interact(group_handler)
        if keys[pygame.K_k]:
            self.health = 0

    def interact(self, group_handler):
        if group_handler.buttons:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.buttons, False, False):
                for button in group_handler.buttons:
                    if self.rect.colliderect(button.rect):
                        button.press(group_handler)

        if group_handler.doors:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.doors, False, False):
                for door in group_handler.doors:
                    if self.rect.colliderect(door.rect):
                        if door.requires_key:
                            for key in group_handler.keys:
                                if key.collected:
                                    if door.object_id == key.link_id:
                                        door.open()
                        else:
                            door.open()

        if group_handler.switches:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.switches, False, False):
                for switch in group_handler.switches:
                    if self.rect.colliderect(switch.rect):
                        switch.flip(group_handler)

    def jump(self):
        if self.rect.bottom == 720 or self.on_block or self.on_platform:
            self.gravity = self.jump_height

    def move(self):
        if self.direction == "left":
            self.rect.x -= self.movement_speed
        if self.direction == "right":
            self.rect.x += self.movement_speed

    def update(self, group_handler, score_handler):
        self.get_input(group_handler)
        self.apply_gravity()
        self.check_block(group_handler)
        self.check_doors(group_handler)
        self.check_platform(group_handler)
        self.check_moving_platform(group_handler)
        self.check_invincibility()
        self.check_walls(group_handler)
