from Classes.Database import Database
from Classes.GroupHandler import GroupHandler
from Classes.ScoreHandler import ScoreHandler
from Classes.User import User


class Game:
    def __init__(self):
        pass

    def generate_level(self, group_handler, level, score_handler):
        # Create groups and generate objects for level
        score_handler.reset_score()
        group_handler.reset_groups()
        group_handler.create_groups(level)
        group_handler.create_objects(level)
        print("Generated level", level)

    def get_level(self):
        # Get level from 'CurrentLevel.txt'
        file = open("./Data/Levels/CurrentLevel.txt", "r")
        current_level = (file.readlines())[0]
        file.close()
        return current_level

    def next_level(self, database, group_handler, score_handler, user):
        # Get level from 'CurrentLevel.txt'
        file = open("./Data/Levels/CurrentLevel.txt", "r")
        data = file.readlines()
        current_level = int(data[0])
        file.close()

        # Update Users.db" database
        username = user.get_username()
        user_data = user.get_data(username)
        if user_data[2] < current_level + 1:
            # Update character permissions
            database.update_value("./Data/Players/Users.db", "users", "characters", str(current_level + 1), "username", str(username))

            # Update level permissions
            database.update_value("./Data/Players/Users.db", "users", "levels", str(current_level + 1), "username", str(username))

        # Update 'Scores.db' database
        current_score = score_handler.get_score()
        database.insert_value("./Data/Players/Scores.db", f"level{current_level}", user.get_username(), current_score)

        # Update 'CurrentLevel.txt'
        file = open("./Data/Levels/CurrentLevel.txt", "w")
        file.write(str(current_level + 1))
        file.close()

        # Generate next level
        current_level += 1
        self.generate_level(group_handler, current_level, score_handler)
        return current_level
    
    def update(self, database, group_handler, score_handler, user):
        if group_handler.players:
            for player in group_handler.players:
                if player.rect.y > 1280:
                    self.next_level(database, group_handler, score_handler, user)