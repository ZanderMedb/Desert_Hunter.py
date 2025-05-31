# Configurações da tela
WIDTH = 800
HEIGHT = 480
CHAO_Y = 400

# Sons
MUSICA = "music"
SOM_JUMP = "jump"
SOM_SHOOT = "shoot"
SOM_HIT = "hit"
SOM_DIE = "die"

# Background
BACKGROUND = "desert"

# Posição inicial do herói
HERO_START_X = 100
HERO_START_Y = CHAO_Y

# Animações do Herói - Direita
HERO_ANIM_IDLE_RIGHT = [
    "player/right/idle1",
    "player/right/idle2",
    "player/right/idle3",
    "player/right/idle4",
    "player/right/idle5"
]

HERO_ANIM_RUN_RIGHT = [
    "player/right/run1",
    "player/right/run2",
    "player/right/run3",
    "player/right/run4",
    "player/right/run5",
    "player/right/run6",
    "player/right/run7",
    "player/right/run8"
]

HERO_ANIM_JUMP_RIGHT = [
    "player/right/idle1"
]

HERO_ANIM_DIE_RIGHT = [
    "player/right/die1",
    "player/right/die2",
    "player/right/die3",
    "player/right/die4",
    "player/right/die5",
    "player/right/die6",
    "player/right/die7",
    "player/right/die8"
]

HERO_ANIM_SHOOT_RIGHT = [
    "player/right/shoot1",
    "player/right/shoot2",
    "player/right/shoot3",
    "player/right/shoot4",
    "player/right/shoot5"
]

# Animações do Herói - Esquerda
HERO_ANIM_IDLE_LEFT = [
    "player/left/idle1",
    "player/left/idle2",
    "player/left/idle3",
    "player/left/idle4",
    "player/left/idle5"
]

HERO_ANIM_RUN_LEFT = [
    "player/left/run1",
    "player/left/run2",
    "player/left/run3",
    "player/left/run4",
    "player/left/run5",
    "player/left/run6",
    "player/left/run7",
    "player/left/run8"
]

HERO_ANIM_JUMP_LEFT = [
    "player/left/idle1"
]

HERO_ANIM_DIE_LEFT = [
    "player/left/die1",
    "player/left/die2",
    "player/left/die3",
    "player/left/die4",
    "player/left/die5",
    "player/left/die6",
    "player/left/die7",
    "player/left/die8"
]

HERO_ANIM_SHOOT_LEFT = [
    "player/left/shoot1",
    "player/left/shoot2",
    "player/left/shoot3",
    "player/left/shoot4",
    "player/left/shoot5"
]

# Mantendo compatibilidade com código existente
HERO_ANIM_IDLE = HERO_ANIM_IDLE_RIGHT
HERO_ANIM_RUN = HERO_ANIM_RUN_RIGHT
HERO_ANIM_JUMP = HERO_ANIM_JUMP_RIGHT
HERO_ANIM_DIE = HERO_ANIM_DIE_RIGHT
HERO_ANIM_SHOOT = HERO_ANIM_SHOOT_RIGHT

# Configurações dos Inimigos
INIMIGOS = [
    {
        "tipo": "Snake",
        "anim_idle_right": ["enemy/right/idle1", "enemy/right/idle1", "enemy/right/idle1"],
        "anim_run_right": [
            "enemy/right/run1", "enemy/right/run2", "enemy/right/run3",
            "enemy/right/run4", "enemy/right/run5", "enemy/right/run6",
            "enemy/right/run7"
        ],
        "anim_die_right": [
            "enemy/right/die1", "enemy/right/die2", "enemy/right/die3",
            "enemy/right/die4", "enemy/right/die5", "enemy/right/die6",
            "enemy/right/die7"
        ],
        "anim_idle_left": ["enemy/left/idle1", "enemy/left/idle1", "enemy/left/idle1"],
        "anim_run_left": [
            "enemy/left/run1", "enemy/left/run2", "enemy/left/run3",
            "enemy/left/run4", "enemy/left/run5", "enemy/left/run6",
            "enemy/left/run7"
        ],
        "anim_die_left": [
            "enemy/left/die1", "enemy/left/die2", "enemy/left/die3",
            "enemy/left/die4", "enemy/left/die5", "enemy/left/die6",
            "enemy/left/die7"
        ],
        "x": 0,
        "y": CHAO_Y,
        "speed": 1,
        "sound": "snake",
        "scale": 1.6
    },
    {
        "tipo": "Gorgon",
        "anim_idle_right": [
            "enemy2/right/idle0,","enemy2/right/idle1", "enemy2/right/idle2",
            "enemy2/right/idle3","enemy2/right/idle4", "enemy2/right/idle5",
            "enemy2/right/idle6"
        ],
        "anim_run_right": [
            "enemy2/right/run1", "enemy2/right/run2", "enemy2/right/run3",
            "enemy2/right/run4", "enemy2/right/run5", "enemy2/right/run6",
            "enemy2/right/run7"
        ],
        "anim_die_right": [
            "enemy2/right/die1", "enemy2/right/die2", "enemy2/right/die3",
            "enemy2/right/die4","enemy2/right/die5","enemy2/right/die6",
            "enemy2/right/die9","enemy2/right/die8","enemy2/right/die7",
        ],
        "anim_idle_left": [
            "enemy2/left/idle0", "enemy2/left/idle1", "enemy2/left/idle2",
            "enemy2/left/idle3", "enemy2/left/idle4", "enemy2/left/idle5",
            "enemy2/left/idle6"
        ],
        "anim_run_left": [
            "enemy2/left/run1", "enemy2/left/run2", "enemy2/left/run3",
            "enemy2/left/run4", "enemy2/left/run5", "enemy2/left/run6",
            "enemy2/left/run7"
        ],
        "anim_die_left": [
            "enemy2/left/die1", "enemy2/left/die2","enemy2/left/die3",
            "enemy2/left/die4", "enemy2/left/die5","enemy2/left/die6",
            "enemy2/left/die7", "enemy2/left/die8","enemy2/left/die9"
        ],
        "x": 0,
        "y": 370,
        "speed": 2,
        "sound": "gorgon",
        "scale": 1.0
    },
    {
        "tipo": "Wolf",
        "anim_idle_right": ["enemy3/right/idle1"],
        "anim_run_right": [
            "enemy3/right/run1", "enemy3/right/run2", "enemy3/right/run3",
            "enemy3/right/run4", "enemy3/right/run5", "enemy3/right/run6",
            "enemy3/right/run7", "enemy3/right/run8", "enemy3/right/run9"
        ],
        "anim_jump_right": [
            "enemy3/right/jump1", "enemy3/right/jump2", "enemy3/right/jump3",
            "enemy3/right/jump4", "enemy3/right/jump5", "enemy3/right/jump6",
            "enemy3/right/jump7", "enemy3/right/jump8", "enemy3/right/jump9",
            "enemy3/right/jump10", "enemy3/right/jump11"
        ],
        "anim_die_right": ["enemy3/right/die1", "enemy3/right/die2"],
        "anim_idle_left": ["enemy3/left/idle1"],
        "anim_run_left": [
            "enemy3/left/run1", "enemy3/left/run2", "enemy3/left/run3",
            "enemy3/left/run4", "enemy3/left/run5", "enemy3/left/run6",
            "enemy3/left/run7", "enemy3/left/run8", "enemy3/left/run9"
        ],
        "anim_jump_left": [
            "enemy3/left/jump1", "enemy3/left/jump2", "enemy3/left/jump3",
            "enemy3/left/jump4", "enemy3/left/jump5", "enemy3/left/jump6",
            "enemy3/left/jump7", "enemy3/left/jump8", "enemy3/left/jump9",
            "enemy3/left/jump10", "enemy3/left/jump11"
        ],
        "anim_die_left": ["enemy3/left/die1", "enemy3/left/die2"],
        "x": 0,
        "y": 420,
        "speed": 1.5,
        "sound": "wolf",
        "scale": 0.7,
        "jump_force": -8,
        "jump_cooldown": 120
    }
]

# Configurações das Fases
FASES = [
    {
        "objetivo": 5,
        "inimigos": ["Snake"],
        "intervalo_spawn": 180
    },
    {
        "objetivo": 8,
        "inimigos": ["Snake", "Gorgon"],
        "intervalo_spawn": 150
    },
    {
        "objetivo": 12,
        "inimigos": ["Snake", "Gorgon", "Wolf"],
        "intervalo_spawn": 120
    }
]

# Configurações do Jogador
PLAYER_CONFIG = {
    "vidas": 3,
    "velocidade": 4,
    "forca_pulo": -10,
    "gravidade": 0.5,
    "velocidade_tiro": 10,
    "tempo_invencivel": 60
}

# Configurações de Partículas
PARTICLE_CONFIG = {
    "cores": [(255, 200, 0), (255, 100, 0), (255, 50, 0)],
    "tamanho_max": 5,
    "velocidade": 3,
    "vida": 30
}

# Configurações de Game Over
GAME_OVER_CONFIG = {
    "cor_texto": (255, 0, 0),
    "tamanho_fonte": 60,
    "cor_fundo": (0, 0, 0, 128)
}

# Configurações de HUD
HUD_CONFIG = {
    "cor_texto": (255, 255, 255),
    "tamanho_fonte": 32,
    "margem": 10
}