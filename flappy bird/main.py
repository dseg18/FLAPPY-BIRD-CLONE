import pygame
import random
import sys

pygame.init()

# pantalla
ANC = 400
ALT = 600
pant = pygame.display.set_mode((ANC, ALT))
pygame.display.set_caption("Flappy Bird")

# tiempo
clk = pygame.time.Clock()

# fuente
fnt = pygame.font.SysFont(None, 40)

#sprites
paj_img = pygame.image.load("imgs/paj.png").convert_alpha()
paj_img = pygame.transform.scale(paj_img, (80, 80))

tub_img = pygame.image.load("imgs/tub.png").convert_alpha()
tub_img = pygame.transform.scale(tub_img, (100, 400))

tub_inv = pygame.transform.flip(tub_img, False, True)

#variables
def reiniciar():
    return {
        "paj_y": 300,
        "vel": 0,
        "tub_x": ANC,
        "alt_tub": random.randint(100, 400),
        "pts": 0,
        "vel_j": 4
    }

juego = reiniciar()

grv = 0.5
sal = -8
anc_tub = 70
gap = 150
paj_x = 50

est = "inicio"

#funcions
def dib_tub(x, alt):
    pant.blit(tub_inv, (x, alt - 400))
    pant.blit(tub_img, (x, alt + gap))


#colision
def colision(paj_y, tub_x, alt_tub):

    margen = 10        # ajusta dificultad
    tam_paj = 80
    hit = 28           # 🔥 tamaño real del cuerpo (ajustado a tu sprite)

    izq = paj_x + (tam_paj//2 - hit)
    der = paj_x + (tam_paj//2 + hit)
    arriba = paj_y + (tam_paj//2 - hit) + margen
    abajo = paj_y + (tam_paj//2 + hit) - margen

    # bordes pantalla
    if arriba < 0 or abajo > ALT:
        return True

    # colisión horizontal real
    if der > tub_x and izq < tub_x + anc_tub:

        # tubo arriba
        if arriba < alt_tub:
            return True

        # tubo abajo
        if abajo > alt_tub + gap:
            return True

    return False


#loop
while True:
    pant.fill((135, 206, 250))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:

                if est == "inicio":
                    est = "jugando"
                    juego = reiniciar()

                elif est == "jugando":
                    juego["vel"] = sal

                elif est == "gameover":
                    est = "inicio"

    if est == "inicio":
        txt = fnt.render("Presiona ESPACIO", True, (255,255,255))
        pant.blit(txt, (70, 250))

    elif est == "jugando":

        juego["vel"] += grv
        juego["paj_y"] += juego["vel"]

        juego["tub_x"] -= juego["vel_j"]

        if juego["tub_x"] < (-anc_tub):
            juego["tub_x"] = ANC
            juego["alt_tub"] = random.randint(100, 400)
            juego["pts"] += 1
            juego["vel_j"] += 0.7

        pant.blit(paj_img, (paj_x, juego["paj_y"]))
        dib_tub(juego["tub_x"], juego["alt_tub"])

        if colision(juego["paj_y"], juego["tub_x"], juego["alt_tub"]):
            est = "gameover"

        txt = fnt.render(f"Puntos: {juego['pts']}", True, (255,255,255))
        pant.blit(txt, (10, 10))

    elif est == "gameover":
        t1 = fnt.render("GAME OVER", True, (255,255,255))
        t2 = fnt.render(f"Puntos: {juego['pts']}", True, (255,255,255))
        t3 = fnt.render("ESPACIO para reiniciar", True, (255,255,255))

        pant.blit(t1, (110, 200))
        pant.blit(t2, (120, 250))
        pant.blit(t3, (30, 300))

    pygame.display.update()
    clk.tick(60)
