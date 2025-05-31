from pgzero.builtins import Actor, sounds
from pgzero.keyboard import keyboard
import condicionais
import pygame

class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = True

        # Animações direcionais
        self.anim_idle_right = condicionais.HERO_ANIM_IDLE_RIGHT
        self.anim_run_right = condicionais.HERO_ANIM_RUN_RIGHT
        self.anim_jump_right = condicionais.HERO_ANIM_JUMP_RIGHT
        self.anim_die_right = condicionais.HERO_ANIM_DIE_RIGHT
        self.anim_shoot_right = condicionais.HERO_ANIM_SHOOT_RIGHT

        self.anim_idle_left = condicionais.HERO_ANIM_IDLE_LEFT
        self.anim_run_left = condicionais.HERO_ANIM_RUN_LEFT
        self.anim_jump_left = condicionais.HERO_ANIM_JUMP_LEFT
        self.anim_die_left = condicionais.HERO_ANIM_DIE_LEFT
        self.anim_shoot_left = condicionais.HERO_ANIM_SHOOT_LEFT

        self.anim_index = 0
        self.anim_timer = 0

        self.lives = 3
        self.is_dead = False
        self.death_frame = 0

        self.state = "idle"
        self.facing = 1  # 1 = direita, -1 = esquerda
        self.is_shooting = False
        self.shoot_frame = 0

    def shoot(self, mouse_pos=None):
        if not self.is_shooting and not self.is_dead:
            self.is_shooting = True
            self.shoot_frame = 0
            self.anim_timer = 0
            if mouse_pos:
                self.facing = 1 if mouse_pos[0] > self.x else -1
            try:
                sounds[condicionais.SOM_SHOOT].play()
            except Exception:
                pass

    def get_current_anim(self):
        """Retorna a animação correta baseada na direção e estado"""
        if self.facing == 1:  # Direita
            if self.is_dead:
                return self.anim_die_right, self.death_frame
            elif self.is_shooting:
                return self.anim_shoot_right, self.shoot_frame
            elif self.state == "run":
                return self.anim_run_right, self.anim_index
            elif self.state == "jump":
                return self.anim_jump_right, self.anim_index
            else:
                return self.anim_idle_right, self.anim_index
        else:  # Esquerda
            if self.is_dead:
                return self.anim_die_left, self.death_frame
            elif self.is_shooting:
                return self.anim_shoot_left, self.shoot_frame
            elif self.state == "run":
                return self.anim_run_left, self.anim_index
            elif self.state == "jump":
                return self.anim_jump_left, self.anim_index
            else:
                return self.anim_idle_left, self.anim_index

    def update(self):
        if self.is_dead:
            if self.death_frame < len(self.get_current_anim()[0]) - 1:
                self.death_frame += 1
            return

        keys = keyboard
        speed = 4

        # Movimento e direção
        moving = False
        if keys.d:
            self.x += speed
            self.facing = 1
            moving = True
        if keys.a:
            self.x -= speed
            self.facing = -1
            moving = True

        # Atualiza direção baseada no mouse quando não está se movendo
        if not moving:
            mouse_x, _ = pygame.mouse.get_pos()
            self.facing = 1 if mouse_x > self.x else -1

        prev_state = self.state
        if moving:
            self.state = "run"
        else:
            self.state = "idle"

        if keys.w and self.on_ground:
            self.vy = -10
            self.on_ground = False
            self.state = "jump"
            try:
                sounds[condicionais.SOM_JUMP].play()
            except Exception:
                pass

        if prev_state != self.state:
            self.anim_index = 0

        if self.is_shooting:
            if len(self.get_current_anim()[0]) > 0 and self.anim_timer % 4 == 0:
                self.shoot_frame = (self.shoot_frame + 1) % len(self.get_current_anim()[0])
                if self.shoot_frame == 0:
                    self.is_shooting = False

        # Física
        self.vy += 0.5
        self.y += self.vy
        if self.y >= condicionais.CHAO_Y:
            self.y = condicionais.CHAO_Y
            self.vy = 0
            self.on_ground = True
            if self.state == "jump":
                self.state = "idle"

        # Animações
        self.anim_timer += 1
        current_anim = self.get_current_anim()[0]
        if self.state == "run":
            if len(current_anim) > 0 and self.anim_timer % 5 == 0:
                self.anim_index = (self.anim_index + 1) % len(current_anim)
        elif self.state == "idle":
            if len(current_anim) > 0 and self.anim_timer % 8 == 0:
                self.anim_index = (self.anim_index + 1) % len(current_anim)
        elif self.state == "jump":
            self.anim_index = 0

    def draw(self):
        anim, frame = self.get_current_anim()
        
        if not anim:  # Se não houver animação para a direção atual
            return  # Não desenha nada
            
        img = anim[min(frame, len(anim)-1)]
        a = Actor(img, (self.x, self.y))
        a.anchor = ('center', 'bottom')
        
        # Não precisamos mais do flip_x pois já temos as imagens corretas
        a.draw()

    def get_shoot_direction(self):
        return self.facing

    def die(self):
        self.is_dead = True
        self.death_frame = 0
        try:
            sounds[condicionais.SOM_DIE].play()
        except Exception:
            pass

    def reset(self):
        self.x = condicionais.HERO_START_X
        self.y = condicionais.HERO_START_Y
        self.vx = 0
        self.vy = 0
        self.state = "idle"
        self.is_dead = False
        self.anim_index = 0
        self.anim_timer = 0

    def lose_life(self):
        self.lives -= 1
        try:
            sounds[condicionais.SOM_HIT].play()
        except Exception:
            pass
        if self.lives <= 0:
            self.die()
        else:
            self.reset()