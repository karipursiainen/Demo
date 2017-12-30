# -*- coding: utf-8 -*-
import pygame, random, sys

"""
Matopeli
Tekijä: Kari Pursiainen
Pvm: 12/2017

Ohjeet: Muuta madon suuntaa nuolinäppäimillä.
        Jos mato osuu numeroon, kasvaa madon pituus vastaavalla määrällä
        Peli päättyy jos:
           - Mato osuu ikkunan reunaan
           - Mato osuu itseensä
"""

def arvoArvoPaikka():
    arvo[0] = random.randint(1, 4)
    paikkax = int(random.randint(0, 620) / 20) * 20
    paikkay = int(random.randint(0, 380) / 20) * 20
    paikkaxy[0] = paikkax
    paikkaxy[1] = paikkay
    osuma[0] = False


def kontrolli(suunta):
    tapahtuma = pygame.event.poll()
    if tapahtuma.type == pygame.QUIT:
        exit()

    if tapahtuma.type == pygame.KEYDOWN:
        if tapahtuma.key == pygame.K_LEFT and suunta[0] != 2:
            suunta[0] = 1
        if tapahtuma.key == pygame.K_RIGHT and suunta[0] != 1:
            suunta[0] = 2
        if tapahtuma.key == pygame.K_UP and suunta[0] != 4:
            suunta[0] = 3
        if tapahtuma.key == pygame.K_DOWN and suunta[0] != 3:
            suunta[0] = 4

def logiikka(suunta, mato, karjen_sijainti, pituus):
    if suunta[0] == 1:
        karjen_sijainti[0] = karjen_sijainti[0] - 20
    if suunta[0] == 2:
        karjen_sijainti[0] = karjen_sijainti[0] + 20
    if suunta[0] == 3:
        karjen_sijainti[1] = karjen_sijainti[1] - 20
    if suunta[0] == 4:
        karjen_sijainti[1] = karjen_sijainti[1] + 20

    # Kärki osuu numeroon
    if karjen_sijainti[0] == paikkaxy[0] and karjen_sijainti[1] == paikkaxy[1]:
        pituus[0] = pituus[0] + arvo[0]
        osuma[0] = True

    mato.append((karjen_sijainti[0], karjen_sijainti[1]))
    if pituus[0] < len(mato):
        mato.pop(0)

def peliOhi (mato, karjen_sijainti):
    gameOver[0] = True
    for pala in mato:
        pygame.draw.circle(naytto, (255, 0, 0), (pala[0] + 10, pala[1] + 10), 10, 0)
        karjen_sijainti[0] = karjen_sijainti[0] + 20
    pygame.display.flip()

def piirtaminen(mato, karjen_sijainti,pituus):
    naytto.fill((0, 0, 0))
    osuiMatoon = False

    # Mato osuu itseensä -> peli päättyy
    # (-2) ei verrata itseensä. Kärjen koord. listan viimeinen alkio
    for i in range(len(mato)-2):
        if karjen_sijainti[0] == mato[i][0] and karjen_sijainti[1] == mato[i][1] and len(mato) >= pituus[0]:
            peliOhi(mato,karjen_sijainti)
            return

    # Kärki osuu ikkunan reunaan -> peli päättyy
    if karjen_sijainti[0] < 0 or karjen_sijainti[1] < 0 or karjen_sijainti[0] > naytto.get_width() - 20 or karjen_sijainti[1] > naytto.get_height() - 20:
        peliOhi(mato,karjen_sijainti)
        return
    else:
        for pala in mato:
            pygame.draw.circle(naytto, (0, 255, 0), (pala[0] + 10, pala[1] + 10), 10, 0)
    # Ei osu numeroon
    if osuma[0] == False:
        pygame.draw.circle(naytto, (255, 255, 255), (paikkaxy[0] + 10, paikkaxy[1] + 10), 10, 0)
        naytettava_teksti = fontti.render(str(arvo[0]), True, (255, 0, 0))
    else: # Osuu numeroon
        pygame.draw.circle(naytto, (0, 255, 0), (paikkaxy[0] + 10, paikkaxy[1] + 10), 10,0)
        naytettava_teksti = fontti.render("", True, (0, 0, 0))
        # Arpoo uuden numeron/paikan
        # Ei saa osua matoon
        while True:
            osuiMatoon = False
            arvoArvoPaikka()
            for pala in mato:
                if paikkaxy[0] == pala[0] and paikkaxy[1] == pala[1]:
                    print(paikkaxy)
                    osuiMatoon = True
            if osuiMatoon == False:
                break

        pygame.draw.circle(naytto, (255, 255, 255), (paikkaxy[0], paikkaxy[1]), 10, 0)
        naytettava_teksti = fontti.render(str(arvo[0]), True, (255, 0, 0))

    naytto.blit(naytettava_teksti, (paikkaxy[0]+6, paikkaxy[1]+3))

    pygame.display.flip()

def uusiPeli():
    fontti = pygame.font.Font(None, 48)
    naytettava_teksti = fontti.render("Uusi peli k/e?", True, (255, 255, 255))
    naytto.blit(naytettava_teksti, (naytto.get_width() * 0.3, naytto.get_height() * 0.4))
    pygame.display.flip()

    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            exit()

        # toimintojen käsittely
        if tapahtuma.type == pygame.KEYDOWN:

            # Uusi peli?
            # Lopetus
            if tapahtuma.key == pygame.K_e:
                exit()

            # Halutaan uusi peli
            if tapahtuma.key == pygame.K_k:
                newGame[0] = True
                return

def main():
    kello = pygame.time.Clock()
    mato = []
    suunta = [1]
    karjen_sijainti = [300, 200]
    pituus = [5]
    arvoArvoPaikka()

    while True:
        kontrolli(suunta)
        logiikka(suunta, mato, karjen_sijainti, pituus)
        piirtaminen(mato, karjen_sijainti,pituus)
        kello.tick(10)

        if gameOver[0] == True:
            break;

while True:
    naytto = pygame.display.set_mode((640, 400))
    pygame.display.set_caption("Matopeli")
    pygame.font.init()
    fontti = pygame.font.Font(None, 24)

    arvo = [1]
    paikkax = 0
    paikkay = 0
    paikkaxy = [paikkax, paikkay]
    osuma = [False]
    gameOver = [False]
    newGame = [False]

    main()
    while True:
        uusiPeli()
        if newGame[0] == True:
            break
