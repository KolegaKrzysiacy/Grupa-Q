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
# - pojazdy własność
# - sponsorowanie typy finansowań


random.seed(42)

DNI_W_ROKU = 365.2425
SEKUNDY_W_DNIU = 86400
SEKUNDY_W_ROKU = DNI_W_ROKU*SEKUNDY_W_DNIU

# TUTAJ LISTY TRZEBA ZROBIĆ PRAWIDZIWE
IMIONA = ["Adam", "Bartek", "Paweł", "Janusz"]
NAZWISKA = ["Nowak", "Kowalski", "Mikke"]
IMIONA_CHOMIKOW = [f"Chomik {i}" for i in range(100)] # tyle ile imion tyle chomików
NAZWY_FIRM = [f"Firma {i}" for i in range(20)] # tyle ile nazw tyle firm
ZODIAKI = range(12) # Tutaj nazwy znaków zodiaku
# rasy
rasy = ["Syryjski", "Dżungarski", "Roborowskiego"]
# przeszkody, podłoża, kategorie
kategorie = ["naturalna", "formuła Ch"]
przeszkody = ["Labirynt", "Rury", "Klocki", "Podesty", "Ścianki"]
podloza = ["Trociny", "Trawa", "Ziemia", "Piasek", "Woda"]
producenci = ["Producent monopolista"]
modele = {
    "Producent monopolista": ["Model Model", "ROZKURWIACZ 5000"]
}
# stanowiska pracownikow
stanowiska = [("Koordynator zawodów", 6100), ("Sędzia", 5900), ("Sprzątacz", 4900)]


def bida_rozklad_normalny(a, b): # tak sie serio robi ponoć (https://en.wikipedia.org/wiki/Irwin–Hall_distribution)
    return (random.uniform(a, b)+random.uniform(a, b)+random.uniform(a, b))/3

# 20 właścicieli chomików
# - imie
# - nazwisko
# - numer telefonu
# - znak zodiaku (Na razie cyfry weź zmień na prawdziwe nazwy pls)
wlasciciele = []
for _ in range(20):
    imie = random.choice(IMIONA)
    nazwisko = random.choice(NAZWISKA)
    nr_tel = random.randint(100000000, 999999999)
    zodiak = random.choice
    wlasciciele.append((imie, nazwisko, nr_tel, zodiak))

# robimy tyle ile imion chomików:
# - imie
# - rasa
# - data urodzenia: od 2018 do 2024 (rozkład jednostajny)
# - data_dolaczenia: w wieku 0.5-1 lat (rozkład jednostajny)
# - data zakończenia aktywności: data urodzenia plus od 1.5 do 3 lat (bida rozkład normalny)
chomiki = []
for i in range(100):
    imie = IMIONA_CHOMIKOW[i]
    rasa = random.choice(rasy)
    data_urodzenia = random.randrange(1514761200, 1735686000)
    data_dolaczenia = int(data_urodzenia + random.uniform(0.5, 1)*SEKUNDY_W_ROKU)
    czas_kariery = int(bida_rozklad_normalny(1, 2.5)*SEKUNDY_W_ROKU)
    data_zakonczenia_aktywnosci = data_dolaczenia + czas_kariery
    chomiki.append((imie, rasa, data_urodzenia, data_dolaczenia, data_zakonczenia_aktywnosci))

# pomocniczy słownik
id_stanowisk = {}
for i, (stanowisko, _) in enumerate(stanowiska):
    id_stanowisk[stanowisko] = i

# pracownicy # Raczej nie będziemy robić pracowników zatrudnionych na sumach przedziałów, to że potrzeba do EKNFa nie znaczy że musimy to robić 
# (ale trzeba odrobine przekształcić dane żeby wjebać do tabelek bo jest tak jak po staremu już nie mam czasu zmienić ale to łatwo będzie raczej)
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


# pomocniczy słownik
osoby_na_stanowisku = {stanowisko: 
                       [i for i, (_, _, id_stanowiska, _, _, _) in enumerate(pracownicy) if id_stanowiska == id_stanowisk[stanowisko]] 
                       for stanowisko, _ in stanowiska}
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
    id_koordynatora = random.choice(osoby_na_stanowisku["Koordynator zawodów"])
    zawody.append((data_rozpoczecia, data_zakonczenia, liczba_widzow, id_koordynatora))


# 20 przeszkód
konkurencje_przeszkody = []
for _ in range(20):
    liczba_przeszkod = random.randint(2, 5)
    konkurencje_przeszkody.append(random.sample(przeszkody, k=liczba_przeszkod))

# konkurencje - 20 konkurencji losowych
# - nazwa konkurencji
# - id kategorii
# - id podloza
# - id przeszkod - odpowiednie id w konkurenje_przeszkody
# - długość trasy - od 10 do 100 metrów
konkurencje = []
for i in range(20):
    nazwa_konkurencji = f"Konkurencja {i}" # Do wyjebania chyba nazwa imo
    id_kategorii = random.randrange(0, len(kategorie))
    id_podloza = random.randrange(0, len(podloza))
    # przeszkody
    id_przeszkod = i
    dlugosc_trasy = random.randint(10, 100)
    konkurencje.append((nazwa_konkurencji, id_kategorii, id_podloza, i, dlugosc_trasy))

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
            id_sedzi = random.choice(osoby_na_stanowisku["Sędzia"])
            rozgrywki.append((id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi))


# POJAZDY NIEKOMPLEEEETNEEE

# # modele pojazdów (10)
# # - producent
# # - nazwa modelu: "Model i"
# # - cena modelu: od 100 do 1000zł
# modele = []
# for i in range(10):
#     producent = random.choice(producenci)
#     nazwa_modelu = random.choice(modele[producent])
#     cena_modelu = random.randint(100, 1000)
#     modele.append((producent, nazwa_modelu, cena_modelu))

# # pojazdy (od 1*liczba właścicieli do 3*liczba właścicieli)
# # - nazwa pojazdu: "Pojazd i"
# # - id_modelu: losowy
# pojazdy = []
# liczba_pojazdow = random.randrange(len(wlasciciele))
# for i in range(liczba_pojazdow):
#     nazwa_pojazdu = f"Pojazd {i}"
#     id_modelu = random.randrange(0, len(modele))
#     pojazdy.append((nazwa_pojazdu, id_modelu))

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
        id_pojazdu = 0 # NA RAZIE WSZYSCY JEŻDŻĄ TYM SAMYM NIEISTNIEJĄCYM POJAZDEM PÓKI NIE MA ZROBIONYCH !!!
    else:
        id_pojazdu = None

    # niech na razie około ćwierć możliwych chomików niech biegnie, potem trzeba to lepiej zrobić    #
    # chcemy mieć przynajmniej 2 chomiki w wyścigu bo jeden chomik sam ze sobą się nie będzie ścigał # Komentarze pisane dawno ale dalej aktualne - 
    # najpierw musimy wiedziec jakie chomiki mogą biegnąć                                            # - na razie git ale potem sie to lepiej zrobi
    ok_chomiki = [i for i, (_, _, _, data_dolaczenia, data_zakonczenia_aktywnosci) in enumerate(chomiki)
        if data_zakonczenia <= data_zakonczenia_aktywnosci
        and data_rozpoczecia >= data_dolaczenia
    ]
    ile_mamy_chomikow = len(ok_chomiki)
    ile_bierzemy_chomikow = max(2, round(bida_rozklad_normalny(ile_mamy_chomikow*0.125, ile_mamy_chomikow*0.375)))
    jakie_chomiki_bierzemy = random.sample(ok_chomiki, k=ile_bierzemy_chomikow)
    for id_chomika in jakie_chomiki_bierzemy:
        wynik = random.random()
        uczestnictwo.append((id_rozgrywki, id_chomika, wynik, id_pojazdu))


# TEŻ NIEDOKOŃCZONE

# # sponsorzy (tyle ile nazw firm)
# # - nazwa firmy
# # - oferta: na razie "nic"
# # - dane kontaktowe: numer telefonu
# # - rozpoczęcie współpracy: od 2021 do 2025
# # - zakończenie współpracy: od rozpoczęcia do 2025 albo wcale
# sponsorzy = []
# for i in range(len(NAZWY_FIRM)):
#     nazwa_firmy = NAZWY_FIRM[i]
#     oferta = "nic"
#     dane_kontaktowe = random.randint(100000000, 999999999)
#     rozpoczecie_wspolpracy = random.randrange(1514761200, 1735686000)
#     if random.random() < 0.1: # 10% szans że już nie ma
#         zakonczenie_wspolpracy = random.randrange(rozpoczecie_wspolpracy, 1735686000)
#     else:
#         zakonczenie_wspolpracy = None
#     sponsorzy.append((nazwa_firmy, oferta, dane_kontaktowe, rozpoczecie_wspolpracy, zakonczenie_wspolpracy))

# # TYPY ŹRÓDEŁ FINANSOWANIA - na razie nie

# # finansowanie - dla każdych zawodów od 1 do 3 sponsorów
# # - id_zawodow
# # - id_firmy, lub null
# # - data wpłaty - w przeciągu 60 dni przed zawodami
# # - kwota - od 10000 do 100000
# finansowanie = []
# for id_zawodow, (data_rozpoczecia, data_zakonczenia, liczba_widzow, koordynator) in enumerate(zawody):
#     liczba_finansowan = random.randint(1, 3)
#     jakie_firmy = random.sample(sponsorzy + [None], k=liczba_finansowan)
#     for id_firmy in jakie_firmy:
#         data_wplaty = random.randrange(data_rozpoczecia - 60*SEKUNDY_W_DNIU, data_rozpoczecia)
#         kwota = random.randint(10000, 100000)
#         finansowanie.append((id_zawodow, id_firmy, data_wplaty, kwota))

# # koszty zawodów - od 5 do 10 dla każdych zawodów
# # - id_zawodow
# # - nazwa kosztu - "Koszt" (Czy tabela rodzaje kosztów?) ---
# # - kwota - od 100 do 10000 złotych (rozkład wykładniczy)
# koszty_zawodow = []
# for id_zawodow, (data_rozpoczecia, data_zakonczenia, liczba_widzow, koordynator) in enumerate(zawody):
#     ile_kosztow = random.randint(5, 10)
#     for _ in range(ile_kosztow):
#         nazwa_kosztu = "Koszt"
#         kwota = 10**random.uniform(2, 4)
#         koszty_zawodow.append((id_zawodow, nazwa_kosztu, kwota))
    

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