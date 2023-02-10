import pygame
import os
import sys
pygame.init()
pygame.font.init()   # Initializare librarie de fonturi
pygame.mixer.init()  # Initializare librarie sunete
# Game Window
WIDTH = 900
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game1")
Border = pygame.Rect(WIDTH//2 - 5, 0, 1, HEIGHT)

FPS = 60
VEL = 5  # Velocitate miscare
Glont_VEL = 7  # Velocitate gloante
Gloante_Max = 3  # Anti-spam gloante
# Lovituri
sunet_hit = pygame.mixer.Sound(os.path.join('p3 images', 'sunet_hit.mp3'))
sunet_glont = pygame.mixer.Sound(os.path.join('p3 images', 'sunet_glont.mp3'))
galben_hit = pygame.USEREVENT+1
rosu_hit = pygame.USEREVENT+2

font_viata = pygame.font.SysFont('helvetica', 25)
winner_font = pygame.font.SysFont('helvetica', 30)
# Dimensiuni Nave
nava_width = 55
nava_height = 40
# Nave
nava_galbena_img = pygame.image.load(os.path.join('p3 images', 'spaceship_yellow2.png'))
nava_galbena = pygame.transform.rotate(pygame.transform.scale(nava_galbena_img, (nava_width, nava_height)), 270)
nava_rosie_img = pygame.image.load(os.path.join('p3 images', 'spaceship_red2.png'))
nava_rosie = pygame.transform.rotate(pygame.transform.scale(nava_rosie_img, (nava_width, nava_height)), 90)
# Background
BG_image = pygame.transform.scale(pygame.image.load(os.path.join('p3 images', 'space2.png')), (WIDTH, HEIGHT))

# Culori
albastru = (0, 0, 255)
alb = (255, 255, 255)
rosu = (255, 0, 0)
galben = (255, 255, 0)
negru = (0, 0, 0)


def draw_window(rect_rosu, rect_galben, gloante_rosu, gloante_galben, viata_galben, viata_rosu):
    window.blit(BG_image, (0, 0))
    pygame.draw.rect(window, negru, Border)

    text_viata_rosu = font_viata.render("Viata: " + str(viata_rosu), 1, rosu)
    text_viata_galben = font_viata.render("Viata: " + str(viata_galben), 1, galben)

    window.blit(text_viata_rosu, (WIDTH - text_viata_rosu.get_width() - 10, 10))
    window.blit(text_viata_galben, (10, 10))

    window.blit(nava_galbena, (rect_galben.x, rect_galben.y))
    window.blit(nava_rosie, (rect_rosu.x, rect_rosu.y))

    for glont in gloante_galben:
        pygame.draw.rect(window, galben, glont)

    for glont in gloante_rosu:
        pygame.draw.rect(window, rosu, glont)

    pygame.display.update()


def control_nava_galbena(taste_apasate, rect_galben):
    if taste_apasate[pygame.K_a] and rect_galben.x - VEL > 0:  # Stanga
        rect_galben.x -= VEL
    if taste_apasate[pygame.K_d] and rect_galben.x + VEL + rect_galben.width < Border.x:  # Dreapta
        rect_galben.x += VEL
    if taste_apasate[pygame.K_w] and rect_galben.y - VEL > 0:  # Sus
        rect_galben.y -= VEL
    if taste_apasate[pygame.K_s] and rect_galben.y + VEL + rect_galben.height < HEIGHT:  # Jos
        rect_galben.y += VEL


def control_nava_rosie(taste_apasate, rect_rosu):
    if taste_apasate[pygame.K_LEFT] and rect_rosu.x - VEL > Border.x + Border.width:  # Stanga
        rect_rosu.x -= VEL
    if taste_apasate[pygame.K_RIGHT] and rect_rosu.x + VEL + rect_rosu.width < WIDTH:  # Dreapta
        rect_rosu.x += VEL
    if taste_apasate[pygame.K_UP] and rect_rosu.y - VEL > 0:  # Sus
        rect_rosu.y -= VEL
    if taste_apasate[pygame.K_DOWN] and rect_rosu.y + VEL + rect_rosu.height < HEIGHT:  # Jos
        rect_rosu.y += VEL


def control_gloante(gloante_galben, gloante_rosu, rect_galben, rect_rosu):
    for glont in gloante_galben:
        glont.x += Glont_VEL
        if rect_rosu.colliderect(glont):
            pygame.event.post(pygame.event.Event(rosu_hit))
            gloante_galben.remove(glont)
        elif glont.x > WIDTH:
            gloante_galben.remove(glont)

    for glont in gloante_rosu:
        glont.x -= Glont_VEL
        if rect_galben.colliderect(glont):
            pygame.event.post(pygame.event.Event(galben_hit))
            gloante_rosu.remove(glont)
        elif glont.x < 0:
            gloante_rosu.remove(glont)


def winner(text):
    winner_extragere = winner_font.render(text, 1, alb)
    window.blit(
        winner_extragere, (WIDTH/2 - winner_extragere.get_width()/2, HEIGHT/2 - winner_extragere.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    rect_rosu = pygame.Rect(700, 300, nava_width, nava_height)
    rect_galben = pygame.Rect(100, 300, nava_width, nava_height)
    # Gloante
    gloante_rosu = []
    gloante_galben = []
    # Viata
    viata_rosu = 10
    viata_galben = 10

    winner_text = ""
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(gloante_galben) < Gloante_Max:
                    glont = pygame.Rect(
                        rect_galben.x + rect_galben.width, rect_galben.y + rect_galben.height//2 - 2, 10, 5)
                    gloante_galben.append(glont)
                    sunet_glont.play()

                if event.key == pygame.K_RCTRL and len(gloante_rosu) < Gloante_Max:
                    glont = pygame.Rect(rect_rosu.x, rect_rosu.y + rect_rosu.height//2 - 2, 10, 5)
                    gloante_rosu.append(glont)
                    sunet_glont.play()

            if event.type == galben_hit:
                viata_galben -= 1
                sunet_hit.play()

            if event.type == rosu_hit:
                viata_rosu -= 1
                sunet_hit.play()
        if viata_rosu <= 0:
            winner_text = "Galben a castigat!"
        if viata_galben <= 0:
            winner_text = "Rosu a castigat!"
        if winner_text != "":
            winner(winner_text)
            break

        taste_apasate = pygame.key.get_pressed()
        control_nava_galbena(taste_apasate, rect_galben)
        control_nava_rosie(taste_apasate, rect_rosu)
        control_gloante(gloante_galben, gloante_rosu, rect_galben, rect_rosu)
        draw_window(rect_rosu, rect_galben, gloante_rosu, gloante_galben, viata_galben, viata_rosu)

    main()


if __name__ == "__main__":
    main()
