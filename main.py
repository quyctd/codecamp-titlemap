import pygame

import game_object

from input.input_manager import InputManager
from maps.map_generator import generate_map
from renderers.image_renderer import ImageRenderer
from physics.box_collider import BoxCollider
from map_titles.grass import Grass
from map_titles.platform import Platform
from map_titles.spike import Spike
from map_titles.spikefake import SpikeFake

BG = (0, 0, 0)
BG = pygame.image.load('bg.jpg')
BG = pygame.transform.scale(BG, (1600, 800))


# 1. Init pygame
pygame.init()

# 2. Set screen
SIZE = (30 * 32, 15 * 32)
canvas = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Jet zero')

# 3. Clock
clock = pygame.time.Clock()

loop = True

input_manager = InputManager()

class Player():
    def __init__(self, x, y, input_manager):
        self.x = x
        self.y = y
        self.vel = 8
        self.width = 25
        self.height = 32
        self.renderer = ImageRenderer("assets/images/sprite/player.png")
        
        self.box_collider = BoxCollider(25, 32)
        self.is_active = True
        self.input_manager = input_manager
        self.isJump = False
        self.jumpCount = 5
        self.count = 0
        self.move = True
    
    def update(self):
        if self.box_collider is not None:
            self.box_collider.x = self.x
            self.box_collider.y = self.y
        
        if self.input_manager.right_pressed:
            self.x += 2
        elif self.input_manager.left_pressed:
            self.x -= 2

        if not self.isJump:
            if self.input_manager.x_pressed:
                self.isJump = True
        else:
            if self.jumpCount >= -5:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount ** 2 * 0.8 * neg
                if neg == 1:
                    if len(game_object.collide_with(self.box_collider, Grass)) != 0:
                        self.jumpCount *= -1
                        
                elif neg == -1:
                    if len(game_object.collide_with(self.box_collider, Grass)) != 0:
                        list_collide = game_object.collide_with(self.box_collider, Grass)
                        for object in list_collide:
                            dy = object.y - 32
                            if object.y < self.y:
                                continue
                            if dy <= self.y:
                                   self.y = dy
                        self.jumpCount = -5
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 5
        
        if not self.isJump:
            if len(game_object.collide_with(self.box_collider, Grass)) != 0:
                list_collide = game_object.collide_with(self.box_collider, Grass)
                for object in list_collide:
                    
                    if self.box_collider.y == object.y:
                        if self.x >= object.x:
                            self.x += 1
                        elif self.x < object.x:
                            self.x -= 1
                        pass
                    else:
                        self.move = True
                        dy = object.y - 32
                        if dy <= self.y:
                            self.y = dy
                
            elif len(game_object.collide_with(self.box_collider, Spike)) != 0:
                self.is_active = False
            elif  len(game_object.collide_with(self.box_collider, SpikeFake)) != 0:
                list_object = game_object.collide_with(self.box_collider, SpikeFake)
                for obj in list_object:
                    obj.renderer = ImageRenderer('assets/images/sprite/spike0000.png')
                self.count += 1
                if self.count >= 30:
                    self.is_active = False
                    self.count = 0
                
            else:
                for object in game_object.game_objects:
                    if (object.x <= self.x <= object.x + 32 or object.x <= self.x + self.width <= object.x + 32) and self.y < object.y:
                        if self.x + 32 == object.x:
                            continue
                        else:
                            self.y = object.y - 32
                            
                            break

    def render(self, canvas):
        if self.renderer is not None:
            self.renderer.render(canvas, self.x, self.y)
        # if self.box_collider is not None:
        #     self.box_collider.render(canvas)

    def deactivate(self):
        self.is_active = False

man = Player(4 * 32, 10 * 32, input_manager)
game_object.add(man)

generate_map('assets/maps/map.json')

while loop:
    # 1. Event processing
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            loop = False
        else:
            input_manager.update(event)

    game_object.update()

    # 2. Draw
    canvas.blit(BG, (0, 0))

    game_object.render(canvas)

    # 3. Flip
    pygame.display.flip()
    clock.tick(60)
