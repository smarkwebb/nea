from Classes.Database import Database
from Classes.Game import Game
from Classes.GroupHandler import GroupHandler
from Classes.Menu import Menu
from Classes.ScoreHandler import ScoreHandler
from Classes.User import User
import pygame


database = Database()
game = Game()
group_handler = GroupHandler()
menu = Menu()
score_handler = ScoreHandler(database)
user = User()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

group_handler.create_groups(0)
group_handler.create_objects(0)

username = None
while not username:
    username = user.login()

user_data = user.get_data(user.get_username())

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game.generate_level(group_handler, 0, score_handler)
        if event.type == pygame.MOUSEBUTTONDOWN:
            menu.mouse_event(database, game, group_handler, score_handler, user)

    game.update(database, group_handler, score_handler, user)
    group_handler.update(group_handler, score_handler)
    menu.update(group_handler, score_handler, user)
    score_handler.update()

    # Check player death
    if group_handler.players:
        for player in group_handler.players:
            if player.health <= 0:
                running = False

    # Blit objects onto screen
    screen.fill((255, 255, 255))
    for group in range(0, len(group_handler.groups)):
        if group_handler.group_vars[group] != None:
            for object in group_handler.group_vars[group]:
                screen.blit(object.surf, object.rect)

    pygame.display.update()
    clock.tick(60)

print("GAME OVER")
