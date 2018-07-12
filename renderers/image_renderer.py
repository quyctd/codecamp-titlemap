import pygame

class ImageRenderer:
    def __init__(self, image_url):
        self.image = pygame.image.load(image_url)
        self.image = pygame.transform.scale(self.image, (32, 32))

    def render(self, canvas, x, y):
        width = self.image.get_width()
        height = self.image.get_height()
        # render_pos = (x - width / 2, y - height / 2)
        render_pos = (x, y)
        canvas.blit(self.image, render_pos)