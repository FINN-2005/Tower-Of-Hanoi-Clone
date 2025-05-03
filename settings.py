import pygame
from pygame import Vector2 as V2

RES = W,H = 1000,600
HW, HH = W/2, H/2
FPS = 120

pygame.init()

class Group(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
    
class disc_group(Group):
    ACTIVE_DISC = None
    def __init__(self, *sprites):
        super().__init__(*sprites)
    
    def draw(self, screen):
        for disc in self.sprites():
            if disc_group.ACTIVE_DISC == disc:
                self.remove(disc)
                self.add(disc)
                break
        for disc in self.sprites():
            disc.draw(screen)
    
    def update(self, *args):
        for disc in reversed(self.sprites()):
            disc.update(*args)


# Groups
TOWER_GROUP = Group()
DISC_GROUP = disc_group()

# Constants
class Disc_stuff:
    MAX_DISC_LEVEL = 6
    W = 200
    H = 35
    class cols:
        default = 'white'
        level_1 = (217, 26, 45)
        level_2 = (245, 242, 54)
        level_3 = (255, 98, 25)
        level_4 = (247, 8, 255)
        level_5 = (22, 247, 37)
        level_6 = (66, 230, 255)

class Tower_stuff:
    stick_h = 275
    stick_w = 15
    base_w = 250
    base_h = 25
    class cols:
        stick = (186, 124, 95)
        base = (74, 49, 38)
    
    