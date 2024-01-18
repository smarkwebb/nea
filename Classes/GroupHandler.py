from Classes.BigPressurePlate import BigPressurePlate
from Classes.Block import Block
from Classes.Button import Button
from Classes.ClickButton import ClickButton
from Classes.DisplayText import DisplayText
from Classes.Door import Door
from Classes.Enemy import Enemy
from Classes.Player import Player
from Classes.HealthBar import HealthBar
from Classes.Image import Image
from Classes.Key import Key
from Classes.MovingPlatform import MovingPlatform
from Classes.Platform import Platform
from Classes.Player import Player
from Classes.PressurePlate import PressurePlate
from Classes.Switch import Switch
from Classes.Wall import Wall
import os
import pygame


class GroupHandler:
    def __init__(self):
        super().__init__()
        self.big_buttons = None
        self.blocks = None
        self.buttons = None
        self.click_buttons = None
        self.display_texts = None
        self.doors = None
        self.enemies = None
        self.health_bars = None
        self.images = None
        self.keys = None
        self.moving_platforms = None
        self.menu_buttons = None
        self.platforms = None
        self.players = None
        self.pressure_plates = None
        self.switches = None
        self.walls = None

        self.groups = [BigPressurePlate, Block, Button, ClickButton, DisplayText,
                       Door, Enemy, HealthBar, Image, Key, MovingPlatform, Platform, Player, PressurePlate, Switch, Wall]
        self.group_vars = [self.big_buttons, self.blocks, self.buttons, self.click_buttons, self.display_texts, self.doors,
                           self.enemies, self.health_bars, self.images, self.keys, self.moving_platforms, self.platforms, self.players, self.pressure_plates, self.switches, self.walls]
        self.objects = ["Big Pressure Plates", "Blocks", "Buttons", "Click Buttons", "Display Texts",
                        "Doors", "Enemies", "Health Bars", "Images", "Keys", "Moving Platforms", "Platforms", "Players", "Pressure Plates", "Switches", "Walls"]
        self.handles = ["Big Pressure Plates/Big Pressure Plate", "Blocks/Block",
                        "Buttons/Button", "Click Buttons/Click Button", "Display Texts/Display Text", "Doors/Door", "Enemies/Enemy", "Health Bars/Health Bar", "Images/Image", "Keys/Key", "Moving Platforms/Moving Platform", "Platforms/Platform", "Players/Player", "Pressure Plates/Pressure Plate", "Switches/Switch", "Walls/Wall"]

    def create_groups(self, current_level):
        for group in range(0, len(self.groups)):
            path = f"./Data/Levels/Level {current_level}/Objects/{self.objects[group]}"
            if os.path.isdir(path):
                self.group_vars[group] = pygame.sprite.Group()

    def create_objects(self, current_level):
        for group in range(0, len(self.groups)):
            for file in range(20):
                path = f"./Data/Levels/Level {current_level}/Objects/{self.handles[group]} {file}.txt"
                if os.path.isfile(path):
                    file = open(path)
                    data = file.readlines()
                    kwargs = {}
                    for entry in data:
                        entry = entry.strip("\n")
                        arg, par = entry.split("=")
                        kwargs[arg] = par
                    self.group_vars[group].add(self.groups[group](**kwargs))
                    file.close()

    def get_objects(self):
        return self.group_vars

    def reset_groups(self):
        for group in range(0, len(self.groups)):
            if self.group_vars[group]:
                self.group_vars[group] = None

    def update(self, group_handler, score_handler):
        for group in range(0, len(self.groups)):
            if self.group_vars[group] != None:
                self.group_vars[group].update(group_handler, score_handler)

        self.big_pressure_plates = self.group_vars[0]
        self.blocks = self.group_vars[1]
        self.buttons = self.group_vars[2]
        self.click_buttons = self.group_vars[3]
        self.display_texts = self.group_vars[4]
        self.doors = self.group_vars[5]
        self.enemies = self.group_vars[6]
        self.health_bars = self.group_vars[7]
        self.images = self.group_vars[8]
        self.keys = self.group_vars[9]
        self.moving_platforms = self.group_vars[10]
        self.platforms = self.group_vars[11]
        self.players = self.group_vars[12]
        self.pressure_plates = self.group_vars[13]
        self.switches = self.group_vars[14]
        self.walls = self.group_vars[15]
