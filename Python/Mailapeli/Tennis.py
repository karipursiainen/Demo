# -*- coding: utf-8 -*-
import pygame, sys, random

"""
Tennis
Tekijä: Kari Pursiainen
Pvm: 1/2018

Ohjeet: Estä pallon pääsy kentän vasempaan tai oikeaan laitaan 'lyömällä' pallo takaisin mailalla.
        Jos pallo osuu laitaan - peli päättyy
        Mailaa voi liikuttaa ylös/alas/vasemmalle/oikealle nuolinäppäimillä
        Pallon osuminen mailaan muuttaa pallon liikerataa
"""

naytto = pygame.display.set_mode((840, 400))
pygame.display.set_caption("Tennis")
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
    # naytto: Näytön koko
    # kuva: olion kuva
    # suunta: olion suunta
    # sijainti: olion sijainti
    # newGame: [0] voiko peli poäättyä jos olio osuu ikkunan reunaan, [1] jos True, peli päättyy ja tiedustellaan uutta peliä
    # reunatKimpoaa: ne reunat oliolle, joihin osuessa peli EI pääty
    def __init__(self,naytto,kuva,suunta=[Vakio.VASEN,Vakio.YLOS], sijainti=[0,0],newGame=[False,False], reunatKimpoaa = [Vakio.YLOS, Vakio.ALAS, Vakio.VASEN, Vakio.OIKEA]):
        self.suunta = suunta
        self.sijainti = sijainti
        self.kuva = kuva
        self.newGame = newGame
        self.naytto = naytto
        self.reunatKimpoaa = reunatKimpoaa

    # Kontrolli
    def painaNappainta(self, maila, nopeus = 1):
        # kontrolli, eli käyttäjän toimintojen kuuntelu ja niihin reagointi
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

        # toimintojen käsittely
        tapahtuma = pygame.key.get_pressed()

        # Vasen maila
        if maila == Vakio.VASEN:
            # ylös
            if tapahtuma[pygame.K_UP]:
                self.sijainti[1] = self.sijainti[1] - nopeus

            # alas
            if tapahtuma[pygame.K_DOWN]:
                self.sijainti[1] = self.sijainti[1] + nopeus

            # vasemmalle
            if tapahtuma[pygame.K_LEFT]:
                self.sijainti[0] = self.sijainti[0] - nopeus

            # oikealle
            if tapahtuma[pygame.K_RIGHT]:
                self.sijainti[0] = self.sijainti[0] + nopeus

        # Oikea maila
        elif maila == Vakio.OIKEA:
            # ylös
            if tapahtuma[pygame.K_KP8]:
                self.sijainti[1] = self.sijainti[1] - nopeus

            # alas
            if tapahtuma[pygame.K_KP2]:
                self.sijainti[1] = self.sijainti[1] + nopeus

            # vasemmalle
            if tapahtuma[pygame.K_KP4]:
                self.sijainti[0] = self.sijainti[0] - nopeus

            # oikealle
            if tapahtuma[pygame.K_KP6]:
                self.sijainti[0] = self.sijainti[0] + nopeus

        # Osuuko olio ikkunan reunaan
        self.osuuIkkunanReunaan(nopeus)

    def uusiPeli(self):
        naytettava_teksti = fontti.render("Uusi peli k/e?", True, (255, 255, 255))
        self.naytto.blit(naytettava_teksti, (self.naytto.get_width() * 0.4, self.naytto.get_height() * 0.4))
        pygame.display.flip()

        self.newGame[1] = False
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

            # toimintojen käsittely
            if tapahtuma.type == pygame.KEYDOWN:

                # Uusi peli?
                # Ei - lopetus
                if tapahtuma.key == pygame.K_e:
                    exit()

                # Kyllä
                if tapahtuma.key == pygame.K_k:
                    # Halutaan uusi peli
                    self.newGame[1] = True
                    return

    # Logiikka
    def osuuIkkunanReunaan(self, nopeus=1):
        # osuu ikkunan reunaan
        # Yläreuna
        if self.sijainti[1] < 0:
            # Kimpoaa
            if Vakio.YLOS in self.reunatKimpoaa:
                self.sijainti[1] = self.sijainti[1] + nopeus
            # Ei kimpoa
            else:
                self.newGame[1] = True
        # Alareuna
        elif self.sijainti[1] > self.naytto.get_height() - self.kuva.get_height():
            # Kimpoaa
            if Vakio.ALAS in self.reunatKimpoaa:
                self.sijainti[1] = self.sijainti[1] - nopeus
            # Ei kimpoa
            else:
                self.newGame[1] = True
        # Oikea reuna - Jos kohde osuu reunaan ja peli päättyy sen vuoksi -> newGame[0] == True
        elif self.sijainti[0] > self.naytto.get_width() - self.kuva.get_width():
            if Vakio.OIKEA in self.reunatKimpoaa:
                self.sijainti[0] = self.sijainti[0] - nopeus
            else:
                self.newGame[1] = True
        # Vasen reuna - Jos kohde osuu reunaan ja peli päättyy sen vuoksi -> newGame[0] == True
        elif self.sijainti[0] < 0:
            if Vakio.VASEN in self.reunatKimpoaa:
                self.sijainti[0] = self.sijainti[0] + nopeus
            else:
                self.newGame[1] = True

        # Olio osuu reunaan ja peli päättyy sen vuoksi
        if self.newGame[0] == True and self.newGame[1] == True:
            self.naytto.blit(mailaPunPic, mailaVasen.sijainti)
            self.naytto.blit(mailaPunPic, mailaOikea.sijainti)
            pygame.display.flip()
            while True:
                self.uusiPeli()
                if self.newGame[1] == True:
                    break
            return

        self.vaihdaSuunta()

    # Osuu ikkunan reunaan tai mailaan - vaihdetaan suuntaa
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
        apuKerroin = random.randint(-5,5)
        Vakio.KERROIN = 1+apuKerroin/10

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
        self.kohtaaVasen(mailaVasen,pallo) # Pallo osuu vasemmanpuoleiseen mailaan
        self.kohtaaOikea(mailaOikea, pallo) # Pallo osuu oikeanpuoleiseen mailaan

    def kohtaaVasen(self,Mailapeli1,Mailapeli2):

        if Mailapeli2.sijainti[0] >= Mailapeli1.sijainti[0] and Mailapeli2.sijainti[0] <= Mailapeli1.sijainti[0] + Mailapeli1.kuva.get_width() and \
                Mailapeli2.sijainti[1] >= Mailapeli1.sijainti[1] and Mailapeli2.sijainti[1] <= Mailapeli1.sijainti[1] + Mailapeli1.kuva.get_height():
            Mailapeli2.suunta[0] = Vakio.OIKEA

            self.kerroin()

    def kohtaaOikea(self,Mailapeli1,Mailapeli2):

        if Mailapeli2.sijainti[0] >= Mailapeli1.sijainti[0]-Mailapeli2.kuva.get_width() and Mailapeli2.sijainti[0] <= Mailapeli1.sijainti[0] and \
                Mailapeli2.sijainti[1] >= Mailapeli1.sijainti[1] and Mailapeli2.sijainti[1] <= Mailapeli1.sijainti[1] + Mailapeli1.kuva.get_height():
            Mailapeli2.suunta[0] = Vakio.VASEN

            self.kerroin()

    def piirra(self):
        self.naytto.blit(self.kuva, [self.sijainti[0], self.sijainti[1]])

# --------------------------------------
while True:
    palloSuunta = [Vakio.VASEN,Vakio.YLOS]
    mailaVasenSijainti = [naytto.get_width()/8,naytto.get_height()/2-mailaPic.get_height()/2]
    mailaOikeaSijainti = [naytto.get_width() / 1.125, naytto.get_height()/2 - mailaPic.get_height() / 2]
    palloSijainti = [naytto.get_width()/2-palloPic.get_width()/2,naytto.get_height()/2-palloPic.get_height()/2]

    kello = pygame.time.Clock()

    # Osuu vasempaan reunaan ja peli päättyy sen vuoksi -> [0] == True
    mailaVasen = Mailapeli(naytto,mailaPic,[Vakio.OIKEA,Vakio.YLOS],mailaVasenSijainti,[False,False],[Vakio.YLOS, Vakio.ALAS, Vakio.VASEN, Vakio.OIKEA])
    mailaOikea = Mailapeli(naytto, mailaPic, [Vakio.VASEN,Vakio.YLOS], mailaOikeaSijainti, [False, False],[Vakio.YLOS, Vakio.ALAS, Vakio.VASEN, Vakio.OIKEA])
    pallo = Mailapeli(naytto,palloPic,[Vakio.VASEN,Vakio.YLOS],palloSijainti,[True,False],[Vakio.YLOS, Vakio.ALAS])

    pallo.kerroin()
    # Arvotaan suunta - ylös/alas
    if random.randint(1,2) == 1:
        pallo.suunta[1] = Vakio.YLOS
    else:
        pallo.suunta[1] = Vakio.ALAS

    while True:
        mailaVasen.painaNappainta(Vakio.VASEN,5)
        mailaOikea.painaNappainta(Vakio.OIKEA,5)
        pallo.liikuta(3)

        kello.tick(Vakio.FPS)

        naytto.fill((0, 0, 0))
        mailaVasen.piirra()
        mailaOikea.piirra()
        pallo.piirra()
        pygame.display.flip()

        # Halutaan uusi peli
        if pallo.newGame[1] == True:
            break
