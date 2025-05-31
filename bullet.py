from pgzero.builtins import Actor
import random
import math

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 10
        self.img = "bullet"  # Uma única imagem simples
        
    def update(self):
        self.x += self.speed * self.direction
        
    def draw(self, screen):
        # Desenha apenas a bala sem o rastro por enquanto
        a = Actor(self.img, (self.x, self.y))
        a.anchor = ('center', 'center')
        a.draw()
        