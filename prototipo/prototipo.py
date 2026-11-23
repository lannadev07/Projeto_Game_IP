
import pygame
import sys

# Inicialização
pygame.init()

# Configurações da janela
LARGURA = 960
ALTURA = 540
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Eleninho")

RELOGIO = pygame.time.Clock()
FPS = 60

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (60, 120, 220)
VERDE = (50, 180, 80)
AMARELO = (255, 220, 70)
MARROM = (130, 85, 45)
AREIA = (230, 190, 120)
LARANJA = (230, 130, 50)
VERMELHO = (220, 60, 60)

# Fontes
FONTE = pygame.font.SysFont("Arial", 28)
FONTE_TITULO = pygame.font.SysFont("Arial", 60, bold=True)
FONTE_HUD = pygame.font.SysFont("Arial", 22)


# CLASSE DO JOGADOR
class Player:

    def __init__(self):
        self.rect = pygame.Rect(80, 395, 35, 55)

        self.velocidade_x = 5
        self.velocidade_y = 0

        self.forca_pulo = -14
        self.gravidade = 0.7

        self.no_chao = False

    def mover(self, teclas):

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade_x

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade_x

    def pular(self):

        if self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

    def aplicar_gravidade(self, plataformas):

        self.velocidade_y += self.gravidade
        self.rect.y += self.velocidade_y

        self.no_chao = False

        for plataforma in plataformas:

            if self.rect.colliderect(plataforma):

                if self.velocidade_y > 0:
                    self.rect.bottom = plataforma.top
                    self.velocidade_y = 0
                    self.no_chao = True

                elif self.velocidade_y < 0:
                    self.rect.top = plataforma.bottom
                    self.velocidade_y = 0

    # Faz o personagem voltar ao início
    # quando cair em um vão
    def voltar_inicio(self):

        self.rect.x = 80
        self.rect.y = 395
        self.velocidade_y = 0
        self.no_chao = False

    def desenhar(self, tela, camera):

        pygame.draw.rect(
            tela,
            AZUL,
            (self.rect.x - camera, self.rect.y, self.rect.width, self.rect.height)
        )

        # Cabeça do personagem
        pygame.draw.circle(
            tela,
            (230, 190, 150),
            (self.rect.centerx - camera, self.rect.y + 10),
            12
        )


# CLASSE DOS COLETÁVEIS
class Collectible:

    def __init__(self, x, y, tipo, cor, simbolo):

        self.rect = pygame.Rect(x, y, 25, 25)
        self.tipo = tipo
        self.cor = cor
        self.simbolo = simbolo
        self.coletado = False

    def desenhar(self, tela, camera):

        if not self.coletado:

            pygame.draw.circle(
                tela,
                self.cor,
                (self.rect.centerx - camera, self.rect.centery),
                13
            )

            texto = FONTE_HUD.render(self.simbolo, True, PRETO)

            tela.blit(
                texto,
                (self.rect.centerx - camera - 7, self.rect.centery - 11)
            )


# TELA INICIAL
def tela_inicial():

    while True:

        TELA.fill((180, 130, 80))

        #Céu
        pygame.draw.rect(TELA, (240, 180, 110), (0, 0, LARGURA, 350))

        #Sol
        pygame.draw.circle(TELA, AMARELO, (800, 100), 55)

        #Chão
        pygame.draw.rect(TELA, AREIA, (0, 350, LARGURA, 190))

        #Cactos
        pygame.draw.rect(TELA, VERDE, (150, 270, 25, 80))
        pygame.draw.rect(TELA, VERDE, (130, 295, 20, 10))
        pygame.draw.rect(TELA, VERDE, (175, 310, 20, 10))

        # Título
        titulo = FONTE_TITULO.render("ELNIGMA", True, PRETO)

        TELA.blit(
            titulo,
            (LARGURA // 2 - titulo.get_width() // 2, 100)
        )

        # Botão iniciar
        botao = pygame.Rect(370, 300, 220, 65)

        pygame.draw.rect(TELA, VERDE, botao, border_radius=12)

        texto = FONTE.render("INICIAR", True, BRANCO)

        TELA.blit(
            texto,
            (botao.centerx - texto.get_width() // 2,
             botao.centery - texto.get_height() // 2)
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if botao.collidepoint(evento.pos):
                    return

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    return

        pygame.display.flip()
        RELOGIO.tick(FPS)


# PRIMEIRA FASE
def primeira_fase():

    jogador = Player()

    camera = 0

    # Plataformas do cenário
    # Alguns espaços ficam sem plataformas
    plataformas = [

        pygame.Rect(0, 450, 400, 90),

        pygame.Rect(480, 450, 300, 90),

        pygame.Rect(850, 450, 350, 90),

        pygame.Rect(1270, 450, 350, 90),

        pygame.Rect(1700, 450, 300, 90)

    ]

    # Itens disponíveis
    coletaveis = [

        Collectible(220, 410, "agua", AZUL, "a"),

        Collectible(600, 410, "comida", AMARELO, "c"),

        Collectible(1000, 410, "kit", VERMELHO, "+")

    ]

    # Contadores
    inventario = {
        "agua": 0,
        "comida": 0,
        "kit": 0
    }

    rodando = True

    while rodando:

        RELOGIO.tick(FPS)

        # Eventos
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_SPACE or evento.key == pygame.K_UP:
                    jogador.pular()

                # Coletar itens
                if evento.key == pygame.K_e:

                    for item in coletaveis:

                        if not item.coletado:

                            area_coleta = jogador.rect.inflate(60, 60)

                            if area_coleta.colliderect(item.rect):

                                item.coletado = True

                                inventario[item.tipo] += 1

        # Movimentação
        teclas = pygame.key.get_pressed()

        jogador.mover(teclas)

        jogador.aplicar_gravidade(plataformas)

        # Impede o jogador de sair pela esquerda
        if jogador.rect.left < 0:
            jogador.rect.left = 0

        # MECÂNICA DE QUEDA:
        # Se o personagem cair para fora da tela,
        # ele volta ao início da fase.
        if jogador.rect.top > ALTURA:

            jogador.voltar_inicio()

        # Câmera acompanha o jogador
        camera = jogador.rect.centerx - LARGURA // 2

        if camera < 0:
            camera = 0

        # Desenho do cenário
        TELA.fill((240, 190, 120))

        # Sol
        pygame.draw.circle(TELA, AMARELO, (800 - camera // 4, 90), 45)

        # Montanhas
        pygame.draw.polygon(
            TELA,
            (190, 120, 80),
            [
                (100 - camera // 3, 350),
                (300 - camera // 3, 170),
                (500 - camera // 3, 350)
            ]
        )

        # Chão e plataformas
        for plataforma in plataformas:

            pygame.draw.rect(
                TELA,
                MARROM,
                (
                    plataforma.x - camera,
                    plataforma.y,
                    plataforma.width,
                    plataforma.height
                )
            )

            pygame.draw.rect(
                TELA,
                AREIA,
                (
                    plataforma.x - camera,
                    plataforma.y,
                    plataforma.width,
                    12
                )
            )

        # Cactos decorativos
        for x in [300, 700, 1100, 1500, 1850]:

            pygame.draw.rect(
                TELA,
                VERDE,
                (x - camera, 370, 20, 80)
            )

            pygame.draw.rect(
                TELA,
                VERDE,
                (x - camera - 15, 390, 15, 10)
            )

            pygame.draw.rect(
                TELA,
                VERDE,
                (x - camera + 20, 405, 15, 10)
            )

        # Coletáveis
        for item in coletaveis:
            item.desenhar(TELA, camera)

        # Jogador
        jogador.desenhar(TELA, camera)

        # HUD
        pygame.draw.rect(TELA, PRETO, (10, 10, 300, 105), border_radius=8)

        texto_agua = FONTE_HUD.render(
            f"Água: {inventario['agua']}",
            True,
            BRANCO
        )

        texto_comida = FONTE_HUD.render(
            f"Comida: {inventario['comida']}",
            True,
            BRANCO
        )

        texto_kit = FONTE_HUD.render(
            f"Kit: {inventario['kit']}",
            True,
            BRANCO
        )

        TELA.blit(texto_agua, (25, 20))
        TELA.blit(texto_comida, (25, 48))
        TELA.blit(texto_kit, (25, 76))

        # Instruções
        instrucoes = FONTE_HUD.render(
            "A/D ou setas: mover | ESPAÇO: pular | E: coletar",
            True,
            PRETO
        )

        TELA.blit(instrucoes, (320, 15))

        pygame.display.flip()


# PROGRAMA PRINCIPAL
def main():

    tela_inicial()

    primeira_fase()


main()
