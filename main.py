import pgzrun
from menu import Menu
from player import Hero
from bullet import Bullet
from enemy import Enemy
import condicionais
from pgzero.builtins import mouse, Actor, sounds, music, keyboard, keys
import math
import random

WIDTH = 800
HEIGHT = 480

menu = Menu()

# Inicialização dos sistemas
hero = Hero(condicionais.HERO_START_X, condicionais.HERO_START_Y)
enemies = []
bullets = []
particles = []

# Estado do jogo
game_state = {
    "contador": 0,
    "fase": 1,
    "objetivo": 10,
    "jogo_zerado": False,
    "game_over_mostrado": False,
    "esperando_game_over": False,
    "timer_game_over": 0,
    "paused": False,
    "enemies_to_remove": [],  # Nova lista para remoção segura
    "bullets_to_remove": []   # Nova lista para remoção segura
}

class Particle:
    def __init__(self, x, y, color, velocity, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.lifetime = lifetime
        self.age = 0
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.age += 1
        return self.age < self.lifetime
        
    def draw(self, screen):
        alpha = 255 * (1 - self.age / self.lifetime)
        screen.draw.filled_circle((int(self.x), int(self.y)), 3, 
                                (self.color[0], self.color[1], self.color[2], alpha))

def create_explosion(x, y, color):
    for _ in range(20):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 5)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        particles.append(Particle(x, y, color, (vx, vy), 30))

def tocar_musica():
    if not music.is_playing(condicionais.MUSICA):
        music.play(condicionais.MUSICA)

def spawn_enemy():
    fase = game_state["fase"]
    if fase < 3:
        tipos_disponiveis = [condicionais.INIMIGOS[0]]
    elif fase < 5:
        tipos_disponiveis = [condicionais.INIMIGOS[0], condicionais.INIMIGOS[1]]
    else:
        tipos_disponiveis = condicionais.INIMIGOS

    enemy_data = random.choice(tipos_disponiveis)
    lado = random.choice(["esq", "dir"]) if enemy_data["tipo"] == "Snake" else "esq"
    
    x = 0 if lado == "esq" else WIDTH
    direction = 1 if lado == "esq" else -1

    enemy_info = enemy_data.copy()
    enemy_info["x"] = x
    enemy = Enemy(enemy_info)
    enemy.direction = direction
    enemy.target_x = hero.x
    enemy.target_y = hero.y
    enemies.append(enemy)

def safe_remove_enemies():
    for enemy in game_state["enemies_to_remove"]:
        if enemy in enemies:
            enemies.remove(enemy)
    game_state["enemies_to_remove"].clear()

def safe_remove_bullets():
    for bullet in game_state["bullets_to_remove"]:
        if bullet in bullets:
            bullets.remove(bullet)
    game_state["bullets_to_remove"].clear()

def update():
    global particles

    if menu.active:
        menu.update()
        return

    if game_state["paused"]:
        return

    # Limpa as listas de remoção
    safe_remove_enemies()
    safe_remove_bullets()

    # Atualiza partículas
    particles = [p for p in particles if p.update()]

    tocar_musica()

    if game_state["esperando_game_over"]:
        game_state["timer_game_over"] += 1
        anim_len = len(hero.anim_die_right) if hasattr(hero, "anim_die_right") else len(condicionais.HERO_ANIM_DIE)
        if game_state["timer_game_over"] >= anim_len * 5:
            game_state["esperando_game_over"] = False
            game_state["game_over_mostrado"] = True
        return

    if game_state["jogo_zerado"] or game_state["game_over_mostrado"]:
        return

    hero.update()

    # Atualiza balas
    for bullet in bullets[:]:
        bullet.update()
        if bullet.x < 0 or bullet.x > WIDTH:
            game_state["bullets_to_remove"].append(bullet)
            create_explosion(bullet.x, bullet.y, (255, 100, 0))

    # Atualiza inimigos
    if not hero.is_dead:
        for enemy in enemies[:]:
            enemy.target_x = hero.x
            enemy.target_y = hero.y
            enemy.update()
            if (enemy.direction == 1 and enemy.x > WIDTH + 40) or (enemy.direction == -1 and enemy.x < -40):
                game_state["enemies_to_remove"].append(enemy)

        # Colisão tiro <-> inimigo
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if not enemy.is_dead and enemy not in game_state["enemies_to_remove"]:
                    if enemy.is_hit_by(bullet):
                        try:
                            if hasattr(enemy, "sound") and enemy.sound:
                                getattr(sounds, enemy.sound).play()
                        except Exception:
                            pass
                        
                        create_explosion(enemy.x, enemy.y, (255, 0, 0))
                        game_state["bullets_to_remove"].append(bullet)
                        enemy.take_damage()
                        
                        if enemy.is_dead:
                            game_state["contador"] += 1
                            game_state["enemies_to_remove"].append(enemy)
                            
                            if game_state["contador"] >= game_state["objetivo"]:
                                if game_state["fase"] < 10:
                                    game_state["fase"] += 1
                                    game_state["objetivo"] = 5 + (game_state["fase"] * 2)
                                    game_state["contador"] = 0
                                    enemies.clear()
                                    for _ in range(min(3, min(3 + game_state["fase"], 8))):
                                        spawn_enemy()
                                else:
                                    game_state["jogo_zerado"] = True
                        break

        # Colisão inimigo <-> jogador
        for enemy in enemies[:]:
            if not enemy.is_dead and abs(hero.x - enemy.x) < 32 and abs(hero.y - enemy.y) < 32:
                create_explosion(hero.x, hero.y, (255, 255, 255))
                hero.lose_life()
                if hero.lives <= 0:
                    game_state["esperando_game_over"] = True
                    game_state["timer_game_over"] = 0
                game_state["enemies_to_remove"].append(enemy)
                break

    # Limite de inimigos e chance de spawn
    max_enemies = min(3 + game_state["fase"], 8)
    spawn_chance = 0.03 + game_state["fase"] * 0.005
    if not game_state["jogo_zerado"] and not game_state["game_over_mostrado"] and len(enemies) < max_enemies:
        if random.random() < spawn_chance:
            spawn_enemy()

def draw():
    if menu.active:
        menu.draw(screen)
        return

    # Background
    img = condicionais.BACKGROUND
    fundo = Actor(img)
    fator = max(WIDTH / fundo.width, HEIGHT / fundo.height)
    fundo.width = int(fundo.width * fator)
    fundo.height = int(fundo.height * fator)
    fundo.topleft = (0, 0)
    fundo.draw()

    # Chão
    cor_chao = (205, 133, 63)
    altura_chao = HEIGHT - condicionais.CHAO_Y
    screen.draw.filled_rect(Rect((0, condicionais.CHAO_Y), (WIDTH, altura_chao)), cor_chao)

    # Desenha elementos do jogo
    for enemy in enemies:
        enemy.draw()
    
    hero.draw()

    for bullet in bullets:
        bullet.draw(screen)

    for particle in particles:
        particle.draw(screen)

    # Interface do usuário
    screen.draw.text(f"Inimigos derrotados: {game_state['contador']}/{game_state['objetivo']}", 
                    (10, 10), color="white", fontsize=36)
    screen.draw.text(f"Fase: {game_state['fase']}", (10, 50), color="yellow", fontsize=32)
    screen.draw.text(f"Vidas: {hero.lives}", (10, 90), color="white", fontsize=32)

    if game_state["game_over_mostrado"]:
        screen.draw.text("GAME OVER", 
                        center=(WIDTH // 2, HEIGHT // 2), 
                        color="red", 
                        fontsize=60)

    if game_state["jogo_zerado"]:
        screen.draw.text("VOCÊ ZEROU O JOGO!", 
                        center=(WIDTH // 2, HEIGHT // 2), 
                        color="gold", 
                        fontsize=60)
    
    if game_state["paused"]:
        screen.draw.filled_rect(Rect((0, 0), (WIDTH, HEIGHT)), (0, 0, 0, 128))
        screen.draw.text("PAUSADO", 
                        center=(WIDTH//2, HEIGHT//2), 
                        fontsize=60, 
                        color="white", 
                        shadow=(2,2))
        screen.draw.text("ESC - Voltar ao jogo", 
                        center=(WIDTH//2, HEIGHT//2 + 60), 
                        fontsize=30, 
                        color="white")
        screen.draw.text("F5 - Salvar jogo", 
                        center=(WIDTH//2, HEIGHT//2 + 90), 
                        fontsize=30, 
                        color="white")

def on_mouse_down(button, pos):
    if menu.active:
        menu.handle_click(pos)
        return

    if game_state["jogo_zerado"] or hero.is_dead or game_state["game_over_mostrado"] or game_state["paused"]:
        return

    if button == mouse.LEFT:
        direction = hero.facing
        new_bullet = Bullet(hero.x + 20 * direction, hero.y - 20, direction)
        bullets.append(new_bullet)
        create_explosion(hero.x + 20 * direction, hero.y - 20, (255, 255, 0))
        try:
            sounds.shoot.play()
        except Exception:
            pass
        hero.shoot(pos)

def on_key_down(key):
    if menu.active:
        action = menu.handle_input(key)
        if action == "novo jogo":
            reset_game()
            menu.active = False
        elif action == "carregar":
            saved_state = menu.load_game()
            if saved_state:
                load_game_state(saved_state)
                menu.active = False
        return

    if game_state["game_over_mostrado"] or game_state["jogo_zerado"]:
        if key in (keys.SPACE, keys.RETURN):
            menu.active = True
            return

    if key == keys.ESCAPE:
        game_state["paused"] = not game_state["paused"]
        return

    if game_state["paused"]:
        if key == keys.F5:
            menu.save_game(game_state)
            try:
                sounds.save.play()
            except:
                pass
        return

    if not hero.is_dead:
        if key in (keys.W, keys.UP) and hero.on_ground:
            hero.vy = -10
            hero.on_ground = False
            try:
                sounds.jump.play()
            except:
                pass

def reset_game():
    global game_state
    game_state = {
        "contador": 0,
        "fase": 1,
        "objetivo": 10,
        "jogo_zerado": False,
        "game_over_mostrado": False,
        "esperando_game_over": False,
        "timer_game_over": 0,
        "paused": False,
        "enemies_to_remove": [],
        "bullets_to_remove": []
    }
    hero.reset()
    hero.lives = 3
    enemies.clear()
    bullets.clear()
    particles.clear()

def load_game_state(saved_state):
    global game_state
    for k in game_state.keys():
        if k in saved_state:
            game_state[k] = saved_state[k]
    hero.lives = saved_state.get("vidas", 3)
    hero.reset()
    enemies.clear()
    bullets.clear()
    particles.clear()

pgzrun.go()