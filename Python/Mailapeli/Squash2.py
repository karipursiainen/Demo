# -*- coding: utf-8 -*-
import pygame, sys, random
"""
Squash
Tekijä: Kari Pursiainen
Pvm: 12/2017

Ohjeet: Estä pallon pääsy vasempaan laitaan 'lyömällä' pallo takaisin mailalla.
        Jos pallo osuu vasempaan laitaan - peli päättyy
        Mailaa voi liikuttaa ylös/alas/vasemmalle/oikealle nuolinäppäimillä
        (oikealle 1/3 ikkunan leveydestä)
        Ylösalasin liikkuva 'linssi' muuttaa pallon liikerataa
"""


naytto = pygame.display.set_mode((640, 400))
pygame.display.set_caption("Squash")

# ladataan kuvat ym
maila = pygame.image.load("Maila.png")
mailaPun = pygame.image.load("MailaPun.png")
pallo = pygame.image.load("Pallo.png")
linssi = pygame.image.load("Linssi.png")

class Vakio:
    YLOS = 1
    ALAS = 2
    VASEN = 3
    OIKEA = 4
    MAILANOPEUS = 3
    PALLONOPEUS = 3
    LINSSINOPEUS = 1
    FPS = 40
    KERROIN = 1

def kontrolli(suunta,mailasijainti,pallosijainti):
    # kontrolli, eli käyttäjän toimintojen kuuntelu ja niihin reagointi
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            exit()
        # toimintojen käsittely
    tapahtuma = pygame.key.get_pressed()

    # Maila ylös
    if tapahtuma[pygame.K_UP] or tapahtuma[pygame.K_KP8]:
        mailasijainti[1] = mailasijainti[1] - Vakio.MAILANOPEUS

    # Maila alas
    if tapahtuma[pygame.K_DOWN] or tapahtuma[pygame.K_KP2]:
        mailasijainti[1] = mailasijainti[1] + Vakio.MAILANOPEUS

    # Maila vasemmalle
    if tapahtuma[pygame.K_LEFT] or tapahtuma[pygame.K_KP4]:
        mailasijainti[0] = mailasijainti[0] - Vakio.MAILANOPEUS

    # Maila oikealle
    if tapahtuma[pygame.K_RIGHT] or tapahtuma[pygame.K_KP6]:
        mailasijainti[0] = mailasijainti[0] + Vakio.MAILANOPEUS


def logiikka(mailasijainti,pallosijainti,pallosuunta,gameOver,linssisijainti,linssisuunta):
    #  "logiikka, eli pelin toimintojen suorittaminen; mm. liikkeiden ja törmäysten tarkastaminen"

    # Maila osuu ikkunan reunaan
    # Yläreuna
    if mailasijainti[1] < 0:
        mailasijainti[1] = mailasijainti[1] + Vakio.MAILANOPEUS
    # Alareuna
    if mailasijainti[1] > naytto.get_height() - maila.get_height():
        mailasijainti[1] = mailasijainti[1] - Vakio.MAILANOPEUS
    # Vasen reuna
    if mailasijainti[0] < 0:
        mailasijainti[0] = mailasijainti[0] + Vakio.MAILANOPEUS
    # Oikea reuna - maila ei liiku oikealle kuin 1/3 ikkunan leveydestä
    if mailasijainti[0] > naytto.get_width()/3:
        mailasijainti[0] = mailasijainti[0] - Vakio.MAILANOPEUS

    # Linssin liike
    if linssisuunta[0] == Vakio.YLOS:
        linssisijainti[1] = linssisijainti[1] - Vakio.LINSSINOPEUS
    if linssisuunta[0] == Vakio.ALAS:
        linssisijainti[1] = linssisijainti[1] + Vakio.LINSSINOPEUS
    # Linssi osuu ikkunan reunaan
    # Yläreuna
    if linssisijainti[1] < 0:
        linssisuunta[0] = Vakio.ALAS
    # Alareuna
    if linssisijainti[1] > naytto.get_height() - linssi.get_height():
        linssisuunta[0] = Vakio.YLOS

    # Pallon liike
    # pallosuunta[0] vasen/oikea, pallosuunta[1] ylös/alas
    # Vasemmalle ylös
    if pallosuunta[0] == Vakio.VASEN and pallosuunta[1] == Vakio.YLOS:
        pallosijainti[0] = pallosijainti[0] - Vakio.PALLONOPEUS
        pallosijainti[1] = pallosijainti[1] - Vakio.PALLONOPEUS*Vakio.KERROIN
    # Vasemmalle alas
    if pallosuunta[0] == Vakio.VASEN and pallosuunta[1] == Vakio.ALAS:
        pallosijainti[0] = pallosijainti[0] - Vakio.PALLONOPEUS
        pallosijainti[1] = pallosijainti[1] + Vakio.PALLONOPEUS*Vakio.KERROIN
    # Oikealle ylös
    if pallosuunta[0] == Vakio.OIKEA and pallosuunta[1] == Vakio.YLOS:
        pallosijainti[0] = pallosijainti[0] + Vakio.PALLONOPEUS
        pallosijainti[1] = pallosijainti[1] - Vakio.PALLONOPEUS*Vakio.KERROIN
    # Oikealle alas
    if pallosuunta[0] == Vakio.OIKEA and pallosuunta[1] == Vakio.ALAS:
        pallosijainti[0] = pallosijainti[0] + Vakio.PALLONOPEUS
        pallosijainti[1] = pallosijainti[1] + Vakio.PALLONOPEUS*Vakio.KERROIN
    #print (Vakio.PALLONOPEUS*Vakio.KERROIN)
    # Pallo osuu ikkunan reunaan
    # Yläreuna
    if pallosijainti[1] < 0:
        pallosuunta[1] = Vakio.ALAS
    # Alareuna
    if pallosijainti[1] > naytto.get_height() - pallo.get_height():
        pallosuunta[1] = Vakio.YLOS
    # Vasen reuna - peli loppuu
    if pallosijainti[0] < 0 - pallo.get_width():
        gameOver[0] = True
    # Oikea reuna - maila ei liiku oikealle kuin 1/2 ikkunan leveydestä
    if pallosijainti[0] > naytto.get_width()-pallo.get_width()/2:
        pallosuunta[0] = Vakio.VASEN

    # Pallo osuu mailaan
    if pallosijainti[0] >= mailasijainti[0] and pallosijainti[0] <= mailasijainti[0] + maila.get_width() and pallosijainti[1] >= mailasijainti[1] and pallosijainti[1] <= mailasijainti[1]+maila.get_height():
        pallosuunta[0] = Vakio.OIKEA
    # Pallon kimpoamiskulma muuttuu
    # Arvo kulma/kerroin

    # Pallo osuu linssiin
    if pallosijainti[0] >= linssisijainti[0] and pallosijainti[0] <= linssisijainti[0] + linssi.get_width():
        if pallosijainti[1] >= linssisijainti[1] and pallosijainti[1] <= linssisijainti[1] + linssi.get_height():
            Vakio.KERROIN = 1 + random.randint(-4,4)/4

def piirtaminen(mailasijainti,pallosijainti,linssisijainti):
    # "piirtaminen, eli pelin grafiikan piirtäminen käyttäjälle"
    naytto.fill((0, 0, 0))
    naytto.blit(maila, mailasijainti)
    naytto.blit(pallo, pallosijainti)
    naytto.blit(linssi, linssisijainti)
    pygame.display.flip()

def main():
    # "pelihahmojen ym. luominen"
    suunta = [Vakio.YLOS]
    palloSuunta = [Vakio.VASEN,Vakio.YLOS]
    linssiSuunta = [Vakio.YLOS]
    mailaSijainti = [naytto.get_width()/6,naytto.get_height()/2-maila.get_height()/2]
    palloSijainti = [naytto.get_width()-pallo.get_width()/2,naytto.get_height()/2-pallo.get_height()/2]
    linssiSijainti = [naytto.get_width()/2,naytto.get_height()/2-linssi.get_height()/2]
    gameOver = [False]
    kello = pygame.time.Clock()

    while True:
        kontrolli(suunta,mailaSijainti,palloSijainti)
        logiikka(mailaSijainti,palloSijainti,palloSuunta,gameOver,linssiSijainti,linssiSuunta)
        piirtaminen(mailaSijainti,palloSijainti,linssiSijainti)

        kello.tick(Vakio.FPS)

        if gameOver[0]:
            naytto.blit(mailaPun, mailaSijainti)
            pygame.display.flip()
            pygame.time.wait(3000)
            break

# kun kaikki on valmista, käynnistetään peli
main()
