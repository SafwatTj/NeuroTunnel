import pygame
import sys
import math

# Farben (Deutsch)
GRUEN = (50, 200, 50)
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
GRAU = (100, 100, 100)
HELLGRAU = (150, 150, 150)

# Fenster
BREITE = 800
HOEHE = 600

# Knopf Definitionen (x, y, breite, hoehe)
KNOEPFE = {
    "8_hz": pygame.Rect(50, HOEHE - 60, 80, 40),
    "10_hz": pygame.Rect(150, HOEHE - 60, 80, 40),
    "12_hz": pygame.Rect(250, HOEHE - 60, 80, 40),
    "start": pygame.Rect(370, HOEHE - 60, 100, 40),
    "stop": pygame.Rect(490, HOEHE - 60, 80, 40)
}

# Standard Frequenz
AKTUELLE_FREQUENZ = 8

# Timer
letzte_flimmer_zeit = 0
flimmer_aktiv = True
programm_laeuft = True
session_aktiv = False
start_zeit = 0


def zeichne_tunnel(fenster, breite, hoehe):
    """Zeichnet einen grünen Tunnel mit konzentrischen Kreisen"""
    mitte_x = breite // 2
    mitte_y = hoehe // 2 - 50  # Etwas nach oben versetzt wegen Knöpfen

    max_radius = int(hoehe * 0.4)
    anzahl_kreise = 30

    for i in range(anzahl_kreise):
        radius = int(max_radius * (1 - i / anzahl_kreise))
        farb_wert = int(50 + 205 * (1 - i / anzahl_kreise))
        farbe = (0, farb_wert, 0)
        pygame.draw.circle(fenster, farbe, (mitte_x, mitte_y), radius, 2)


def zeichne_knopfe(fenster, aktiv_frequenz, session_aktiv):
    """Zeichnet die Buttons mit aktuellen Farben"""
    schrift = pygame.font.Font(None, 28)

    # 8 Hz Knopf
    farbe = GRUEN if aktiv_frequenz == 8 else GRAU
    pygame.draw.rect(fenster, farbe, KNOEPFE["8_hz"])
    text = schrift.render("8 Hz", True, SCHWARZ)
    fenster.blit(text, (KNOEPFE["8_hz"].x + 15, KNOEPFE["8_hz"].y + 8))

    # 10 Hz Knopf
    farbe = GRUEN if aktiv_frequenz == 10 else GRAU
    pygame.draw.rect(fenster, farbe, KNOEPFE["10_hz"])
    text = schrift.render("10 Hz", True, SCHWARZ)
    fenster.blit(text, (KNOEPFE["10_hz"].x + 10, KNOEPFE["10_hz"].y + 8))

    # 12 Hz Knopf
    farbe = GRUEN if aktiv_frequenz == 12 else GRAU
    pygame.draw.rect(fenster, farbe, KNOEPFE["12_hz"])
    text = schrift.render("12 Hz", True, SCHWARZ)
    fenster.blit(text, (KNOEPFE["12_hz"].x + 10, KNOEPFE["12_hz"].y + 8))

    # Start Knopf
    if not session_aktiv:
        pygame.draw.rect(fenster, GRUEN, KNOEPFE["start"])
        text = schrift.render("START", True, SCHWARZ)
    else:
        pygame.draw.rect(fenster, GRAU, KNOEPFE["start"])
        text = schrift.render("START", True, (50, 50, 50))
    fenster.blit(text, (KNOEPFE["start"].x + 18, KNOEPFE["start"].y + 8))

    # Stop Knopf
    if session_aktiv:
        pygame.draw.rect(fenster, (255, 50, 50), KNOEPFE["stop"])
        text = schrift.render("STOP", True, SCHWARZ)
    else:
        pygame.draw.rect(fenster, GRAU, KNOEPFE["stop"])
        text = schrift.render("STOP", True, (50, 50, 50))
    fenster.blit(text, (KNOEPFE["stop"].x + 18, KNOEPFE["stop"].y + 8))


def zeige_epilepsie_warnung(fenster):
    schrift = pygame.font.Font(None, 36)
    schrift_klein = pygame.font.Font(None, 24)

    fenster.fill(SCHWARZ)

    text1 = schrift.render("ACHTUNG - EPILEPSIE WARNUNG", True, (255, 0, 0))
    text2 = schrift_klein.render("Blinkendes Licht (8-12 Hz) - Nicht bei Epilepsie verwenden!", True, WEISS)
    text3 = schrift_klein.render("Druecke eine beliebige Taste zum Fortfahren...", True, WEISS)

    fenster.blit(text1, (BREITE // 2 - text1.get_width() // 2, HOEHE // 2 - 50))
    fenster.blit(text2, (BREITE // 2 - text2.get_width() // 2, HOEHE // 2))
    fenster.blit(text3, (BREITE // 2 - text3.get_width() // 2, HOEHE // 2 + 80))

    pygame.display.flip()

    warten = True
    while warten:
        for ereignis in pygame.event.get():
            if ereignis.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ereignis.type == pygame.KEYDOWN:
                warten = False


def main():
    global AKTUELLE_FREQUENZ, letzte_flimmer_zeit, flimmer_aktiv
    global programm_laeuft, session_aktiv, start_zeit

    pygame.init()
    fenster = pygame.display.set_mode((BREITE, HOEHE))
    pygame.display.set_caption("NeuroTunnel - Entwickelt von Safwat Burkhonov")

    zeige_epilepsie_warnung(fenster)

    uhr = pygame.time.Clock()
    letzte_flimmer_zeit = pygame.time.get_ticks()
    flimmer_aktiv = True
    programm_laeuft = True
    session_aktiv = False

    schrift_gross = pygame.font.Font(None, 48)
    schrift_klein = pygame.font.Font(None, 28)
    schrift_name = pygame.font.Font(None, 20)

    while programm_laeuft:
        for ereignis in pygame.event.get():
            if ereignis.type == pygame.QUIT:
                programm_laeuft = False

            if ereignis.type == pygame.MOUSEBUTTONDOWN:
                maus_pos = pygame.mouse.get_pos()

                # Frequenz Knöpfe (nur wenn keine Session läuft)
                if not session_aktiv:
                    if KNOEPFE["8_hz"].collidepoint(maus_pos):
                        AKTUELLE_FREQUENZ = 8
                    if KNOEPFE["10_hz"].collidepoint(maus_pos):
                        AKTUELLE_FREQUENZ = 10
                    if KNOEPFE["12_hz"].collidepoint(maus_pos):
                        AKTUELLE_FREQUENZ = 12

                # Start Knopf
                if KNOEPFE["start"].collidepoint(maus_pos) and not session_aktiv:
                    session_aktiv = True
                    start_zeit = pygame.time.get_ticks()
                    letzte_flimmer_zeit = pygame.time.get_ticks()
                    flimmer_aktiv = True

                # Stop Knopf
                if KNOEPFE["stop"].collidepoint(maus_pos) and session_aktiv:
                    session_aktiv = False

            if ereignis.type == pygame.KEYDOWN:
                if ereignis.key == pygame.K_ESCAPE:
                    programm_laeuft = False

        aktuelle_zeit = pygame.time.get_ticks()

        if session_aktiv:
            vergangene_sekunden = (aktuelle_zeit - start_zeit) / 1000.0

            # 60 Sekunden Session
            if vergangene_sekunden >= 60:
                session_aktiv = False
            else:
                # Flimmern mit aktueller Frequenz
                intervall_ms = 1000.0 / AKTUELLE_FREQUENZ
                if aktuelle_zeit - letzte_flimmer_zeit >= intervall_ms:
                    flimmer_aktiv = not flimmer_aktiv
                    letzte_flimmer_zeit = aktuelle_zeit

                # Zeichnen mit Flimmern
                if flimmer_aktiv:
                    fenster.fill(SCHWARZ)
                    zeichne_tunnel(fenster, BREITE, HOEHE)
                else:
                    fenster.fill(SCHWARZ)

                # Status anzeigen
                verbleibend = int(60 - vergangene_sekunden)
                text_timer = schrift_klein.render(f"Zeit: {verbleibend} s", True, WEISS)
                fenster.blit(text_timer, (10, 10))
                text_freq = schrift_klein.render(f"{AKTUELLE_FREQUENZ} Hz", True, GRUEN)
                fenster.blit(text_freq, (10, 40))
        else:
            # Ruhezustand - keine Session aktiv
            fenster.fill(SCHWARZ)
            zeichne_tunnel(fenster, BREITE, HOEHE)

            text_wahl = schrift_gross.render(f"{AKTUELLE_FREQUENZ} Hz", True, GRUEN)
            fenster.blit(text_wahl, (BREITE // 2 - text_wahl.get_width() // 2, HOEHE // 2 - 100))

            text_info = schrift_klein.render("Waehle Frequenz (8,10,12 Hz) und druecke START", True, WEISS)
            fenster.blit(text_info, (BREITE // 2 - text_info.get_width() // 2, HOEHE // 2 - 20))

        # Dein Name in Grün
        text_name = schrift_name.render("Entwickelt von Safwat Burkhonov", True, GRUEN)
        fenster.blit(text_name, (BREITE - text_name.get_width() - 10, HOEHE - 25))

        # Knöpfe zeichnen
        zeichne_knopfe(fenster, AKTUELLE_FREQUENZ, session_aktiv)

        pygame.display.flip()
        uhr.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()