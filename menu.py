import pgzrun
from pgzero.builtins import Actor, Rect
import math

class Menu:
    def __init__(self):
        self.active = True
        self.contagem = None
        self.timer_contagem = 0
        self.cor_fundo = (0, 0, 0, 200)
        self.cor_texto = (255, 255, 255)
        self.timer_animacao = 0
        
    def draw(self, screen):
        if not self.active:
            return
        
        # Fundo escuro semi-transparente
        screen.draw.filled_rect(Rect((0, 0), (800, 480)), self.cor_fundo)
        
        if self.contagem is not None:
            # Desenha contagem regressiva
            contagem = str(max(1, 4 - int(self.timer_contagem / 60)))
            screen.draw.text(contagem, center=(400, 240), fontsize=120, 
                           color=(255, 215, 0), shadow=(2, 2))
        else:
            # Título com efeito de sombra
            screen.draw.text("Desert Hunter", center=(400, 100), fontsize=60,
                           color=(255, 215, 0), shadow=(2, 2))
            
            # Texto do tutorial com efeito pulsante
            pulso = math.sin(self.timer_animacao * 0.1) * 0.2 + 0.8
            
            # Tutorial de controles
            texto_tutorial = [
                "CONTROLES:",
                "W - Pular",
                "A/D - Mover Esquerda/Direita",
                "Clique do Mouse - Atirar",
                "ESC - Pausar"
            ]
            
            pos_y = 200
            for linha in texto_tutorial:
                screen.draw.text(linha, center=(400, pos_y), 
                               fontsize=30, color=self.cor_texto)
                pos_y += 40
            
            # Texto inicial com animação
            texto_iniciar = "Pressione ESPAÇO para Começar"
            escala_texto = 40 * pulso
            screen.draw.text(texto_iniciar, center=(400, 400), 
                           fontsize=int(escala_texto), color=(255, 215, 0))

    def update(self):
        self.timer_animacao += 1
        
        if self.contagem is not None:
            self.timer_contagem += 1
            if self.timer_contagem >= 180:  # 3 segundos (60 frames por segundo)
                self.active = False
                self.contagem = None

    def handle_input(self, key):
        if hasattr(key, 'name'):
            k = key.name.lower()
        else:
            k = str(key).lower()

        if k == "space" and self.contagem is None:
            self.contagem = True
            self.timer_contagem = 0
            try:
                from pgzero.builtins import sounds
                if hasattr(sounds, "menu_select"):
                    sounds.menu_select.play()
            except Exception:
                pass
            return "novo jogo"
        return None