from Classes.Database import Database
import pygame


class DisplayText(pygame.sprite.Sprite):
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

        # Tuple formatting
        bg_colour = self.bg_colour.strip("()")
        fg_colour = self.fg_colour.strip("()")
        self.bg_list = bg_colour.split(", ")
        self.fg_list = fg_colour.split(", ")
        self.font = pygame.font.Font(
            "Assets/Fonts/Munro.ttf", int(self.font_size))

        field = None
        for score in range(10):
            if self.function == f"score{score}":
                field = score
        if field:
            database = Database()
            data = database.get_data(
                "./Data/Players/Scores.db", "level1", None)
            try:
                score = data[field]
                self.surf = self.font.render(f"{score[0]}: {score[1]}", False, (int(self.bg_list[0]), int(
                    self.bg_list[1]), int(self.bg_list[2])), (int(self.fg_list[0]), int(self.fg_list[1]), int(self.fg_list[2])))
            except:
                self.surf = self.font.render(f"None", False, (int(self.bg_list[0]), int(
                    self.bg_list[1]), int(self.bg_list[2])), (int(self.fg_list[0]), int(self.fg_list[1]), int(self.fg_list[2])))
        elif self.function == "current_score":
            self.surf = self.font.render(f"{pygame.time.get_ticks()}", False, (int(self.bg_list[0]), int(
                self.bg_list[1]), int(self.bg_list[2])), (int(self.fg_list[0]), int(self.fg_list[1]), int(self.fg_list[2])))
        else:
            self.surf = self.font.render(self.text, False, (int(self.bg_list[0]), int(self.bg_list[1]), int(
                self.bg_list[2])), (int(self.fg_list[0]), int(self.fg_list[1]), int(self.fg_list[2])))
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

    def show(self, level, score_handler):
        field = None
        for score in range(10):
            if self.function == f"score{score}":
                field = score
        if field:
            database = Database()
            data = database.get_data(
                "./Data/Players/Scores.db", f"level{level}", None)
            try:
                score = data[field]
                self.surf = self.font.render(f"{score[0]}: {score[1]}", False, (int(self.bg_list[0]), int(
                    self.bg_list[1]), int(self.bg_list[2])), (int(self.fg_list[0]), int(self.fg_list[1]), int(self.fg_list[2])))
            except:
                self.surf = self.font.render(f"None", False, (int(self.bg_list[0]), int(
                    self.bg_list[1]), int(self.bg_list[2])), (int(self.fg_list[0]), int(self.fg_list[1]), int(self.fg_list[2])))
        elif self.function == "current_score":
            self.surf = self.font.render(f"{score_handler.get_score()}", False, (int(self.bg_list[0]), int(
                self.bg_list[1]), int(self.bg_list[2])), (int(self.fg_list[0]), int(self.fg_list[1]), int(self.fg_list[2])))
        else:
            self.surf = self.font.render(self.text, False, (int(self.bg_list[0]), int(self.bg_list[1]), int(
                self.bg_list[2])), (int(self.fg_list[0]), int(self.fg_list[1]), int(self.fg_list[2])))
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

    def hide(self):
        self.surf = pygame.Surface((0, 0))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(bottomleft=(int(self.x), int(self.y)))

    def update(self, group_handler, score_handler):
        if self.function == "current_score":
            self.show(None, score_handler)
