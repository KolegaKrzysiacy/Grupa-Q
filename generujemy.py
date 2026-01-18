import random
# import mysql.connector

# con = mysql.connector.connect(
#   host="localhost",
#   user="admin",
#   password="admin",
#   database="grupaq"
# )

# mycursor = con.cursor()

# na razie nie ma:
# - testów antydopingowych i substancji
# - ważenia


random.seed(42)

DNI_W_ROKU = 365.2425
SEKUNDY_W_DNIU = 86400
SEKUNDY_W_ROKU = DNI_W_ROKU*SEKUNDY_W_DNIU

IMIONA = ["Adam", "Bartek", "Paweł", "Janusz"]
NAZWISKA = ["Nowak", "Kowalski", "Mikke"]

def bida_rozklad_normalny(a, b): # tak sie serio robi ponoć (https://en.wikipedia.org/wiki/Irwin–Hall_distribution)
    return (random.uniform(a, b)+random.uniform(a, b)+random.uniform(a, b))/3

# 20 właścicieli chomików
# - imie
# - nazwisko
# - numer telefonu
wlasciciele = []
for _ in range(20):
    imie = random.choice(IMIONA)
    nazwisko = random.choice(NAZWISKA)
    nr_tel = random.randint(100000000, 999999999)
    wlasciciele.append((imie, nazwisko, nr_tel))

# rasy chomików (ręcznie)
rasy = ["Syryjski", "Dżungarski", "Roborowskiego"]

# robimy 100 chomików:
# - imie: na razie "Chomik i"
# - rasa
# - data urodzenia: od 2018 do 2024 (rozkład jednostajny)
# - data zakończenia aktywności: data urodzenia plus od 1.5 do 3 lat (bida rozkład normalny)
chomiki = []
for i in range(100):
    imie = f"Chomik {i}"
    rasa = random.choice(rasy)
    data_urodzenia = random.randrange(1514761200, 1735686000)
    # Czy data dołączenia potrzebna? --- Wydaje mi się że raczej tak, żeby wiedzieć ile on biega i bierze ogólnie udział w zawodach, bo nie biegają od momentu urodzenia
    czas_kariery = int(bida_rozklad_normalny(1.5, 3)*SEKUNDY_W_ROKU)
    data_zakonczenia_aktywnosci = data_urodzenia + czas_kariery
    chomiki.append((imie, rasa, data_urodzenia, data_zakonczenia_aktywnosci))

# teraz stanowiska pracownikow (ręcznie)
# Czy powinni wszyscy na jednym stanowisku dostawać tyle samo? --- Wydaje mi się żę nie ma sensu zbyt komplikować, jak coś to moża dodać kolumne premia czy coś w wtedy wynagrodzenie to suma
stanowiska = [("Koordynator zawodów", 6100), ("Sędzia", 5900), ("Sprzątacz", 4900)]
id_stanowisk = {}
for i, (stanowisko, _) in enumerate(stanowiska):
    id_stanowisk[stanowisko] = i
koordynatorzy = [i for i, s in enumerate(stanowiska) if s[0] == "Koordynator zawodów"]
sedziowie = [i for i, s in enumerate(stanowiska) if s[0] == "Sędzia"]
sprzatacze = [i for i, s in enumerate(stanowiska) if s[0] == "Sprzątacz"]

# pracownicy
# - imie
# - nazwisko
# - id stanowiska
# - data zatrudnienia: od 2021 do 2025
# - data zwolnienia: od daty zatrudnienia do 2025 albo wcale
# - numer telefonu
pracownicy = []
chcemy_pracownikow = ["Koordynator zawodów"]*5 + ["Sędzia"]*8 + ["Sprzątacz"]*15
for stanowisko in chcemy_pracownikow:
    imie = random.choice(IMIONA)
    nazwisko = random.choice(NAZWISKA)
    id_stanowiska = id_stanowisk[stanowisko]
    nr_tel = random.randint(100000000, 999999999)
    data_zatrudnienia = random.randrange(1514761200, 1735686000)
    if random.random() < 0.1: # 10% szans że już nie ma
        data_zwolnienia = random.randrange(data_zatrudnienia, 1735686000)
    else:
        data_zwolnienia = None
    pracownicy.append((imie, nazwisko, id_stanowiska, data_zatrudnienia, data_zwolnienia, nr_tel))

# teraz 50 zawodów
# - data rozpoczęcia: od 2021 do 2025
# - data zakończenia: po od 3 do 7 dniach (rozkład jednostajny)
# - liczba widzow: od 100 do 1000 jednostajny
# - id_koordynatora
zawody = [] # ! zawody nie będą po kolei + zawody mogą się pokrywać
for _ in range(50):
    data_rozpoczecia = random.randrange(1514761200, 1735686000)
    czas_trwania = random.randint(3, 7)
    data_zakonczenia = data_rozpoczecia + czas_trwania*SEKUNDY_W_DNIU
    liczba_widzow = random.randint(100, 1000)
    id_koordynatora = random.randrange(0, len(koordynatorzy))
    zawody.append((data_rozpoczecia, data_zakonczenia, liczba_widzow, id_koordynatora))

# przeszkody, podłoża, kategorie - recznie
kategorie = ["naturalna", "formuła Ch"]
przeszkody = ["Labirynt", "Rury", "Klocki", "Podesty", "Ścianki"] # Pls wymyśl coś nie mam totalnie pomysłów --- xDDDDDDDDD, chyba git tyle, jak coś to usuń albo dodaj
podloza = ["Trociny", "Trawa", "Ziemia", "Piasek", "Woda"]

# konkurencje - 20 konkurencji losowych
# - nazwa konkurencji: "Konkurencja i"
# - id kategorii
# - id podloza
# - id przeszkody (Czy nie powinno móc być więcej niż jednej?) --- właśnie w sumie to tak lepiej by było chyba
# - długość trasy - od 10 do 100 metrów
konkurencje = []
for i in range(20):
    nazwa_konkurencji = f"Konkurencja {i}"
    id_kategorii = random.randrange(0, len(kategorie))
    id_podloza = random.randrange(0, len(podloza))
    id_przeszkody = random.randrange(0, len(przeszkody))
    dlugosc_trasy = random.randint(10, 100)
    konkurencje.append((nazwa_konkurencji, id_kategorii, id_podloza, id_przeszkody, dlugosc_trasy))

# generujemy rozgrywki dla każdych zawodów - od 10 do 50 na dzień dla każdych zawodów (rozkład normalny):
# - id zawodów
# - id konkurencji
# - data rozgrywki - po kolei dni
# - id sedzi
rozgrywki = []
for id_zawodow, (data_rozpoczecia, data_zakonczenia, liczba_widzow, koordynator) in enumerate(zawody):
    czas_trwania = round((data_zakonczenia - data_rozpoczecia)/SEKUNDY_W_DNIU)
    for dzien in range(czas_trwania):
        liczba_rozgrywek = round(bida_rozklad_normalny(10, 50))
        data_rozgrywki = data_rozpoczecia + dzien*SEKUNDY_W_DNIU
        for _ in range(liczba_rozgrywek):
            id_konkurencji = random.randrange(0, len(konkurencje))
            id_sedzi = random.randrange(0, len(sedziowie))
            rozgrywki.append((id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi))

# modele pojazdów (10)
# - producent: na razie "Producent monopolista" (Kurde no i tabela producenci teraz chyba, tego od chuja będzie, można wyjebać wsm żeby mniej roboty było)
# - nazwa modelu: "Model i"
# - cena modelu: od 100 do 1000zł
modele = []
for i in range(10):
    producent = "Producent monopolista"
    nazwa_modelu = f"Model {i}"
    cena_modelu = random.randint(100, 1000)
    modele.append((producent, nazwa_modelu, cena_modelu))

# pojazdy (od 1*liczba właścicieli do 3*liczba właścicieli)
# - nazwa pojazdu: "Pojazd i"
# - id_modelu: losowy
pojazdy = []
liczba_pojazdow = random.randrange(len(wlasciciele))
for i in range(liczba_pojazdow):
    nazwa_pojazdu = f"Pojazd {i}"
    id_modelu = random.randrange(0, len(modele))
    pojazdy.append((nazwa_pojazdu, id_modelu))

# uczestnictwo (i wyniki) - dla każdej rozgrywki w każdych zawodach
# jak chomik jest w tabeli to uczestniczył a jak nie jest to nie uczestniczył
# - id_rozgrywki
# - id_chomika
# - wynik - jak na razie nie mamy typów rozgrywek ani nic więc liczby od 0 do 1 (Trzeba zrobić czas i miejsce z tego)
# - id_pojazdu
uczestnictwo = []
for id_rozgrywki, (id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi) in enumerate(rozgrywki):
    # trzeba wiedzieć czy będzie pojazd czy nie będzie pojazdu:
    rozgrywka = rozgrywki[id_rozgrywki]
    id_konkurencji = rozgrywka[1] # to 1 może się zmienić
    konkurencja = konkurencje[id_konkurencji]
    id_kategorii = konkurencja[1] # to też
    kategoria = kategorie[id_kategorii]
    if kategoria == "formuła Ch":
        id_pojazdu = random.randrange(0, len(pojazdy)) # UWAGA: TOTALNIE BEZ SENSU - TRZEBA ZASYMULOWAĆ WŁASNOŚĆ POJAZDÓW (ale na razie działa technicznie, potem się zajmę tym)
    else:
        id_pojazdu = None

    # niech na razie około ćwierć możliwych chomików niech biegnie, potem trzeba to lepiej zrobić
    # chcemy mieć przynajmniej 2 chomiki w wyścigu bo jeden chomik sam ze sobą się nie będzie ścigał
    # najpierw musimy wiedziec jakie chomiki mogą biegnąć
    ok_chomiki = [i for i, (_, _, data_urodzenia, data_zakonczenia_aktywnosci) in enumerate(chomiki)
        if data_zakonczenia <= data_zakonczenia_aktywnosci
        and data_rozpoczecia >= data_urodzenia + 0.5*SEKUNDY_W_ROKU # nie zmuszajmy małych chomików do biegania !!!
    ]
    ile_mamy_chomikow = len(ok_chomiki)
    ile_bierzemy_chomikow = max(2, round(bida_rozklad_normalny(ile_mamy_chomikow*0.125, ile_mamy_chomikow*0.375)))
    jakie_chomiki_bierzemy = random.sample(ok_chomiki, k=ile_bierzemy_chomikow)
    for id_chomika in jakie_chomiki_bierzemy:
        wynik = random.random()
        uczestnictwo.append((id_rozgrywki, id_chomika, wynik, id_pojazdu))


# sponsorzy (20)
# - nazwa firmy: na razie "Firma i"
# - oferta: na razie "nic"
# - dane kontaktowe: numer telefonu
# - rozpoczęcie współpracy: od 2021 do 2025
# - zakończenie współpracy: od rozpoczęcia do 2025 albo wcale
sponsorzy = []
for i in range(20):
    nazwa_firmy = f"Firma {i}"
    oferta = "nic"
    dane_kontaktowe = random.randint(100000000, 999999999)
    rozpoczecie_wspolpracy = random.randrange(1514761200, 1735686000)
    if random.random() < 0.1: # 10% szans że już nie ma
        zakonczenie_wspolpracy = random.randrange(rozpoczecie_wspolpracy, 1735686000)
    else:
        zakonczenie_wspolpracy = None
    sponsorzy.append((nazwa_firmy, oferta, dane_kontaktowe, rozpoczecie_wspolpracy, zakonczenie_wspolpracy))

# TYPY ŹRÓDEŁ FINANSOWANIA - na razie nie

# finansowanie - dla każdych zawodów od 1 do 3 sponsorów
# - id_zawodow
# - id_firmy, lub null
# - data wpłaty - w przeciągu 60 dni przed zawodami
# - kwota - od 10000 do 100000
finansowanie = []
for id_zawodow, (data_rozpoczecia, data_zakonczenia, liczba_widzow, koordynator) in enumerate(zawody):
    liczba_finansowan = random.randint(1, 3)
    jakie_firmy = random.sample(sponsorzy + [None], k=liczba_finansowan)
    for id_firmy in jakie_firmy:
        data_wplaty = random.randrange(data_rozpoczecia - 60*SEKUNDY_W_DNIU, data_rozpoczecia)
        kwota = random.randint(10000, 100000)
        finansowanie.append((id_zawodow, id_firmy, data_wplaty, kwota))

# koszty zawodów - od 5 do 10 dla każdych zawodów
# - id_zawodow
# - nazwa kosztu - "Koszt" (Czy tabela rodzaje kosztów?) ---
# - kwota - od 100 do 10000 złotych (rozkład wykładniczy)
koszty_zawodow = []
for id_zawodow, (data_rozpoczecia, data_zakonczenia, liczba_widzow, koordynator) in enumerate(zawody):
    ile_kosztow = random.randint(5, 10)
    for _ in range(ile_kosztow):
        nazwa_kosztu = "Koszt"
        kwota = 10**random.uniform(2, 4)
        koszty_zawodow.append((id_zawodow, nazwa_kosztu, kwota))
    

#for i in rozgrywki: # chomiki / zawody / rozgrywki / uczestnictwo, można testować sobie
#    print(i)






#to zostaw na razie
#powinno działać jak wszystkie tabele będą wypełnione ale to się jeszcze potem sprawdzi
"""
tables = [producenci, modele, pojazdy, rasy, wlasciciele, chomiki, substancje, kontrola_substancji, kontrole_antydopingowe, sponsorzy, typy_zrodel_finansowania, stanowiska, pracownicy, zawody, rodzaje_kosztow, koszty_zawodow, finansowanie, rozgrywki, uczestnictwo, przeszkody, podloza, kategorie, konkurencje, konkurencje_przeszkody, wazenie]
databases = ["producenci", "modele", "pojazdy", "rasy", "wlasciciele", "chomiki", "substancje", "kontrola_substancji", "kontrole_antydopingowe", "sponsorzy", "typy_zrodel_finansowania", "stanowiska", "pracownicy", "zawody", "rodzaje_kosztow", "koszty_zawodow", "finansowanie", "rozgrywki", "uczestnictwo", "przeszkody", "podloza", "kategorie", "konkurencje", "konkurencje_przeszkody", "wazenie"]
variables = ["(nazwa_producenta)", "(nazwa_modelu, cena_modelu, id_producenta)", "(nazwa_pojazdu, id_modelu)", "(nazwa_rasy)", "(imie_wlasciciela, nazwisko_wlasciciela, numer_telefonu)", "(imie_chomika, id_wlasciciela, id_rasy, data_urodzenia, data_dolaczenia, data_odejscia)", "(nazwa_substancji)", "(id_kontroli, id_substancji, wynik_testu)", "(id_chomika, id_zawodow, data_kontroli)", "(nazwa_firmy, oferta, dane_kontaktowe, rozpoczecie_wspolpracy, zakonczenie_wspolpracy)", "(nazwa_typu)", "(nazwa_stanowiska, wyplata)", "(imie_pracownika, nazwisko_pracownika, id_stanowiska, data_zatrudnienia, data_zwolnienia, numer_telefonu)", "(data_rozpoczecia, data_zakonczenia, liczba_widzow, id_koordynatora)", "(nazwa_kosztu)", "(id_zawodow, id_kosztu, kwota)", "(id_zawodow, id_typu, id_firmy, data_wplaty, kwota)", "(id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi)", "(id_chomika, id_rozgrywki, czas, miejsce, id_pojazdu)", "(rodzaj_przeszkody)", "(nazwa_podloza)", "(nazwa_kategorii)", "(nazwa_konkurencji, id_kategorii, id_podloza, dlugosc_trasy)", "(id_konkurencji, id_przeszkody)", "(id_chomika, id_zawodow, waga, data_wazenia)"]
lenghts = [1, 3, 2, 1, 3, 6, 1, 3, 3, 5, 1, 2, 6, 4, 1, 3, 5, 4, 5, 1, 1, 1, 4, 2, 4]
def fill(table, database, variable, lenght):
    sql = "INSERT INTO " + database + " " + variable + " VALUES (%s" + ", %s" * (lenght - 1) + ")"
    mycursor.executemany(sql, table)

for i in range(len(tables)):
    fill(tables[i], databases[i], variables[i], lenghts[i])


"""


# mycursor.close()
# con.close()