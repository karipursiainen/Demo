# -*- coding: utf-8 -*-
import pygame, sys, random

"""
Squash
Tekijä: Kari Pursiainen
Pvm: 12/2017

Ohjeet: Estä pallon pääsy vasempaan laitaan 'lyömällä' pallo takaisin mailalla.
        Jos pallo osuu vasempaan laitaan - peli päättyy
        Mailaa voi liikuttaa ylös/alas/vasemmalle/oikealle nuolinäppäimillä
        Pallon osuminen mailaan muuttaa pallon liikerataa
"""

naytto = pygame.display.set_mode((640, 400))
pygame.display.set_caption("Squash")
pygame.font.init()
fontti = pygame.font.Font(None, 48)

# ladataan kuvat ym
mailaPic = pygame.image.load("Maila.png")
mailaPunPic = pygame.image.load("MailaPun.png")
palloPic = pygame.image.load("Pallo.png")

class Vakio:
    YLOS = 1
    ALAS = 2
    VASEN = 3
    OIKEA = 4
    FPS = 40
    KERROIN = 1


class Mailapeli:
    def __init__(self,naytto,kuva,suunta=[Vakio.VASEN,Vakio.YLOS], sijainti=[0,0],newGame=[False,False]):
        self.suunta = suunta
        self.sijainti = sijainti
        self.kuva = kuva
        self.newGame = newGame
        self.naytto = naytto

    # Kontrolli
    def painaNappainta(self, nopeus = 1):
        # kontrolli, eli käyttäjän toimintojen kuuntelu ja niihin reagointi
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

        # toimintojen käsittely
        tapahtuma = pygame.key.get_pressed()

        # ylös
        if tapahtuma[pygame.K_UP] or tapahtuma[pygame.K_KP8]:
            self.sijainti[1] = self.sijainti[1] - nopeus

        # alas
        if tapahtuma[pygame.K_DOWN] or tapahtuma[pygame.K_KP2]:
            self.sijainti[1] = self.sijainti[1] + nopeus

        # vasemmalle
        if tapahtuma[pygame.K_LEFT] or tapahtuma[pygame.K_KP4]:
            self.sijainti[0] = self.sijainti[0] - nopeus

        # oikealle
        if tapahtuma[pygame.K_RIGHT] or tapahtuma[pygame.K_KP6]:
            self.sijainti[0] = self.sijainti[0] + nopeus

        self.osuuIkkunanReunaan(nopeus)

    def uusiPeli(self):
        naytettava_teksti = fontti.render("Uusi peli k/e?", True, (255, 255, 255))
        self.naytto.blit(naytettava_teksti, (self.naytto.get_width() * 0.4, self.naytto.get_height() * 0.4))
        pygame.display.flip()

        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

            # toimintojen käsittely
            if tapahtuma.type == pygame.KEYDOWN:

                # Uusi peli?
                if tapahtuma.key == pygame.K_e:
                    exit()

                # Halutaan uusi peli
                if tapahtuma.key == pygame.K_k:
                    self.newGame[1] = True
                    return

    # Logiikka
    def osuuIkkunanReunaan(self,nopeus=1):
        # osuu ikkunan reunaan
        # Yläreuna
        if self.sijainti[1] < 0:
            self.sijainti[1] = self.sijainti[1] + nopeus
        # Alareuna
        if self.sijainti[1] > self.naytto.get_height() - self.kuva.get_height():
            self.sijainti[1] = self.sijainti[1] - nopeus
        # Vasen reuna - Jos kohde osuu reunaan ja peli päättyy sen vuoksi -> newGame == True
        if self.sijainti[0] < 0 and self.newGame[0] == False:
            self.sijainti[0] = self.sijainti[0] + nopeus
        elif self.sijainti[0] < 0 and self.newGame[0] == True:
            self.naytto.blit(mailaPunPic, maila.sijainti)
            pygame.display.flip()
            while True:
                self.uusiPeli()
                if self.newGame[1] == True:
                    break
            return

        # Oikea reuna
        if self.sijainti[0] > self.naytto.get_width():
            self.sijainti[0] = self.sijainti[0] - nopeus

        self.vaihdaSuunta()

    def vaihdaSuunta(self):
        if self.sijainti[0] < 0:
            self.suunta[0] = Vakio.OIKEA
        if self.sijainti[0] > self.naytto.get_width()-self.kuva.get_width():
            self.suunta[0] = Vakio.VASEN

        if self.sijainti[1] < 0:
            self.suunta[1] = Vakio.ALAS
        if self.sijainti[1] > self.naytto.get_height()-self.kuva.get_height():
            self.suunta[1] = Vakio.YLOS

    def kerroin(self):
        while True:
            apuKerroin = random.randint(-5,5)
            Vakio.KERROIN = 1+apuKerroin/10
            break

    def liikuta(self, nopeus=1):

        # liike
        # suunta[0] vasen/oikea, suunta[1] ylös/alas
        # Vasemmalle ylös
        if self.suunta[0] == Vakio.VASEN and self.suunta[1] == Vakio.YLOS:
            self.sijainti[0] = self.sijainti[0] - nopeus
            self.sijainti[1] = self.sijainti[1] - nopeus * Vakio.KERROIN
        # Vasemmalle alas
        if self.suunta[0] == Vakio.VASEN and self.suunta[1] == Vakio.ALAS:
            self.sijainti[0] = self.sijainti[0] - nopeus
            self.sijainti[1] = self.sijainti[1] + nopeus * Vakio.KERROIN
        # Oikealle ylös
        if self.suunta[0] == Vakio.OIKEA and self.suunta[1] == Vakio.YLOS:
            self.sijainti[0] = self.sijainti[0] + nopeus
            self.sijainti[1] = self.sijainti[1] - nopeus * Vakio.KERROIN
        # Oikealle alas
        if self.suunta[0] == Vakio.OIKEA and self.suunta[1] == Vakio.ALAS:
            self.sijainti[0] = self.sijainti[0] + nopeus
            self.sijainti[1] = self.sijainti[1] + nopeus * Vakio.KERROIN

        self.osuuIkkunanReunaan(1)
        self.kohtaa(maila,pallo)

    def kohtaa(self,Mailapeli1,Mailapeli2):
        if Mailapeli2.sijainti[0] >= Mailapeli1.sijainti[0] and Mailapeli2.sijainti[0] <= Mailapeli1.sijainti[0] + Mailapeli1.kuva.get_width() and \
                Mailapeli2.sijainti[1] >= Mailapeli1.sijainti[1] and Mailapeli2.sijainti[1] <= Mailapeli1.sijainti[1] + Mailapeli1.kuva.get_height():
            Mailapeli2.suunta[0] = Vakio.OIKEA
            self.kerroin()

    def piirra(self):
        self.naytto.blit(self.kuva, [self.sijainti[0], self.sijainti[1]])

# --------------------------------------
while True:
    suunta = [Vakio.VASEN,Vakio.YLOS]
    palloSuunta = [Vakio.VASEN,Vakio.YLOS]
    mailaSijainti = [naytto.get_width()/6,naytto.get_height()/2-mailaPic.get_height()/2]
    palloSijainti = [naytto.get_width()-palloPic.get_width()/2,naytto.get_height()/2-palloPic.get_height()/2]

    kello = pygame.time.Clock()

    # Osuu vasempaan reunaan ja peli päättyy sen vuoksi -> [0] == True
    maila = Mailapeli(naytto,mailaPic,suunta,mailaSijainti,[False,False])
    pallo = Mailapeli(naytto,palloPic,[Vakio.VASEN,Vakio.YLOS],palloSijainti,[True,False])

    pallo.kerroin()
    # Arvotaan suunta - ylös/alas
    if random.randint(1,2) == 1:
        pallo.suunta[1] = Vakio.YLOS
    else:
        pallo.suunta[1] = Vakio.ALAS

    while True:
        maila.painaNappainta(5)
        pallo.liikuta(5)

        kello.tick(Vakio.FPS)

        naytto.fill((0, 0, 0))
        maila.piirra()
        pallo.piirra()
        pygame.display.flip()

        # Halutaan uusi peli
        if pallo.newGame[1] == True:
            break