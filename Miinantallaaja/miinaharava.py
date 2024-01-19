'''
Miinantallaaja - Tehnyt Jimi Gustafsson

Miinaharava peli, jossa pelaaja voi pelata ennalleen 
määrätyillä  kenttäkoilla tai omavalintaisella koolla.
Pelaajalla on mahdollisuus tallentaa pelikerran tulos tulostaulukkoon.

-----------------------------------------------------------------

Lainattu materiaalista "kokoelma" koodia valikon luomiseksi.
'''

from random import randint
import json
import os
from datetime import datetime
from time import time
import haravasto as ha

asetukset = {
"X_KOKO" : 0,
"Y_KOKO" : 0,
"MIINALKM" : 0
}

ajastin = {"alkuaika" : 0, "loppuaika" : 0, "kulunut" : 0}

kentta = {
"front": [],
"back": [],
"jaljella": [],
"pelitila" : 0,
#pelitila 0 = peli päällä
#pelitila 1 = hävitty
#pelitila 2 = peli voitettu
"aika" : 0
}

PER_SIVU = 5

LOGO = (
    r"           _______ __________________ _        _______  _               ""\n"
    r"          (       )\__   __/\__   __/( (    /|(  ___  )( (    /|        ""\n"
    r"          | () () |   ) (      ) (   |  \  ( || (   ) ||  \  ( |        ""\n"
    r"          | || || |   | |      | |   |   \ | || (___) ||   \ | |        ""\n"
    r"          | |(_)| |   | |      | |   | (\ \) ||  ___  || (\ \) |        ""\n"
    r"          | |   | |   | |      | |   | | \   || (   ) || | \   |        ""\n"
    r"          | )   ( |___) (______) (___| )  \  || )   ( || )  \  |        ""\n"
    r"          |/     \|\_______/\_______/|/    )_)|/     \||/    )_)        ""\n"
    r"                                                                        ""\n"
    r"_________ _______  _        _        _______  _______ _________ _______ ""\n"
    r"\__   __/(  ___  )( \      ( \      (  ___  )(  ___  )\__    _/(  ___  )""\n"
    r"   ) (   | (   ) || (      | (      | (   ) || (   ) |   )  (  | (   ) |""\n"
    r"   | |   | (___) || |      | |      | (___) || (___) |   |  |  | (___) |""\n"
    r"   | |   |  ___  || |      | |      |  ___  ||  ___  |   |  |  |  ___  |""\n"
    r"   | |   | (   ) || |      | |      | (   ) || (   ) |   |  |  | (   ) |""\n"
    r"   | |   | )   ( || (____/\| (____/\| )   ( || )   ( ||\_)  )  | )   ( |""\n"
    r"   )_(   |/     \|(_______/(_______/|/     \||/     \|(____/   |/     \|""\n"
    r"                                                                          "                                                                                                                            
    )

def main():
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
    kentta["front"] = []
    kentta["back"] = []
    kentta["jaljella"] = []
    kentta["pelitila"] = 0
    kentta["aika"] = 0
    ajastin["alku"] = time()
    luo_kentat(asetukset["X_KOKO"], asetukset["Y_KOKO"])
    miinoita(kentta["back"], kentta["jaljella"], asetukset["MIINALKM"])
    ha.lataa_kuvat("spritet")
    ha.luo_ikkuna(asetukset["X_KOKO"]*40, asetukset["Y_KOKO"]*40 + 50)
    ha.aseta_piirto_kasittelija(piirra_kentta)
    ha.aseta_hiiri_kasittelija(hiiri_kasittelija)
    ha.aloita()

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    ha.tyhjaa_ikkuna()
    ha.piirra_tausta()
    ha.aloita_ruutujen_piirto()
    ajastin["loppuaika"] = time()
    ajastin["kulunut"] = round(ajastin["loppuaika"] - ajastin["alku"])
    #1.1.70+sekuntteja - 1.1.70+vähemmän sekuntteja
    for i, j in enumerate(kentta["front"]):
        for k, ruutu in enumerate(j):
            ha.lisaa_piirrettava_ruutu(ruutu, k*40, i*40)
    if kentta["pelitila"] == 1:
        for i, j in enumerate(kentta["back"]):
            for k, ruutu in enumerate(j):
                if "x" in ruutu:
                    kentta["front"][i][k] = kentta["back"][i][k]
    if len(kentta["jaljella"]) == 0:
        kentta["pelitila"] = 2
    ha.piirra_tekstia("🗙", asetukset["X_KOKO"] * 40 - 40, asetukset["Y_KOKO"] \
    * 40 + 2, vari=(200, 0, 0, 255), fontti="Arial", koko=32)
    ha.piirra_tekstia("⛭", asetukset["X_KOKO"] * 40 - 80, asetukset["Y_KOKO"] \
    * 40, vari=(110, 110, 110, 255), fontti="Arial", koko=32)
    if kentta["pelitila"] == 0:
        ha.piirra_tekstia(str(ajastin["kulunut"]), 0, asetukset["Y_KOKO"] \
        * 40, vari=(200, 0, 0, 255), fontti="Arial", koko=32)
    else:
        ha.piirra_tekstia("🖫", asetukset["X_KOKO"] * 40 - 120, asetukset["Y_KOKO"] \
        * 40, vari=(110, 110, 110, 255), fontti="Arial", koko=32)
        if asetukset["X_KOKO"] > 6:
            if kentta["pelitila"] == 1:
                ha.piirra_tekstia("Hävisit!", 0, asetukset["Y_KOKO"] * \
                40, vari=(255, 51, 51, 255), fontti="Arial", koko=32)
            else:
                ha.piirra_tekstia("Voitit!", 0, asetukset["Y_KOKO"] * \
                40, vari=(51, 180, 51, 255), fontti="Arial", koko=32)
        else:
            if kentta["pelitila"] == 1:
                ha.piirra_tekstia("L", 6, asetukset["Y_KOKO"] * \
                40, vari=(255, 51, 51, 255), fontti="Arial", koko=32)
            else:
                ha.piirra_tekstia("W", 6, asetukset["Y_KOKO"] * \
                40, vari=(51, 180, 51, 255), fontti="Arial", koko=32)
    ha.piirra_ruudut()

def luo_kentat(kenttax, kenttay):
    '''
    Luo kentänhallintaa varten tarvittavat eri tason kentät,
    frontend: Mitä pelaaja näkee, päivittyy sitä mukaan mitä saa tietoa backendistä
    backend: Mitä kentällä sijaitsee, kentän tiedot luodaan pelin alussa
    jaljella: Mihin ei olla sijoitettu pommia. Käytetään backend -kentän luomisessa
    '''
    for _ in range(kenttay):
        kentta["front"].append([])
        for _ in range(kenttax):
            kentta["front"][-1].append(" ")
    #Luo tyhjän kentän alkuun, tietoa tulee lisää mitä backendistä pyydetään.
    for _ in range(kenttay):
        kentta["back"].append([])
        for _ in range(kenttax):
            kentta["back"][-1].append("0")
    #luo pelikentän, johon sijoitetaan kentän arvot (toistaiseksi tyhjää)
    for x in range(kenttax):
        for y in range(kenttay):
            kentta["jaljella"].append((x, y))
    #luo listan tyhjistä (miinattomista) koordinaateista miinoitusta varten 
    #(x, y) ennen miinoitusta kaikki ovat tyhjiä.
    
def miinoita(miinakentta, vapaat, miinat):
    """
    Asettaa kentälle N kpl miinoja satunnaisiin paikkoihin.
    """
    asetettu = 0
    while asetettu < miinat:
        miinoitettava = randint(0, (len(vapaat) - 1))
        #index 1 = rivi, index2 = sarake
        index1, index2 = vapaat[miinoitettava][0], vapaat[miinoitettava][1]
        miinakentta[index2][index1] = "x"
        #nyt generoituun kohtaan laitetaan miina, nyt asetetaan numerot miinan viereen.
        scan_x = index1 - 1
        scan_y = index2 - 1
        for _ in range(3):
            if scan_y < 0:
                scan_y += 1
                continue
                #jos skannattavan kohdan y pienempi kuin 0 ei 
                #tietenkään voida skannata vaan siirrytään seuraavaan.
            try:
                for _ in range(3):
                    if scan_x < 0:
                        scan_x += 1
                        continue
                        #Jos skannattavan kohdan x pienempi kuin 0, siirrytään seuraavaan.
                    try:
                        ruutu = miinakentta[scan_y][scan_x]
                    except IndexError:
                        scan_x += 1
                        continue
                        #Jos x menee yli kentän rajojen, 
                        #siirrytään seuraavaan, pidetään looppi päällä
                    else:
                        if "0" in ruutu:
                            miinakentta[scan_y][scan_x] = "1"
                            #jos ruutu on tyhjä, asetetaan ensimmäinen vieruusnumero eli yksi
                        elif not "x" in ruutu:
                            miinakentta[scan_y][scan_x] = int(miinakentta[scan_y][scan_x])
                            miinakentta[scan_y][scan_x] += 1
                            miinakentta[scan_y][scan_x] = str(miinakentta[scan_y][scan_x])
                            #Kunhan ruudussa ei ole miinaa jo valmiina mutta on jo 
                            #todettu aiempi miina tämän vieressä, lisätään yksi.
                        scan_x += 1
                        #Kierros käyty läpi, siirrytään seuraavaan
            except IndexError:
                scan_y += 1
                continue
                #Jos y menee ali kentän rajojen, siirrytään seuraavaan.
            else:
                scan_y += 1
                scan_x -= 3
                #siirrytään seuraavalle sarakkeelle ja aloitetaan 
                #scannaus vasemmalta miinasta katsottuna
        del vapaat[miinoitettava]
        #poistaa vapaiden koordinaattien listasta tämän koordinaatin
        asetettu += 1

def hiiri_kasittelija(x, y, painike, muokkausnapit):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Kerää painetun kohdan sijainnin x, y koordinaatilla ja mitä painettu
    Tarkistaa myös mitä annetussa x, y koordinaatissa on:
    1. Jos lippu
        1.1. Painettu oikealla hiiren näppäimellä, poista
        1.2. Painettu vasemmalla, sivuuta.
    2. Jos pommi, GAME OVER
    3. Jos numero, paljasta
    4. Jos tyhjää, TULVA
        4.1 Jos frontend tyhjää ja painettu oikealla hiiren näppäimellä, aseta lippu
    """
    x = x // 40
    y = y // 40
    nakyva = kentta["front"]
    miinakentta = kentta["back"]
    #ruudun koko 40, jakamalla tällä saadaan käyttökelpoista inputtia
    #vasen == 1, oikea == 4 
    if x < asetukset["X_KOKO"] and y < asetukset["Y_KOKO"]:
        if kentta["pelitila"] == 0:
            if painike == 4: 
                if nakyva[y][x] == " ":
                    nakyva[y][x] = "f"
                elif nakyva[y][x] == "f":
                    nakyva[y][x] = " "
                    #Kaksi ylempää asettaa tai poistaa lipun.
            elif painike == 1:
                if nakyva[y][x] == "f":
                    pass
                    #Jos pelaaja asettanut lipun, ei reagoida mitenkään 
                    #vasempaan hiiren painallukseen tässä ruudussa
                elif miinakentta[y][x] == "x":
                    kentta["pelitila"] = 1
                    #Jos painaa vasemmalla hiiren painalluksella pommiin == GAME OVER!!!
                elif miinakentta[y][x] == "0" and nakyva[y][x] == " ":
                    tulvataytto(miinakentta, nakyva, x, y, painike)
                elif nakyva[y][x] == " ":
                    nakyva[y][x] = miinakentta[y][x]
                    del kentta["jaljella"][-1]
                    #muut vaihtoehdot käyty läpi, ruudussa voi olla vain numero
        elif kentta["pelitila"] == 1 or kentta["pelitila"] == 2:
            main()
    if painike == 1:
        if x == asetukset["X_KOKO"] - 1 and y == asetukset["Y_KOKO"]:
            ha.lopeta()
            paavalikko()
        elif x == asetukset["X_KOKO"] - 2 and y == asetukset["Y_KOKO"]:
            ha.lopeta()
            oma_peli()
        elif x == asetukset["X_KOKO"] - 3 and y == asetukset["Y_KOKO"] and kentta["pelitila"] > 0:
            lisaa_tilasto(data)
            tallenna_tilasto(data, "tilastot.json")
            main()
    if kentta["pelitila"] != 0:
        kulunut_aika = str(ajastin["kulunut"])[:]
        kentta["aika"] = kulunut_aika
            

def tulvataytto (miinakentta, nakyva, x, y, painettu):
    """
    Tarkistaa mitä annetussa x, y koordinaatissa on:
    1. Jos lippu
        1.1. Painettu oikealla hiiren näppäimellä, poista
        1.2. Painettu vasemmalla, sivuuta.
    2. Jos pommi, GAME OVER
    3. Jos numero, paljasta
    4. Jos tyhjää, TULVA
        4.1 Jos frontend tyhjää ja painettu oikealla hiiren näppäimellä, aseta lippu
    """
    
    tarkistettavat = [y, x]
    while len(tarkistettavat) > 0:
    #aloitetaan skannaamaan ruutuja
        scan_y = tarkistettavat [-2]
        scan_x = tarkistettavat [-1]
        scan_y -= 1
        scan_x -= 1
        #Koska operaatio voi olla raskas, ovat koordinaatit yhdellä 
        #pitkällä listalla, parittomat y ja parilliset x koordinaatteja.
        del tarkistettavat[-2:]
        #poistaa kaksi viimeistä arvoa listalta. Sijainti tallennettu jo muuttujiin
        for _ in range(3):
            if scan_y < 0:
                scan_y += 1
                continue
                #jos skannattavan kohdan y pienempi kuin 0 ei tietenkään 
                #voida skannata vaan siirrytään seuraavaan.
            try:
                for _ in range(3):
                    if scan_x < 0:
                        scan_x += 1
                        continue
                        #Jos skannattavan kohdan x pienempi kuin 0, siirrytään seuraavaan.
                    try:
                        ruutu = miinakentta[scan_y][scan_x]
                        nahtyjo = nakyva[scan_y][scan_x]
                    except IndexError:
                        scan_x += 1
                        continue
                        #Jos x menee yli kentän rajojen, siirrytään seuraavaan, 
                        #pidetään looppi päällä
                    else:
                        if "0" in ruutu and nahtyjo == " ":
                            nakyva[scan_y][scan_x] = miinakentta[scan_y][scan_x]
                            tarkistettavat.extend((scan_y, scan_x))
                            del kentta["jaljella"][-1]
                            #jos " " ruudussa, tehdään siitä näkyvä frontendissä ja 
                            #lisätään ruutu tarkistettavien listalle
                        elif int(ruutu) in range(1, 9) and nahtyjo == " ":
                            nakyva[scan_y][scan_x] = miinakentta[scan_y][scan_x]
                            del kentta["jaljella"][-1]
                            #jos numero ruudussa, tehdään siitä näkyvä frontendissä
                        scan_x += 1
                        #Kierros käyty läpi, siirrytään seuraavaan
            except IndexError:
                scan_y += 1
                continue
                #Jos y menee ali kentän rajojen, siirrytään seuraavaan.
            else:
                scan_y += 1
                scan_x -= 3
                #siirrytään seuraavalle sarakkeelle ja aloitetaan 
                #scannaus vasemmalta miinasta katsottuna   
        

def lataa_tilasto(tiedosto):
    '''
    Lataa tilastotiedoston, 
    jos sitä ei ole, luodaan uusi
    '''
    try:
        with open(tiedosto, encoding="utf8") as lahde:
            tilasto = json.load(lahde)
    except (IOError, json.JSONDecodeError):
        tilasto = []
        tallenna_tilasto(tilasto, tiedosto)
    return tilasto
    
def tallenna_tilasto(tilasto, tiedosto):
    '''
    Tallentaa tilastotiedon pythonista ulkoiseen
    json tiedostoon.
    '''
    try:
        with open(tiedosto, "w", encoding="utf8") as kohde:
            json.dump(tilasto, kohde)
    except IOError:
        print("Pelidataa ei voitu tallentaa. Suoritus ei tallentunut")
        
def lisaa_tilasto(tilasto):
    '''
    Lisää pelin tilaston ladattuun tilastoon.
    Pitää tallentaa tallenna_tiedosto a käyttäen
    '''
    pvm = datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
    kenttakoko = asetukset["X_KOKO"] * asetukset["Y_KOKO"] 
    avaamatta = len(kentta["jaljella"])
    if not kentta["jaljella"]:
        voittiko = "Voitto!"
    else:
        voittiko = "Tappio"
    tilasto.append({
        "tulos": voittiko,
        "avaamatta": avaamatta,
        "kenttakoko": kenttakoko,
        "miinoja": asetukset["MIINALKM"],
        "kesto": str(kentta["aika"]),
        "aika": pvm
    })
    
def paavalikko():
    '''
    Pelin päävalikko.
    '''
    os.system('cls')
    print(LOGO)
    print("1. Aloita\n2. Custom peli\n3. Tilastot\n4. Lopeta\n")
    while True:
        valinta = input("\nAnna syöte: ").replace(" ", "")
        if valinta == "1":
            pika_aloitus()
            break
        if valinta == "2":
            oma_peli()
            break
        if valinta == "3":
            nayta_tilastot(data)
            break
        if valinta in ("4",""):
            os.system('cls')
            break
        print("Väärä syöte!")

def pika_aloitus():
    '''
    Valikko sisältää pika-aloitusvaihtoehdot
    Avataan päävalikon kautta
    '''
    os.system('cls')
    print(LOGO)
    print("1. Helppo\n2. Keskivaikea\n3. Vaikea\n4. Hyvin vaikea\n5. Takaisin\n")
    while True:
        valinta = input("\nAnna syöte: ").replace(" ", "")
        if valinta == "1":
            asetukset["X_KOKO"] = 7
            asetukset["Y_KOKO"] = 7
            asetukset["MIINALKM"] = 8
            main()
            break
        if valinta == "2":
            asetukset["X_KOKO"] = 10
            asetukset["Y_KOKO"] = 10
            asetukset["MIINALKM"] = 15
            main()
            break
        if valinta == "3":
            asetukset["X_KOKO"] = 15
            asetukset["Y_KOKO"] = 15
            asetukset["MIINALKM"] = 35
            main()
            break
        if valinta == "4":
            asetukset["X_KOKO"] = 20
            asetukset["Y_KOKO"] = 20
            asetukset["MIINALKM"] = 70
            main()
            break
        if valinta in ("5",""):
            paavalikko()
            break
        print("Väärä syöte!")
    
def oma_peli():
    '''
    Tässä valikossa voi määrittää itsellensä
    mieluisan pelialueen mitat ja miinojen määrän.
    Avataan päävalikon tai pelin "asetukset"-kuvakkeen kautta
    '''
    os.system('cls')
    print(LOGO)
    print("Anna kentän mitat. Jokainen ruutu on 40x40 kokoinen.\n\n"
        "Esim. Suositeltu enimmäiskoko 1920x1080 ruudulle on 48x26\nVähimmäiskoko on 5x5\n\n"
        "Anna kentän mitat kokonaislukuina muodossa leveys x korkeus x miina lkm\n\n"
        "Jätä tyhjäksi palataksesi päävalikkoon\n")
    while True:
        valinta = input("\nAnna syöte: ").replace(" ", "").lower().split("x")
        if valinta == ['']:
            paavalikko()
            break
        try:
            asetukset["X_KOKO"], asetukset["Y_KOKO"], \
            asetukset["MIINALKM"] = list(map(int, valinta))
            if asetukset["X_KOKO"] < 5 or asetukset["Y_KOKO"] < 5:
                print("Liian pieni kenttä!")
            elif asetukset["MIINALKM"] >= asetukset["X_KOKO"] * asetukset["Y_KOKO"]:
                print("Miinoja ei voi olla enemmän kuin kentällä on tilaa!")
            elif asetukset["X_KOKO"] > 48 or asetukset["Y_KOKO"] > 26:
                yesno = input("Kentän koko ylittää 1920x1080 ruudulle suositellut maksimimitat."
                "\n Pelin toiminta ei ole taattu Jatketaanko (y/n)?: ").replace(" ", "").lower()
                if yesno == "n":
                    continue
                if yesno == "y":
                    main()
                    break
                if yesno == "":
                    paavalikko()
                    break
                else:
                    print("Väärä syöte!")
            else:
                main()
                break
        except (AttributeError, ValueError):
            print("väärä syöte!")
                
def nayta_tilastot(tilasto):
    '''
    Tämä valikkosivu näyttää tilastot.
    Näyttää top 5 parhaimmat, nopeimmat ja huonoimmat suoritukset
    Valikon kautta voidaan myös nollata tilastot
    '''
    os.system('cls')
    print(LOGO)
    print("TOP 5 PARHAIMMAT\n------------------")
    for i in range(5):
        alku = i * PER_SIVU
        tilasto.sort(reverse=True, key=lajittele_paras)
        muotoile_tilastot(tilasto[alku:5])
    print("--------------------------------------\n")
    print("TOP 5 NOPEIMMAT\n------------------")
    for i in range(5):
        alku = i * PER_SIVU
        tilasto.sort(key=lajittele_nopein)
        muotoile_tilastot(tilasto[alku:5])
    print("--------------------------------------\n")
    print("TOP 5 HUONOIMMAT\n------------------")
    for i in range(5):
        alku = i * PER_SIVU
        tilasto.sort(reverse=False, key=lajittele_paras)
        muotoile_tilastot(tilasto[alku:5])
    print('\n\nKirjoita "NollaaTilastot" tyhjätäksesi tilastot.\nSinun tulee käynnistää sovellus '
        'uudestaan tämän jälkeen.\n\nJätä tyhjäksi palataksesi päävalikkoon')
    while True:
        valinta = input("\nAnna syöte: ").replace(" ", "")
        if valinta == "":
            paavalikko()
            break
        elif valinta == "NollaaTilastot":
            yesno = input("Oletko varma (y/n)?: ").replace(" ", "").lower()
            if yesno == "n":
                continue
            elif yesno == "y":
                tilasto = []
                tallenna_tilasto(tilasto, "tilastot.json")
                os.system('cls')
                break
            elif yesno == "":
                paavalikko()
                break
            else:
                print("Väärä syöte!")
        else:
            print("Väärä syöte!")
            
    
def muotoile_tilastot(rivit):
    '''
    Muotoilee tilastot nayta_tilastot funktiota varten
    '''
    for i, data in enumerate(rivit):
        print(
            f"{i+1}.{data['tulos']}   Avaamatta: {data['avaamatta']}\n"
            f"Kentän koko: {data['kenttakoko']}   Miinoja: {data['miinoja']} \n"
            f"Pelin kesto: {data['kesto']}s   {data['aika']}\n"
        )
        
def lajittele_paras(tilasto):
    '''
    Lajittelee tilaston 1. Tuloksen (voitto/häviö mukaan) 
    2. Kentän koon ja 3. miinojen määrän mukaan
    '''
    return len(tilasto["tulos"]), tilasto["kenttakoko"], tilasto["miinoja"]
    
def lajittele_nopein(tilasto):
    '''
    Lajittelee tilaston nopeusjärjestyksessä,
    eli kuinka kauan tuloksen saantiin meni.
    '''
    return tilasto["kesto"]

if __name__ == "__main__":
    
    data = lataa_tilasto("tilastot.json")
    paavalikko()
