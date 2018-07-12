from game_object import GameObject
from renderers.image_renderer import ImageRenderer
from physics.box_collider import BoxCollider

class Platform(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, x, y)
        self.renderer = ImageRenderer('assets/images/sprite/platform0000.png')
        self.box_collider = BoxCollider(32, 32)
