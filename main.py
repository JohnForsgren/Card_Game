
# -*- coding: utf-8 -*-

from Funktioner import *
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



'''
VARIABLER SOM ORSAKAR PROBLEM OCH MÅSTE LÄGGAS IN SOM ARGUMENT:
- Fönstret
- (R) bricka (Ändrat till self)

ÖVRIGA VARIABLER
- spriteSheet_Lagringsvariabel
- Alla bilder (De ritas i knapp-funktionen)
- Färger

'''




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
for k in range(28):
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


def drawCardFromDeck(spelareSomSkaPlockaUppKortet, antalKort):
    '''drawCardFromDeck(a,b) plockar upp b antal kort för spelare a.'''
    if spelareSomSkaPlockaUppKortet == 1:
        deck = deckSpelare1
        delAvListaMedAllaKort = listaMedAllaKort[0:52]
        '''listaMedAllaKort[0:52] innehåller samtliga kort för spelare 1. Denna lista gås igenom för att plocka fram de kort som slumpas fram (och dras) från spelare 1:s Deck. '''
    else:
        deck = deckSpelare2
        delAvListaMedAllaKort = listaMedAllaKort[52:104]

    firstCounter = 0
    for bricka in listaMedAllaBrickor:  # OPTIMERING: Då programmet är klart kan detta ändras så att alla brickor inte gås igenom, utan endast HANDBRICKORNA.
        if bricka.holdsCardNumber == 0 and bricka.hand_plan == "Hand" and bricka.ownedByPlayer == spelareSomSkaPlockaUppKortet:  # Om brickan är tom, är en handbricka, och tillhör spelaren som plockar upp korten.
            if firstCounter == antalKort:  # Denna rad avgör hur många kort som plockas upp, eftersom att programmet bryter då det maximala antalet kortet plockats upp.
                break
            slump = random.randint(0, len(deck) - 1)#Slumpar fram ett kort i decken.
            '''Anledningen varför -1 krävs vid len() är för att len alltid börjar räkna från 1. Exempel: Om listan XXX är 5 element lång syftar XXX[4] till det sista elementet i listan, medan XXX[len(XXX)] syftar till XXX[5]'''
            # print("========Kortet som slumpats fram var: " + str(deck[slump].color) + str(deck[slump].tal) + " ===========")
            for kort in delAvListaMedAllaKort:#Går igenom listan med alla relevanta kort....
                if kort.color == deck[slump].color and kort.tal == deck[slump].tal:  # ... letar fram (motsvarande kort som slumpats fram i kortleken) i listaMedAllaKort.
                    placeCardAtBrick(kort, bricka, spelare1, spelare2)               # ... lägger in kortet i brickan
                    firstCounter += 1  # Då if-satsen ovan exekveras innebär det att ett kort successfully har hittas och dragits. firstCounter ökas då för att förhindra att för många kort dras.
                    break
            print("Följande kort tas bort: " + str(kort.color) + str(kort.tal))
            deck.remove(kort) # Kortet som togs fram i for-loopen ovan tas bort ur kortlistan.
            '''%%%%Notering: Detta verkar fungera, men jag fattar INTE varför. Då vi skriver "deck = deckSpelare1" ovan definierar vi väl en ny variabel "deck" som är 
             SEPARAT från "deckspelare1", så när vi skriver deck.remove(kort) tar det väl endast bort kortet från "deck" och INTE "deckspelare1"?   '''





def placeCardAtBrick(kortet, brickan, spelare1, spelare2):
    '''==== VIKTIGAST: DENNA FUNKTION MÅSTE ALLTID KALLAS SÅ FORT ETT KORT LÄGGS NER - KORTET FÅR INTE LÄGGAS NER PÅ *NÅGOT* ANNAT SÄTT!!! ===='''
    '''==============================================================================
    Tillägg: Om kortet som läggs ner låg i graveyard (dvs deckHandPlan) betyder det att kortet har återupplivats, och MÅSTE TAS BORT från graveyardlistan.
    =============================================================================='''
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

    if kort.tal == 9:
        if kort.deckHandPlanGraveyard == "Plan" and kort.ownedByPlayer == 1:
            spelare1.ninesOnTheField -= 1
            print("---------- En nia tas bort från spelare 1:s plan. Spelare 1 har nu " + str(spelare1.ninesOnTheField) + " nior på planen.")
            if spelare1.ninesOnTheField == 0:
                for kort2 in listaMedAllaKort:
                    if kort2.ownedByPlayer == 1 and kort2.tal < 9:
                        kort2.shield -= 1
                        '''PROBLEM: Vi kan alltid lägga till sköldar utan att ta hänsyn till andra sköldeffekter, men vi kan INTE nödvändigtvis ta bort sköldar bara för att niorna försvinner. 
                        Potentiell lösning: Om endast ett kort ska sköldas per tur kan detta kanske lösas genom att ha ett sparatSköldKort för varje spelare. Ett problem med detta är dock om denna sparning inte görs i funktionsdokumentet.'''
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
    if cardNumber == 5 and brickNumber > 10: # Femmor vinner alltid över klädda kort, men bara då FEMMORNA attackerar
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
    '''TILLÄGG: Skapa en funtkion som hanterar livspoäng (eller dylikt) i de 3 satsera ovan!
    - För att kunna göra det krävs det att funktionen "vilketKortVinner()" returnerar med än bara en sträng; Det ideala är att den
    returnerar ett sträng med minst 2 element, där första elementet är vilket kort som vinner, och andra elementet är t.ex hur mycket livspoäng
    som spelaren i fråga förlorar.'''
    if spelaresTur == 1:
        '''NOTERING: Potentiellt sett blir spelet roligare om handlingar inte räknas som förflyttningar då man vinner mot motståndarkortet (Snowball)'''
        spelare1.amountOfMovesOnTheField += 1
    elif spelaresTur == 2:
        spelare2.amountOfMovesOnTheField += 1
    print("Spelare 1 har nu lagt såhär många drag under sin tur: " + str(
        spelare1.amountOfMovesOnTheField) + ". Och spelare 2: " + str(spelare2.amountOfMovesOnTheField))


def skickaTillbakaUpplyftKort(upplyftKort, sparadBricka):
    upplyftKort.isTheCardUpplyft = False
    sparadBricka.holdsCardColor = upplyftKort.color
    sparadBricka.holdsCardNumber = upplyftKort.tal
    globalaVariabler.aCardIsBeingHeld = False

def resurection(spelare, listaMedAllaBrickor, spelare1, spelare2, graveyardSpelare1, graveyardSpelare2):
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






def hanteraAktivaEffekter(theCardsColor, kortetsTal, spelaresTur, upplyftKort, sparadBricka, spelare1, spelare2):
    skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)#Viktigt att detta ligger FÖRST, annars kommer programmet inte upptäcka att ett kort faktiskt ligger på rutan där
    if kortetsTal == 1:
        print("ESS AKTIVERAT - FINAL DESTINY")
        for bricka2 in listaMedAllaBrickor:#############################Kan vara bra att lägga in denna lista i argumentet för att undvika potentiella problem!
            if bricka2.holdsCardNumber != 0:
                for kort2 in listaMedAllaKort:
                    if kort2.color == bricka2.holdsCardColor and kort2.tal == bricka2.holdsCardNumber and kort2.ownedByPlayer == bricka2.ownedByPlayer:
                        sendCardAtBrickToGraveyard(kort2, bricka2, spelare1, spelare2)
                        # HITTA KORTET "kort2" i brickan, och SKICKA SEDAN IN DESSA 2 VARIABLER I graveyardfunktionen.

        if spelaresTur == 1:#Låter MOTSTÅNDARSPELAREN plocka upp några kort, eftersom att hen annars startar sin tur med tom hand.
            drawCardFromDeck(2, 1)
        else:
            drawCardFromDeck(1, 1)


    elif kortetsTal == 2:
        print("En tvåa aktiverades. Två kort dras ut kortleken.")
        drawCardFromDeck(spelaresTur, 2)
    elif kortetsTal == 3:
        print("Kortet 3 klickades. Nu måste vi markera ett MOTSTÅNDARKORT.")
        globalaVariabler.aktiveraEffekt = "Ja"#Då aktiveraEffekt sätts till "Ja" innebär det att vi har försökt aktivera ett kort med en manuell effekt. Detta triggar funktionen för manuella effekter.
    elif kortetsTal == 4:
        print("Kortet 4 klickades. Nu måste vi markera ett ALLIERAT KORT.")
        globalaVariabler.aktiveraEffekt = "Ja"
    elif kortetsTal > 9:
        print("ETT KORT aktiverades. Första kortet i graveyard återuppstår.")
        '''Problem: 
        - (R) Skicka tillbaka markerat kort.
        - (R) BUG: Den markerade brickan är tömd på kort just då effekten aktiveras.
        - (R) BUG: Hela planen fylls med kortet som lyfts upp! 
        - Ta bort kortet från graveyard.
        - Går ej om len(Graveyard) == 0. 
        '''
        if spelaresTur == 1:
            if len(graveyardSpelare1) == 0:
                print("OGILTIGT DRAAG: Spelare 1:s graveyard var tom. Inga drag tas från spelaren dock.")
                spelare1.amountOfMovesOnTheField -= 1
            else:
                resurection(1, listaMedAllaBrickor, spelare1, spelare2, graveyardSpelare1, graveyardSpelare2)
        if spelaresTur == 2:
            if len(graveyardSpelare2) == 0:
                print("OGILTIGT DRAAG: Spelare 2:s graveyard var tom. Inga drag tas från spelaren dock.")
                spelare2.amountOfMovesOnTheField -= 1
            else:
                resurection(2, listaMedAllaBrickor, spelare1, spelare2, graveyardSpelare1, graveyardSpelare2)


    else:
        print("Kortet innehöll ingen specialeffekt. Inget av spelarens drag dras av dock. ")
        if spelaresTur == 1:
            spelare1.amountOfMovesOnTheField -= 1
        else:
            spelare2.amountOfMovesOnTheField -= 1

    if spelaresTur == 1:
        print("Ett drag för spelare 1 registreras (Förutsatt att kortet innehöll en specialeffekt).")
        spelare1.amountOfMovesOnTheField += 1
    else:
        print("Ett drag för spelare 2 registreras (Förutsatt att kortet innehöll en specialeffekt).")
        spelare2.amountOfMovesOnTheField += 1




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



# ============================ HÄR BÖRJAR MAIN ==================================


import pygame
import sys
from pygame.locals import *
import random


# ============ FUNKTIONER (DVS INTE KLASSER) som sköter en del av det repetitiva arbetet ============

def visaMeddelande(texten, meddelandetsX, meddelandetsY, textStorlek, color):
    # Denna funktion skriver ut en text på skärmen. Den första parametern är det meddelande som ska visas, och se andra 2 parametrarna är koordinaterna för meddelandet.
    textYta = pygame.font.Font("freesansbold.ttf", textStorlek).render(texten, True,
                                                                       color)  # Detta motsvarar ett print-påstående i pygame (dvs på skärmen). lol.
    textRektangel = textYta.get_rect()  # [???]Denna funktion ANTAR VI används för att returnera något som ska visa en rektangel.
    textRektangel.center = (meddelandetsX, meddelandetsY)
    # För att placera texten i mitten av skärmen skriver vi "FÖNSTRETS_BREDD/2, FÖNSTRETS_HÖJD/2" i dessa parametrar.
    theWindow.blit(textYta, textRektangel)  # Detta ritar textRektangeln med texten på vårt fönster. .



def kollaOmKortetKanPlockasUpp():
    '''Kollar i nuläget bara om spelaren i fråga inte redan lagt ut 2 kort från handen.'''
    if kort.deckHandPlanGraveyard == "Hand":
        if spelaresTur == 1:
            if spelare1.antalKortLagda < maxAmountOfCardsFromHand:
                print(
                    "Spelare 1 har inte lagt ut 2 kort under sin tur än, så kortet kan lyftas upp. [förutsätter att inga kort har specialkrav för att läggas]")
                kort.canTheCardBePickedUp = True
            else:
                kort.canTheCardBePickedUp = False

        elif spelaresTur == 2:
            if spelare2.antalKortLagda < maxAmountOfCardsFromHand:
                print(
                    "Spelare 2 har inte lagt ut 2 kort under sin tur än, så kortet kan lyftas upp. [förutsätter att inga kort har specialkrav för att läggas]")
                kort.canTheCardBePickedUp = True
            else:
                kort.canTheCardBePickedUp = False

    elif kort.deckHandPlanGraveyard == "Plan":
        if spelaresTur == 1:
            if spelare1.amountOfMovesOnTheField < maxAmountOfMovesOnField:
                print("Spelare 1 har inte än gjort 3 drag (på fältkorten) under sin tur, så kortet kan lyftas upp. ")
                kort.canTheCardBePickedUp = True
            else:
                kort.canTheCardBePickedUp = False
        elif spelaresTur == 2:
            if spelare2.amountOfMovesOnTheField < maxAmountOfMovesOnField:
                print("Spelare 2 har inte än gjort 3 drag (på fältkorten) under sin tur, så kortet kan lyftas upp. ")
                kort.canTheCardBePickedUp = True
            else:
                kort.canTheCardBePickedUp = False


def checkIfTheCardCanBePutDown():
    '''Kollar i nuläget endast om spelaren förbrukat sina drag på fältet eller inte.'''
    kort.canTheCardBePlacedDown = True

def determineIfTheAttackIsValid(upplyftKort, bricka):
    '''Kolla vilken spelare som attackerar, dvs vilken spelare som har kortet i handen. Spelare som attakerar = upplyftKort.ownedByPlayer'''
    if upplyftKort.ownedByPlayer == 1:
        print("Kortet som attakerar tillhör spelare 1")
        for kort2 in listaMedAllaKort:
            if kort2.color == bricka.holdsCardColor and kort2.tal == bricka.holdsCardNumber and kort2.ownedByPlayer == 2:
                if kort2.shield != 0:
                    globalaVariabler.isTheAttackValid = False
                    print("OGILTIG ATTACK. Anledning: Minst en NIA låg ute på motståndarens fält och attacken gjordes mot en 1-8:a ")
                else:
                    globalaVariabler.isTheAttackValid = True

    elif upplyftKort.ownedByPlayer == 2:
        print("Kortet som attakerar tillhör spelare 2")
        for kort2 in listaMedAllaKort:
            if kort2.color == bricka.holdsCardColor and kort2.tal == bricka.holdsCardNumber and kort2.ownedByPlayer == 1:
                if kort2.shield != 0:
                    globalaVariabler.isTheAttackValid = False
                    print("OGILTIG ATTACK. Anledning: Minst en NIA låg ute på motståndarens fält och attacken gjordes mot en 1-8:a ")
                else:
                    globalaVariabler.isTheAttackValid = True



# ==============DRAR KORT UNDER FÖRSTA TUREN==============
drawCardFromDeck(1, 5)
drawCardFromDeck(2, 5)

# ==================PROGRAMMETS START==================
globalaVariabler.aCardIsBeingHeld = False
spelaresTur = 1
breakFromTheLoop = False
isItTheFirstTurn = True
while True:
    if spelaresTur == 1:
        theWindow.fill(colorForPlayer1)
    elif spelaresTur == 2:
        theWindow.fill(colorForPlayer2)

    for theEvent in pygame.event.get():
        if theEvent.type == QUIT:
            pygame.quit()
            sys.exit()
        enBrickaHarKlickats = False# Om en bricka inte klickats och vi håller ett kort i handen, behövs denna variabel för att skicka tillbaka kortet.
        for bricka in listaMedAllaBrickor:#Denna sats används för att kontrollera att en bricka har klickats på. Om detta INTE skett vill vi att programmet skickar tillbaka kort som hålls i handen (eftersom att kort inte får läggas utanför brickor).
            if theEvent.type == pygame.MOUSEBUTTONDOWN and bricka.hitBox.collidepoint(theEvent.pos):
                print("En bricka klickades på. Brickan höll kortet " + str(bricka.holdsCardColor) + str(bricka.holdsCardNumber) + " Koordinater: " + str(bricka.givetTal))
                enBrickaHarKlickats = True
                theBrickThatHasBeenClicked = bricka


        # ==========EFFEKTKNAPPEN KLICKADES OCH ETT KORT HÖLLS I HANDEN ==========
        if theEvent.type == pygame.MOUSEBUTTONDOWN and effektKnapp.hitBox.collidepoint(theEvent.pos):
            print("Effektknappen klickades ")
            if globalaVariabler.aCardIsBeingHeld == True:
                print("Ett kort var markerat")
                if upplyftKort.deckHandPlanGraveyard == "Plan":
                    print("Kortet låg på planen")
                    if spelaresTur == 1:
                        hanteraAktivaEffekter(upplyftKort.color, upplyftKort.tal, 1, upplyftKort, sparadBricka, spelare1, spelare2)
                    else:
                        hanteraAktivaEffekter(upplyftKort.color, upplyftKort.tal, 2, upplyftKort, sparadBricka, spelare1, spelare2)


        for bricka in listaMedAllaBrickor:  # Denna sats används för att kontrollera att en bricka har klickats på. Om detta INTE skett vill vi att programmet skickar tillbaka kort som hålls i handen (eftersom att kort inte får läggas utanför brickor).
            if theEvent.type == pygame.MOUSEBUTTONUP:  # Satserna med breakFromTheLoop förhindrar att mer än ett kort används vid samma nertryck med musen. Utan denna sats kan två kort plockas upp på samma klick, vilket kan orsaka problem.
                breakFromTheLoop = False
            if breakFromTheLoop == True:
                break

            # ========== EN EFFEKT HAR AKTIVERATS. CHECK: HAR ETT KORT KLICKATS OCH ÄR DET GILTIGT ATT AKTIVERA EFFEKTEN PÅ DET KORTET? AKTIVERA ISÅFALL EFFEKTEN. ==========
            if globalaVariabler.aktiveraEffekt == "Ja":
                #print("Nu ska en effekt aktiveras. Inväntar klick på ett kort som effekten ska tillämpas på.")
                upplyftKort.isTheCardUpplyft = True
                if enBrickaHarKlickats == False and theEvent.type == pygame.MOUSEBUTTONDOWN and effektKnapp.hitBox.collidepoint(theEvent.pos) == False:
                    print("Ett kort hölls i handen och klicket gjordes utanför en bricka. Kortet skickas tillbaka.")
                    skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)
                    globalaVariabler.aktiveraEffekt = "Nej"
                    if spelaresTur == 1:  # Ger tillbaka spelaren sitt förlorade drag.
                        spelare1.amountOfMovesOnTheField -= 1
                    else:
                        spelare2.amountOfMovesOnTheField -= 1
                if theEvent.type == pygame.MOUSEBUTTONDOWN and bricka.hitBox.collidepoint(theEvent.pos):
                    print("En bricka klickades.")
                    if bricka.holdsCardNumber != 0:
                        print("Brickan var inte tom")

                        hanteraManuellaEffekter(bricka, upplyftKort, sparadBricka, globalaVariabler, spelaresTur)

                    else:
                        print("Brickan var tom. Effekten kan inte appliceras där.")
                        skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)
                        globalaVariabler.aktiveraEffekt = "Nej"
                        if spelaresTur == 1:  # Ger tillbaka spelaren sitt förlorade drag.
                            spelare1.amountOfMovesOnTheField -= 1
                        else:
                            spelare2.amountOfMovesOnTheField -= 1

            # ========== ETT KORT ÄR MARKERAT. CHECK: HAR ETT KORT KLICKATS OCH KAN DET LÄGGAS NER I EN TOM BRICKA ELLER INTERAGERA MED ETT ANNAT KORT? ==========
            elif globalaVariabler.aCardIsBeingHeld == True:

                if enBrickaHarKlickats == False and theEvent.type == pygame.MOUSEBUTTONDOWN and effektKnapp.hitBox.collidepoint(theEvent.pos) == False :
                    print("Ett kort hölls i handen och klicket gjordes utanför en bricka. Kortet skickas tillbaka.")
                    skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)
                if theEvent.type == pygame.MOUSEBUTTONDOWN and bricka.hitBox.collidepoint(theEvent.pos):
                    print("En bricka klickades på OCH ETT KORT HÖLLS I HANDEN. Brickan höll kortet " + str(bricka.holdsCardColor) + str(bricka.holdsCardNumber) + " Koordinater: " + str(bricka.givetTal))
                    enBrickaHarKlickats = True

                    # === OM KORTET SOM KLICKATS LIGGER I HANDEN ===
                    if upplyftKort.deckHandPlanGraveyard == "Hand":
                        '''Tillägg: För att senare kunna aktivera korts specialeffekter måste denna del av programmet kunna hantera andra kort än det som är upplyft. Då krävs det att en kort-for-loop läggs in här. '''
                        print("Det markerade kortet låg i handen. Det kan därmed bara läggas ner på PLANBRICKOR för SPELAREN VARS TUR DET ÄR.")
                        if bricka.ownedByPlayer == spelaresTur and bricka.hand_plan == "Plan" and bricka.holdsCardNumber == 0:
                            print("Brickan var en tom planbricka för spelaren vars tur det var. Vi tar för givet att draget är giltigt och lägger ner kortet i brickan. (Och struntar i aktiva effekter som kan appliceras på egna kort.) ")
                            placeCardAtBrick(upplyftKort, bricka, spelare1, spelare2)#Funktionen lägger ner kortet "upplyftKort" på brickan "bricka". s

                            if spelaresTur == 1:  # Registrerar att ett kort lagts ner.
                                spelare1.antalKortLagda += 1
                            elif spelaresTur == 2:
                                spelare2.antalKortLagda += 1
                            print("Spelare 1 har nu lagt såhär många kort: " + str(spelare1.antalKortLagda) + ". Och spelare 2 har lagt: " + str(spelare2.antalKortLagda))
                            break  # Break måste vara här, för om kortet läggs ner i en bricka och for-loopen fortsätter till resterande brickor, blir det knas.
                        else:
                            print("Något av följande påstående var uppfyllt: 1. Brickan tillhörde mostståndaren. 2. Brickan var inte en planbricka. 3. Brickan var occuperad. DRAGET ÄR OGILTIGT.")
                            skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)
                            #Break kan eventuellt läggas till.

                    # === OM KORTET SOM KLICKATS LIGGER PÅ PLANEN: CHECK: HAR ETT MOTSTÅNDARKORT KLICKATS? + HANTERING AV ATTACKFUNKTIONEN ===
                    elif upplyftKort.deckHandPlanGraveyard == "Plan":
                        print("Det markerade kortet låg i planen. Det kan därmed bara läggas ner på PLANBRICKOR för MOTSTÅNDAREN.")
                        if bricka.ownedByPlayer != spelaresTur and bricka.hand_plan == "Plan" and bricka.holdsCardNumber != 0:
                            print("Brickan var en occuperad planbricka för motståndarspelaren. Draget kan dock fortfarande göras ogiltigt av kort passiva effekter. ")

                            determineIfTheAttackIsValid(upplyftKort, bricka)
                            if globalaVariabler.isTheAttackValid == True:
                                handeBattleBetweenTwoCards(   theCardThatWins(upplyftKort.color, upplyftKort.tal, bricka.holdsCardColor, bricka.holdsCardNumber), listaMedAllaKort, bricka, sparadBricka, upplyftKort, spelaresTur, spelare1, spelare2)
                                upplyftKort.isTheCardUpplyft = False  # Notera att detta redan inkluderas i funktionen skickaTillbakaKortet().
                                globalaVariabler.aCardIsBeingHeld = False
                            else:
                                print("Draget var inte giltigt. Kortet skickas tillbaka. ")
                                skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)
                                breakFromTheLoop = True
                        else:
                            print("Något av följande påstående var uppfyllt: 1. Brickan tillhörde spelaren vars tur det var. 2. Brickan var inte en planbricka. 3. Brickan var tom. DRAGET ÄR OGILTIGT.")
                            skickaTillbakaUpplyftKort(upplyftKort, sparadBricka)
                            breakFromTheLoop = True

            # ========== INGET KORT ÄR MARKERAT. CHECK: HAR ETT KORT KLICKATS OCH KAN DET LYFTAS UPP? ==========
            elif globalaVariabler.aCardIsBeingHeld == False:
                for kort in listaMedAllaKort:
                    if theEvent.type == pygame.MOUSEBUTTONDOWN and kort.hitBox.collidepoint(theEvent.pos):
                        if kort.ownedByPlayer == spelaresTur:
                            breakFromTheLoop = True
                            print("Kortet " + str(kort.color) + str(kort.tal) + " klickades. Kortet tillhör spelare " + str(kort.ownedByPlayer) + " och ligger i " + str(kort.deckHandPlanGraveyard))
                            print("Inget kort var markerat. Vi ser om det är giltigt att markera kortet")
                            print("Kortet som klickades tillhörde spelaren vars tur det var. Det är dock ogiltigt att plocka upp kortet om spelaren redan lagt max antal kort, alternativt gjort max antal drag.")
                            kollaOmKortetKanPlockasUpp()

                            if kort.canTheCardBePickedUp == True:
                                print("Det var ett giltigt drag att plocka upp kortet, så det lyfts upp.")
                                print("Brickan innehöll kortet: " + str(theBrickThatHasBeenClicked.holdsCardColor) + " " + str(theBrickThatHasBeenClicked.holdsCardNumber) + ". Brickan töms på detta kort.")
                                kort.isTheCardUpplyft = True
                                globalaVariabler.aCardIsBeingHeld = True
                                upplyftKort = kort
                                globalaVariabler.aCardIsBeingHeld = True
                                sparadBricka = theBrickThatHasBeenClicked
                                theBrickThatHasBeenClicked.holdsCardNumber = 0
                                theBrickThatHasBeenClicked.holdsCardColor = "Ingen"  # Med stor sannolikhet är denna rad inte nödvändig pga att holdsCardNumber=0 redan indikerar att brickan är tom. Jag har dock denna rad för säkerhets skull.
                                break
                            elif kort.canTheCardBePickedUp == False:
                                print("Det var ett ogiltigt drag att plocka upp kortet, så det lyfts inte upp.")
                                # Tidigare har vi sparat koordinaterna vid denna punkt, men i nuläget har vi inga koordinater att spara. Troligtvis ska inget stå här.
                        elif kort.ownedByPlayer != spelaresTur:
                            pass
                            #print("Kortet tillhörde inte spelaren vars tur det var, så det kan inte plockas upp.")
                            #Tidigare har vi sparat koordinaterna vid denna punkt, men i nuläget har vi inga koordinater att spara. Troligtvis ska inget stå här.


            # ========== GER KORTEN DERAS KOORDINATER BEROENDE PÅ POSITION ==========
            for kort in listaMedAllaKort:
                if kort.deckHandPlanGraveyard == "Graveyard":
                    kort.hitBox.center = (250, 530)

            # ========== VÄXLAR MELLAN SPELARNAS TURER ==========


        if theEvent.type == pygame.MOUSEBUTTONDOWN and turKnapp.hitBox.collidepoint(theEvent.pos) and globalaVariabler.aCardIsBeingHeld == False:#Detta kan bytas till ELIF senare, eftersom att endast en knapp kan klickas per theEvent.
            if globalaVariabler.aCardIsBeingHeld == False:
                if spelaresTur == 1:
                    spelaresTur = 2
                    print("Turknappen klickades. Nu är det spelare " + str(spelaresTur) + "s tur.")
                    spelare1.amountOfMovesOnTheField = 0
                    spelare1.antalKortLagda = 0# Resettar spelarens drag från handen och på fältet till 0.
                    if isItTheFirstTurn == False: # Detta motverkar att spelare 2 plockar upp 2 kort under sin första tur.
                        drawCardFromDeck(2,2)  # FUNKTIONEN (dvs ej del av en klass) drawCardFromDeck(a, b) plockar upp b antal kort för spelare a.
                    isItTheFirstTurn = False

                elif spelaresTur == 2:
                    spelaresTur = 1
                    print("Turknappen klickades. Nu är det spelare " + str(spelaresTur) + "s tur.")
                    drawCardFromDeck(1, 2)
                    spelare2.amountOfMovesOnTheField = 0
                    spelare2.antalKortLagda = 0
                break

    #antalDragKnapp.ritaKnapp(VIT, theWindow)
    #visaPassivaKortKnapp.ritaKnapp(VIT, theWindow)
    turKnapp.ritaKnapp(GREEN, theWindow)
    effektKnapp.ritaKnappMedBild("Effect", theWindow)
    defendButton.ritaKnappMedBild("Defend", theWindow)
    restorationKnapp.ritaKnappMedBild("Restoration", theWindow)

    for bricka in listaMedAllaBrickor:
        bricka.ritaBricka(theWindow)

    visaMeddelande(str(spelaresTur), turKnapp.hitBox.center[0], turKnapp.hitBox.center[1], 30, SVART)  # Visar siffran för spelaresTur. Koordinater: turknappens centrum. Storlek: 30

    visaMeddelande("SPELARE 1: Handdrag: " + str(spelare1.antalKortLagda) + "   Plandrag: " + str(spelare1.amountOfMovesOnTheField),
                   antalDragKnapp.hitBox.center[0], antalDragKnapp.hitBox.center[1], 15, SVART)#Skriver ut antal drag för respeketive spelare.
    visaMeddelande("SPELARE 2: Handdrag: " + str(spelare2.antalKortLagda) + "   Plandrag: " + str(spelare2.amountOfMovesOnTheField),
                   antalDragKnapp.hitBox.center[0], antalDragKnapp.hitBox.center[1]-550, 15, SVART)

    visaMeddelande("P1 nior: " + str(spelare1.ninesOnTheField) + "    P2 nior: " + str(spelare2.ninesOnTheField), visaPassivaKortKnapp.hitBox.center[0], visaPassivaKortKnapp.hitBox.center[1], 15, SVART)



    counter = 0
    x = 0
    y = 0
    for kort in listaMedAllaKort:  # Ritar kort genom metoden ritaHitboxOchBild.

        if spelaresTur == 1 and kort.ownedByPlayer == 2 and kort.deckHandPlanGraveyard != "Plan":
            kort.ritaBakgrund(theWindow)
        elif spelaresTur == 2 and kort.ownedByPlayer == 1 and kort.deckHandPlanGraveyard != "Plan":
            kort.ritaBakgrund(theWindow)
        else:
            kort.ritaKortet(72 * x, 97 * y, theWindow)
        if kort.shield != 0:
            kort.ritaGenomskinlig(theWindow, DefendIcon, 10, 3)
        if kort.isTheCardUpplyft == True:
            if globalaVariabler.aktiveraEffekt == "Nej":
                kort.ritaGenomskinlig(theWindow, highlightImage, -15, -15)
            else:
                upplyftKort.ritaGenomskinlig(theWindow, highlightImageInverted, -15, -15)
        x += 1
        if x == 13:
            x = 0
            y += 1
        counter += 1
        if counter == 52:
            x = 0
            y = 0


    pygame.display.update()
    clockvariableForFPS.tick(11)














