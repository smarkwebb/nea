from Classes.Database import Database
from Classes.Game import Game
from Classes.GroupHandler import GroupHandler
from Classes.ScoreHandler import ScoreHandler
from Classes.User import User
import pygame
import sys


class Menu:
    def __init__(self):
        pass

    def mouse_event(self, database, game, group_handler, score_handler, user):
        # Handles mouse events
        pos = pygame.mouse.get_pos()

        if group_handler.click_buttons:
            for button in group_handler.click_buttons:
                if button.check_pressed(pos):
                    if button.function == "play":
                        file = open("Data/Players/CurrentCharacter.txt", "r")
                        character = file.readlines()[0]
                        file.close()
                        if character in ("Bob UNLOCKED", "Charles UNLOCKED", "Robin UNLOCKED", "Sam UNLOCKED"):
                            file = open("Data/Levels/CurrentLevel.txt", "r")
                            level = file.readlines()[0]
                            file.close()
                            if level:
                                game.next_level(database, group_handler, score_handler, user)
                    if button.function == "quit":
                        sys.exit()
                    if "character" in button.function:
                        self.select_character(button.function, user)
                    if "level" in button.function:
                        self.select_level(button.function, game, group_handler, user)

    def select_character(self, function, user):
        user_data = user.get_data(user.get_username())
        characters = ["Bob", "Robin", "Charles", "Sam"]

        # Check 'Users.db' database
        for index in range(len(characters)):
            if function == f"character{index + 1}":
                if user_data[2] > index:  # Check user has unlocked character
                    character = f"{characters[index]} UNLOCKED"
                else:
                    return None

        # Update 'CurrentCharacter.txt'
        file = open("./Data/Players/CurrentCharacter.txt", "w")
        file.write(str(character))
        file.close()

    def select_level(self, function, game, group_handler, user):
        user_data = user.get_data(user.get_username())

        # Check 'Users.db' database
        for index in range(6):
            if function == f"level{index + 1}":
                if user_data[3] > index:
                    level = index + 1
                else:
                    return None
                
        # Update 'CurrentLevel.txt'
        file = open("./Data/Levels/CurrentLevel.txt", "w")
        file.write(str(level))
        file.close()

        # Start level
        game.generate_level(group_handler, level)

    def hover_preview(self, group_handler, score_handler):
        # Displays level previews on hover
        pos = pygame.mouse.get_pos()
        if group_handler.click_buttons:
            for button in group_handler.click_buttons:
                if button.check_pressed(pos):
                    for index in range(6):
                        if button.function == f"level{index}":
                            for text in group_handler.display_texts:
                                if "score" in text.function:
                                    text.show(index, score_handler)
                            for image in group_handler.images:
                                if "level" in image.image_id:
                                    image.hide()
                                if image.image_id == f"level{index}":
                                    image.show()

    def update(self, group_handler, score_handler):
        self.hover_preview(group_handler, score_handler)

        if group_handler.images:
            for image in group_handler.images:
                if "character" in image.image_id:
                    image.show()
