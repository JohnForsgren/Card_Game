
# -*- coding: utf-8 -*-



import pygame
import sys
from pygame.locals import *
import random

pygame.init()
clockvariableForFPS = pygame.time.Clock()
windowWidth = 900
windowHeight = 600
theWindow = pygame.display.set_mode((windowWidth, windowHeight))

kortPlatsInnutiSS_X = 0
kortPlatsInnutiSS_Y = 0
spriteSheet_Lagringsvariabel = pygame.image.load('Kortleken.png').convert_alpha()
EffectImage = pygame.image.load('EffectImage.png').convert_alpha()
DefendImage = pygame.image.load('DefendImage.png').convert_alpha()
DefendIcon = pygame.image.load('DefendIcon.png').convert_alpha()
RestorationImage = pygame.image.load('RestorationImage.png').convert_alpha()
highlightImage = pygame.image.load('GuildTrim.png').convert_alpha()
highlightImageInverted = pygame.image.load('GuildTrim_Inverted.png').convert_alpha()

colorForPlayer1 = (15, 110, 140)
colorForPlayer2 = (170, 60, 60)
SVART = (0, 0, 0)
VIT = (255, 255, 255)
GRAY = (30, 50, 60)
GREEN = (0, 200, 0)


maxAmountOfCardsFromHand = 3
maxAmountOfMovesOnField = 2


class GlobalaVariabler():
    def __init__(self, aktiveraEffekt, aCardIsBeingHeld):
        self.aktiveraEffekt = aktiveraEffekt
        self.aCardIsBeingHeld = aCardIsBeingHeld
        self.isTheAttackValid = True

class Overclass():
    def __init__(self, fourNumbersDecidingTheRectanglesProperties):
        self.hitBox = pygame.Rect(fourNumbersDecidingTheRectanglesProperties)
class Kort():
    isTheCardUpplyft = False
    canTheCardBePlacedDown = True
    canTheCardBePickedUp = True
    def __init__(self, fourNumbersDecidingTheRectanglesProperties, colorF, talF, deckHandPlanGraveyardF, ownedByPlayerF):
        self.hitBox = pygame.Rect(fourNumbersDecidingTheRectanglesProperties)
        self.color = colorF
        self.tal = talF
        self.deckHandPlanGraveyard = deckHandPlanGraveyardF
        self.ownedByPlayer = ownedByPlayerF
        self.shield = 0

    def ritaKortet(self, kortPlatsInnutiSS_X, kortPlatsInnutiSS_Y, placeWhereWeShallDraw):
        self.kortetsKoordinaterISS = spriteSheet_Lagringsvariabel.subsurface(pygame.Rect(kortPlatsInnutiSS_X, kortPlatsInnutiSS_Y, 71, 96))
        placeWhereWeShallDraw.set_colorkey((0, 0, 0))

        placeWhereWeShallDraw.blit(self.kortetsKoordinaterISS, (self.hitBox[0], self.hitBox[1]))
        #             "Vad vill vi rita?" ,  ("Vilken x-koordinat vill vi rita det på?", "Vilken y-koordinat?")

    def ritaBakgrund(self, placeWhereWeShallDraw):
        self.kortetsKoordinaterISS = spriteSheet_Lagringsvariabel.subsurface(pygame.Rect(144, 388, 71, 96))
        placeWhereWeShallDraw.blit(self.kortetsKoordinaterISS, (self.hitBox[0], self.hitBox[1]))

    def ritaGenomskinlig(self, placeWhereWeShallDraw, bild, forskjutningX, forskjutningY):
        nyYta = pygame.Surface((bild.get_width(), bild.get_height())).convert()  # Definierar en yta som vi kan rita på, som är SKILJD från vårt "fönster".
        # Notera att storleken på en bild kan ges genom "Bilden.get_width()" och "Bilden.get_height()"
        nyYta.blit(placeWhereWeShallDraw, (-self.hitBox[0], -self.hitBox[1]))  # Ritar ytan på theWindow - JAG VET INTE VARFÖR KOORDINATERNA MÅSTE VARA NEGATIVA - sannolikt pga att de definieras på ett annorlunda sätt.
        nyYta.blit(bild, (0, 0))  # Ritar BILDEN på ytan
        nyYta.set_colorkey(SVART)  # Bestämmer ytans genomskinlighetsfärg.
        placeWhereWeShallDraw.blit(nyYta,(self.hitBox[0] + forskjutningX, self.hitBox[1] + forskjutningY))  # Ritar ytan (med bilden inkluderad) på theWindow.


class Bricka():
    def __init__(self, fourNumbersDecidingTheRectanglesProperties, ownedByPlayerF, hand_planF, givetTalF, holdsCardColorF="Ingen", holdsCardNumberF=0):
        self.hitBox = pygame.Rect(fourNumbersDecidingTheRectanglesProperties)
        self.hand_plan = hand_planF
        self.ownedByPlayer = ownedByPlayerF
        self.holdsCardColor = holdsCardColorF
        self.holdsCardNumber = holdsCardNumberF
        self.givetTal = givetTalF

    def ritaBricka(self, placeWhereWeShallDraw):
        if self.hand_plan == "Plan":
            pygame.draw.rect(placeWhereWeShallDraw, SVART, self.hitBox)
        elif self.hand_plan == "Hand":
            pygame.draw.rect(placeWhereWeShallDraw, GRAY, self.hitBox)
            # Notering: Kom ihåg att det är enkelt att lägga in finare bilder på brickorna än färgade rutor!


class Knapp():
    def __init__(self, fourNumbersDecidingTheRectanglesProperties):
        self.hitBox = pygame.Rect(fourNumbersDecidingTheRectanglesProperties)

    def ritaKnapp(self, color, placeWhereWeShallDraw):
        pygame.draw.rect(placeWhereWeShallDraw, color, self.hitBox)

    def ritaKnappMedBild(self, typ, placeWhereWeShallDraw):
        if typ == "Defend":
            bild = DefendImage
        elif typ == "Effect":
            bild = EffectImage
        elif typ == "Restoration":
            bild = RestorationImage

        self.bildensKoordinaterISS = bild.subsurface(pygame.Rect(0, 0, self.hitBox[2], self.hitBox[3]))
        '''Denna variabel plockar ut bilden från spritesheeten (som alltid har koordinaterna (0,0) eftersom att det endast är en bild) och sätter den på knappens hitbox.'''
        placeWhereWeShallDraw.blit(self.bildensKoordinaterISS, (self.hitBox[0], self.hitBox[1]))
        #             "Vad vill vi rita?" ,  ("Vilken x-koordinat vill vi rita det på?", "Vilken y-koordinat?")


class Spelare():
    def __init__(self, antalKortLagda, amountOfMovesOnTheField):
        self.antalKortLagda = antalKortLagda # Räknar spelarnas drag
        self.amountOfMovesOnTheField = amountOfMovesOnTheField # Räknar spelens plandrag, dvs hur många förflyttningas rom kan göras på planen
        self.ninesOnTheField = 0 # Om denna variabel inte är 0 aktiveras nians speicaleffekt.

# DEFINIERING AV INSTANCES
# SKAPAR SPELARNA och KNAPPARNA
globalaVariabler = GlobalaVariabler("Nej", False)
spelare1 = Spelare(0, 0)
spelare2 = Spelare(0, 0)

antalDragKnapp = Knapp((320, 540, 220, 50))
visaPassivaKortKnapp = Knapp((50,450,50,50))

turKnapp = Knapp((385, 480, 100, 50))
defendButton = Knapp((785, 450, 50, 110))
effektKnapp = Knapp((845, 450, 50, 50))
restorationKnapp = Knapp((845, 510, 50, 50))

# ============FOR-LOOP för att definiera alla BRICKOR============
listaMedAllaBrickor = []
listaMedAllaPLANBrickor = []
listaMedAllaHANDBrickor = []
kolumn = 1
Y = 30
rad = 1
counter = 0
handEllerPlan = "Hand"
spelare1eller2 = 2
givetTal = 1
for k in range(24):
    if rad == 1:
        spelare1eller2 = 2  # Vi börjar med spelare 2 eftersom att spelare 2:s brickor skrivs på toppen av theWindow.
        handEllerPlan = "Hand"
    elif rad == 2:
        spelare1eller2 = 2
        handEllerPlan = "Plan"
    elif rad == 3:
        spelare1eller2 = 1
        handEllerPlan = "Plan"
    else:
        spelare1eller2 = 1
        handEllerPlan = "Hand"
    listaMedAllaBrickor.append(Bricka((100 * kolumn, Y, 71, 96), spelare1eller2, handEllerPlan, givetTal, "Ingen", 0))
    if handEllerPlan == "Hand":
        listaMedAllaHANDBrickor.append(Bricka((100 * kolumn, Y, 71, 96), spelare1eller2, handEllerPlan, 1))
    else:
        listaMedAllaPLANBrickor.append(Bricka((100 * kolumn, Y, 71, 96), spelare1eller2, handEllerPlan, 1))
    kolumn += 1
    givetTal += 1
    if kolumn == 8:
        kolumn = 1
        Y += 110
        rad += 1

# ============FOR-LOOP för att definiera alla KORT============
listaMedAllaKort = []
rad = 1
tal = 1
X = 0
Y = 0
theColor = "Klöver"
bytSpelare = False
spelare1eller2 = 1
for i in range(104):
    if bytSpelare == False:
        spelare1eller2 = 1
    else:
        spelare1eller2 = 2  # Notera att detta innebär att spelare 1:s kort ligger FÖRST i kortleken!

    if rad == 1:
        theColor = "Klöver"
    elif rad == 2:
        theColor = "Ruter"
    elif rad == 3:
        theColor = "Hjärter"
    elif rad == 4:
        theColor = "Spader"
    listaMedAllaKort.append(Kort((X, Y, 71, 96), theColor, tal, "Deck", spelare1eller2))
    tal += 1

    if tal == 14:  # Om vi kommit till radens slut resettar vi raden...
        if rad != 4:  # ...förutsatt att vi INTE kommot till den sista raden och sista kolumnen.
            rad += 1
            tal = 1
        else:  # Om vi kommit till radens slutOCH  den sista kolumnen
            rad = 1
            tal = 1
            bytSpelare = True
            X = 800
            Y = 0
    X += 0
    Y += 5

deckSpelare1 = listaMedAllaKort[0:52]
deckSpelare2 = listaMedAllaKort[52:104]
graveyardSpelare1 = []
graveyardSpelare2 = []  # Eventuellt kan "planSpelare1/2 också vara nödvändigt, men jag ser ingen användning för det atm.

#  ====FUNKTIONER=====================================================
def placeCardAtBrick(kortet, brickan, spelare1, spelare2):
    if brickan.hand_plan == "Plan": # Vi vill bara att korten registreras om de läggs på planen (Vi vill exempelvis INTE göra detta då vi drar kort från Deck).
        if kortet.tal == 9:
            if kortet.ownedByPlayer == 1:
                spelare1.ninesOnTheField += 1
                print("+++++++++ EN NIA LÄGGS TILL I spelare 1:s plan. Spelare 1 har nu " + str(spelare1.ninesOnTheField) + " nior på planen.")
                if spelare1.ninesOnTheField != 0:
                    print("Spelare 1 har nu minst 1 nia på planen. Alla kort under 9 sköldas.")
                    for kort2 in listaMedAllaKort:
                        if kort2.ownedByPlayer == 1 and kort2.tal < 9:
                            kort2.shield += 1
            elif kortet.ownedByPlayer == 2:
                spelare2.ninesOnTheField += 1
                print("+++++++++ EN NIA LÄGGS TILL I spelare 2:s plan. Spelare 2 har nu " + str(spelare2.ninesOnTheField) + " nior på planen.")
                if spelare2.ninesOnTheField != 0:
                    print("Spelare 2 har nu minst 1 nia på planen. Alla kort under 9 sköldas.")
                    for kort2 in listaMedAllaKort:
                        if kort2.ownedByPlayer == 2 and kort2.tal < 9:
                            kort2.shield += 1

    if kortet.ownedByPlayer == 1 and spelare1.ninesOnTheField != 0 and kortet.tal < 9 and kortet.ownedByPlayer == 1:
        kortet.shield = True
    elif kortet.ownedByPlayer == 2 and spelare2.ninesOnTheField != 0 and kortet.tal < 9 and kortet.ownedByPlayer == 2:
        kortet.shield = True

    kortet.isTheCardUpplyft = False#Denna rad är endast nödvändig då vi lägger kortet direkt från handen, dvs den är onödig för t.ex funktionen "drawCardFromDeck" samt funktioner som placerar kort på planen genom effeter.
    globalaVariabler.aCardIsBeingHeld = False#Även denna rad är endast nödvändig om vi lagt kortet på planen direkt från handen.
    kortet.hitBox.center = brickan.hitBox.center#Lägger kortet i brickan (endast genom dess hitbox samt visuellt)
    kortet.deckHandPlanGraveyard = brickan.hand_plan #Sätter kortets egenskap till "Hand" eller "Plan" beroende på vilken sådan egenskap brickan har.
    brickan.holdsCardColor = kortet.color#Låter brickan veta om vilket kort som lagts i den.
    brickan.holdsCardNumber = kortet.tal


def sendCardAtBrickToGraveyard(kort, bricka, spelare1, spelare2):
    '''==== VIKTIGAST: DENNA FUNKTION MÅSTE ALLTID KALLAS SÅ FORT ETT KORT SKICKAS TILL GRAVEYARD - KORTET FÅR INTE SKICKAS DIT PÅ *NÅGOT* ANNAT SÄTT!!! ===='''

    if kort.tal == 9: # Kollar om kortet är en nia; detta för att kunna hantera nians passiva effekt som sköldar alla kort mellan 1-8. Så länge kortets shield-variabel inte är 0 har kortet en sköld.
        if kort.deckHandPlanGraveyard == "Plan" and kort.ownedByPlayer == 1:
            spelare1.ninesOnTheField -= 1
            print("---------- En nia tas bort från spelare 1:s plan. Spelare 1 har nu " + str(spelare1.ninesOnTheField) + " nior på planen.")
            if spelare1.ninesOnTheField == 0:
                for kort2 in listaMedAllaKort:
                    if kort2.ownedByPlayer == 1 and kort2.tal < 9:
                        kort2.shield -= 1
        elif kort.deckHandPlanGraveyard == "Plan" and kort.ownedByPlayer == 2:
            spelare2.ninesOnTheField -= 1
            print("---------- En nia tas bort från spelare 2:s plan. Spelare 2 har nu " + str(spelare2.ninesOnTheField) + " nior på planen.")
            if spelare2.ninesOnTheField == 0:
                for kort2 in listaMedAllaKort:
                    if kort2.ownedByPlayer == 2 and kort2.tal < 9:
                        kort2.shield -= 1

    if kort.ownedByPlayer == 1:
        graveyardSpelare1.append(kort)
    elif kort.ownedByPlayer == 2:
        graveyardSpelare2.append(kort)
    kort.deckHandPlanGraveyard = "Graveyard"
    bricka.holdsCardNumber = 0
    bricka.holdsCardColor = "Ingen"
    '''TILLÄGG: FÖR ATT KUNNA ÅTERUPPLIVA KORT krävs det att det läggs in i denna funktion att korten placeras i graveyard-listan.'''


def theCardThatWins(cardColor, cardNumber, brickColor, brickNumber):
    if cardNumber == 5 and brickNumber > 10: # Femmor vinner över klädda kort, men bara då FEMMORNA attackerar
        return "Handen"
    elif cardNumber > brickNumber:
        return "Handen"
    elif cardNumber < brickNumber:
        return "Motståndarkortet"
    elif cardNumber == brickNumber:
        return "Oavgjort"


def handeBattleBetweenTwoCards( theCardThatWins, listaMedAllaKort, bricka, sparadBricka, upplyftKort, spelaresTur, spelare1, spelare2):
    if theCardThatWins == "Handen":
        print("Kortet i handen var STARKARE än kortet i brickan.")
        for kort in listaMedAllaKort:  # Loopen letar fram kortet som ligger i brickan och sätter det kortets egenskap till Graveyard.
            if kort.color == bricka.holdsCardColor and kort.tal == bricka.holdsCardNumber and kort.ownedByPlayer != spelaresTur:
                print("Kortet som låg på motståndarplanen var: " + str(kort.color) + str(kort.tal))
                sendCardAtBrickToGraveyard(kort, bricka, spelare1, spelare2)

                sparadBricka.holdsCardColor = upplyftKort.color
                sparadBricka.holdsCardNumber = upplyftKort.tal
                break
    elif theCardThatWins == "Motståndarkortet":
        print("Kortet i handen var SVAGARE än kortet i brickan.")
        upplyftKort.hitBox.center = (10, 10)
        sendCardAtBrickToGraveyard(upplyftKort, sparadBricka, spelare1, spelare2)
    elif theCardThatWins == "Oavgjort":
        print("Kortet i handen var LIKA STARKT än kortet i brickan.")
        sendCardAtBrickToGraveyard(upplyftKort, sparadBricka, spelare1, spelare2)
        for kort in listaMedAllaKort:  # Loopen letar fram kortet som ligger i brickan och sätter det kortets egenskap till Graveyard.
            if kort.color == bricka.holdsCardColor and kort.tal == bricka.holdsCardNumber and kort.ownedByPlayer != spelaresTur:
                print("Kortet som låg på motståndarplanen var: " + str(kort.color) + str(kort.tal))
                sendCardAtBrickToGraveyard(kort, bricka, spelare1, spelare2)
                break

    if spelaresTur == 1:
        spelare1.amountOfMovesOnTheField += 1
    elif spelaresTur == 2:
        spelare2.amountOfMovesOnTheField += 1
    print("Spelare 1 har nu lagt såhär många drag under sin tur: " + str(
        spelare1.amountOfMovesOnTheField) + ". Och spelare 2: " + str(spelare2.amountOfMovesOnTheField))


def skickaTillbakaUpplyftKort(upplyftKort, sparadBricka):#Skickar tillbaka det kort som var markerat till sin bricka.
    upplyftKort.isTheCardUpplyft = False
    sparadBricka.holdsCardColor = upplyftKort.color
    sparadBricka.holdsCardNumber = upplyftKort.tal
    globalaVariabler.aCardIsBeingHeld = False

def resurection(spelare, listaMedAllaBrickor, spelare1, spelare2, graveyardSpelare1, graveyardSpelare2):#Återupplivar kortet länst upp i spelarens graveyard.
    if spelare == 1:
        for bricka2 in listaMedAllaBrickor:
            if bricka2.holdsCardNumber == 0 and bricka2.hand_plan == "Plan" and bricka2.ownedByPlayer == 1:
                placeCardAtBrick(graveyardSpelare1[len(graveyardSpelare1) - 1], bricka2, spelare1, spelare2)
                graveyardSpelare1.pop(len(graveyardSpelare1) - 1)
                break
    elif spelare == 2:
        for bricka2 in listaMedAllaBrickor:
            if bricka2.holdsCardNumber == 0 and bricka2.hand_plan == "Plan" and bricka2.ownedByPlayer == 2:
                placeCardAtBrick(graveyardSpelare2[len(graveyardSpelare2) - 1], bricka2, spelare1, spelare2)
                graveyardSpelare2.pop(len(graveyardSpelare2) - 1)
                break



def hanteraManuellaEffekter(bricka, upplyftKort, sparadBricka, globalaVariabler, spelaresTur):
    '''Se idéer för kortspelet för en översikt över kortens effekter.'''
    if bricka.hand_plan == "Plan":
        print("En planbricka klickades. Endast kort vars manuella effekter kan appliceras på plan kort tittas på.")
        if upplyftKort.tal == 3 and spelaresTur != bricka.ownedByPlayer:
            print("3 Aktiverades på en MOTSTÅNDARBRICKA. Det klickade motståndarkortet plockas bort.")
            for kort in listaMedAllaKort:
                if kort.color == bricka.holdsCardColor and kort.tal == bricka.holdsCardNumber and kort.ownedByPlayer != spelaresTur:
                    sendCardAtBrickToGraveyard(kort, bricka, spelare1, spelare2)
                    skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)
                    globalaVariabler.aktiveraEffekt = "Nej"
        elif upplyftKort.tal == 4 and spelaresTur == bricka.ownedByPlayer and bricka.holdsCardNumber != 0:
            print("4 Aktiverades på en en ALLIERAD BRICKA. Det klickade kortet offtas. I utbyte får ett extra drag göras.")
            for kort in listaMedAllaKort:
                if kort.color == bricka.holdsCardColor and kort.tal == bricka.holdsCardNumber and kort.ownedByPlayer == spelaresTur:
                    print("Kortet " + str(kort.color) + str(kort.tal) + "Skickas till graveyard och spelaren får 2 extra drag.")
                    sendCardAtBrickToGraveyard(kort, bricka, spelare1, spelare2)
                    skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)
                    globalaVariabler.aktiveraEffekt = "Nej"
                    if spelaresTur == 1:
                        spelare1.amountOfMovesOnTheField -= 2
                    else:
                        spelare2.amountOfMovesOnTheField -= 2
