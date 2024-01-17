import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.image.load("./Assets/Sprites/Player.png")
        self.surf_size = 30
        self.rect = self.surf.get_rect(bottomleft=(int(x), int(y)))

        self.attack_damage = 25
        self.direction = "right"
        self.gravity = 0
        self.health = 100
        self.object_id = "player0"
        self.invincible = False
        self.jump_height = 20
        self.keys_collected = 0
        self.last_damaged = pygame.time.get_ticks()
        self.movement_speed = 4
        self.on_platform = False
        self.scale = 1

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
            print(f"{target} is now invincible")

    def change_scale(self, new_scale):
        if new_scale > self.scale:
            if new_scale < 3:
                self.surf_size = 30 * new_scale
                pygame.transform.smoothscale_by(self.surf, new_scale)
                self.rect = self.surf.get_rect(
                    bottomleft=(self.rect.bottomleft))
                self.jump_height = 15 / (new_scale / 1.5)
                self.scale = new_scale
        if new_scale < self.scale:
            if new_scale > 0.5:
                self.surf_size = 30 * new_scale
                pygame.transform.smoothscale_by(self.surf, new_scale)
                # self.surf = pygame.Surface((30 * new_scale, 30 * new_scale))
                self.rect = self.surf.get_rect(
                    bottomleft=(self.rect.bottomleft))
                self.jump_height = 15 / (new_scale)
                self.scale = new_scale

    def check_block(self, group_handler):
        if group_handler.blocks:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.blocks, False, False):
                for block in group_handler.blocks:
                    if self.rect.colliderect(block.rect):
                        if self.surf_size > block.surf_size:
                            if self.direction == "right":
                                block.rect.left = self.rect.right
                            if self.direction == "left":
                                block.rect.right = self.rect.left
                        else:
                            if self.direction == "right":
                                self.rect.x = block.rect.left
                            if self.direction == "left":
                                self.rect.x = block.rect.right

    def check_enemy(self, group_handler):
        if group_handler.enemies:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.enemies, False, False):
                for enemy in group_handler.enemies:
                    if self.rect.colliderect(enemy.rect):
                        self.attack(enemy)

    def check_invincibility(self):
        if self.invincible == True:
            if pygame.time.get_ticks() - self.last_damaged > 1000:
                self.invincible = False
                print(f"{self} is no longer invincible")

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

    def check_walls(self, group_handler):
        if group_handler.walls:
            if pygame.sprite.groupcollide(group_handler.players, group_handler.walls, False, False):
                for wall in group_handler.walls:
                    if self.rect.colliderect(wall.rect):
                        if self.rect.x > wall.rect.x:
                            self.rect.x = wall.rect.right + 1
                            return True
                        if self.rect.x < wall.rect.x:
                            self.rect.x = wall.rect.left - 1
                            return True

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
            self.interact()
        if keys[pygame.K_k]:
            self.health = 0

    def interact(self):
        pass

    def jump(self):
        if self.rect.bottom == 720 or self.on_platform:
            self.gravity = self.jump_height

    def move(self):
        if self.direction == "left":
            if self.rect.left >= 0:
                self.rect.x -= self.movement_speed

        if self.direction == "right":
            if self.rect.right <= 1280 or self.keys_collected >= 1:
                self.rect.x += self.movement_speed

    def update(self, group_handler):
        self.apply_gravity()
        self.check_block(group_handler)
        self.check_enemy(group_handler)
        self.check_platform(group_handler)
        self.check_invincibility()
        self.check_walls(group_handler)
        self.get_input(group_handler)
