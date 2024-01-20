from datetime import datetime
import pygame
import sqlite3


class ScoreHandler:
    def __init__(self, database):
        super().__init__()
        self.old_scores = []
        self.current_score = pygame.time.get_ticks() - sum(self.old_scores)

        # Create level tables
        for index in range(1,7):
            database.create_table("./Data/Players/Scores.db", f"level{index}", "username STRING, score INTEGER")

    def clear_scores(self):
        pass

    def get_score(self):
        return self.current_score

    """ def sort_scores(self):
        for i in range(10):
            for score in range(0, len(scores)-1):
                if scores[score][2] > scores[score+1][2]:
                    temp = scores[score]
                    scores[score] = scores[score+1]
                    scores[score+1] = temp
        return scores """

    def update(self):
        print(self.old_scores)
        self.current_score = pygame.time.get_ticks() - sum(self.old_scores)
        # print(f"current score {self.current_score} old score {self.old_score}"

    def reset_score(self):
        self.old_scores.append(self.current_score)
        return self.old_scores
        # print("Score reset! old score", self.old_score)

    def write_score(self, current_level):
        connection = sqlite3.connect("./Data/Players/Scores.db")
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO level{current_level} VALUES ('Sam', {self.current_score})")
        print(f"{self.current_score} written to level{current_level} table")
