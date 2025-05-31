from pgzero.builtins import Actor
import math
import random
import condicionais

class Enemy:
    def __init__(self, info):
        self.tipo = info["tipo"]
        self.x = info["x"]  # Não sobrescreve!
        self.y = info.get("y", condicionais.CHAO_Y)
        self.on_ground = True
        self.is_dead = False
        self.death_frame = 0
        self.anim_index = 0
        self.anim_timer = 0

        # Novas animações direcionais
        self.anim_idle_right = info.get("anim_idle_right", [])
        self.anim_run_right = info.get("anim_run_right", [])
        self.anim_die_right = info.get("anim_die_right", [])
        self.anim_idle_left = info.get("anim_idle_left", [])
        self.anim_run_left = info.get("anim_run_left", [])
        self.anim_die_left = info.get("anim_die_left", [])
        
        # Para o Wolf que tem animação de pulo
        if self.tipo == "Wolf":
            self.anim_jump_right = info.get("anim_jump_right", [])
            self.anim_jump_left = info.get("anim_jump_left", [])
        
        self.speed = info.get("speed", 1)
        self.sound = info.get("sound", None)
        self.scale = info.get("scale", 1.0)
        self.direction = info.get("direction", 1)  # NÃO calcula aleatoriamente aqui!
        self.vy = 0
        self.target_x = 0
        self.target_y = 0
        self.attack_timer = 0
        self.attack_cooldown = 60
        self.health = info.get("health", 1)

    
    def update(self):
        if self.is_dead:
            if self.death_frame < len(self.get_current_anim()[0]) - 1:
                self.death_frame += 1
            return

        self.anim_timer += 1
        current_anim = self.get_current_anim()[0]
        if len(current_anim) > 0 and self.anim_timer % 10 == 0:
            self.anim_index = (self.anim_index + 1) % len(current_anim)
        
        if self.tipo in ["Snake", "Gorgon"]:
            move_speed = self.speed if self.tipo == "Snake" else self.speed * 1.2
            self.x += move_speed * self.direction
                    
        elif self.tipo == "Wolf":
            self.x += self.speed * self.direction * 1.2
            if random.random() < 0.02 and self.on_ground:
                self.vy = -8
                self.on_ground = False
        
        if not self.on_ground:
            self.vy += 0.5
            self.y += self.vy
            if self.y >= condicionais.CHAO_Y:
                self.y = condicionais.CHAO_Y
                self.vy = 0
                self.on_ground = True

    def get_current_anim(self):
        """Retorna a animação correta baseada na direção"""
        if self.direction == 1:  # Direita
            if self.is_dead:
                return self.anim_die_right, self.death_frame
            elif not self.on_ground and self.tipo == "Wolf":
                return self.anim_jump_right, self.anim_index
            else:
                return self.anim_run_right, self.anim_index
        else:  # Esquerda
            if self.is_dead:
                return self.anim_die_left, self.death_frame
            elif not self.on_ground and self.tipo == "Wolf":
                return self.anim_jump_left, self.anim_index
            else:
                return self.anim_run_left, self.anim_index

    def draw(self):
        anim, frame = self.get_current_anim()
        
        if not anim:  # Se não houver animação para a direção atual
            return  # Não desenha nada
            
        img = anim[min(frame, len(anim)-1)]
        a = Actor(img, (self.x, self.y))
        a.anchor = ('center', 'bottom')
        
        # Aplica escala
        if self.scale != 1.0:
            import pygame
            a._surf = pygame.transform.scale(
                a._surf, 
                (int(a._surf.get_width() * self.scale), 
                 int(a._surf.get_height() * self.scale))
            )
        
        # Efeito de dano
        if hasattr(self, 'hit_timer') and self.hit_timer > 0:
            import pygame
            a._surf.fill((255, 0, 0, 128), special_flags=pygame.BLEND_ADD)
            self.hit_timer -= 1
            
        a.draw()

    def get_rect(self):
        width = 30 * self.scale
        height = 40 * self.scale
        
        if self.tipo == "Gorgon":
            width = 60 * self.scale
            height = 200 * self.scale
            return Rect((self.x - width/2, self.y - height/2), (width, height))
        elif self.tipo == "Wolf":
            return Rect((self.x - width/2, self.y - height + 35), (width, height))
        
        return Rect((self.x - width/2, self.y - height), (width, height))

    def is_hit_by(self, bullet):
        hit_box_width = 24 * self.scale
        hit_box_height = 32 * self.scale
        
        if self.tipo == "Gorgon":
            hit_box_width = 60 * self.scale
            hit_box_height = 200 * self.scale
            enemy_foot_y = self.y
            return (abs(bullet.x - self.x) < hit_box_width and 
                    bullet.y < enemy_foot_y + 100 and
                    bullet.y > enemy_foot_y - 100)
        elif self.tipo == "Wolf":
            return (abs(bullet.x - self.x) < hit_box_width and 
                    abs(bullet.y - (self.y - 35)) < hit_box_height)
        
        return (abs(bullet.x - self.x) < hit_box_width and 
                abs(bullet.y - self.y) < hit_box_height)

    def take_damage(self):
        self.health -= 1
        self.hit_timer = 5
        if self.health <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.death_frame = 0