import random
from faker import Faker         #pip install faker w gitbash
from datetime import datetime
import mysql.connector

"""
con = mysql.connector.connect(
   host="localhost",
   user="admin",
   password="admin",
   database="grupaq"
 )

mycursor = con.cursor()

#resetuje baze danych i czyści auto increment, żeby zaczynało się od 1, bo inaczej jak się generuje FK z range() kod się wysypuję
databases = ["producenci", "modele", "pojazdy", "czas_pojazdy", "rasy", "wlasciciele", "chomiki", "substancje", "kontrole_antydopingowe", "kontrola_substancji", "sponsorzy", "typy_zrodel_finansowania", "stanowiska", "pracownicy", "zatrudnienie", "zawody", "rodzaje_kosztow", "koszty_zawodow", "finansowanie", "kategorie", "podloza", "przeszkody", "konkurencje", "konkurencje_przeszkody", "rozgrywki", "uczestnictwo", "wazenie"]
mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
for x in databases:
    mycursor.execute(f"TRUNCATE TABLE {x}")
mycursor.execute("SET FOREIGN_KEY_CHECKS=1")
con.commit()
"""

# na razie nie ma:
# - testów antydopingowych i substancji
# - ważenia
# - pojazdy własność
# - sponsorowanie typy finansowań


random.seed(42)

DNI_W_ROKU = 365.2425
SEKUNDY_W_DNIU = 86400
SEKUNDY_W_ROKU = DNI_W_ROKU*SEKUNDY_W_DNIU


def to_tuples(lst):
    return [(x,) for x in lst] #jak są tabele z tylko jednym wierszem nie licząc PK, to np ["Producent monopolista"] bierze jako str, [("Producent monopolista")], to też, dopiero [("Producent monopolista",)] działa

def to_date(lst, n):
    return [x[:n] + (datetime.fromtimestamp(x[n]).date(),) + x[n+1:] for x in lst]

def to_timestamp(lst, n):
    return [x[:n] + (datetime.fromtimestamp(x[n]),) + x[n+1:] for x in lst]
# TUTAJ LISTY TRZEBA ZROBIĆ PRAWIDZIWE
fake = Faker("pl_PL") #imiona i nazwiska
NAZWY_FIRM = [f"Firma {i}" for i in range(20)] # tyle ile nazw tyle firm
ZODIAKI = ["Baran", "Byk", "Bliźnięta", "Rak", "Lew", "Panna", "Waga", "Skorpion", "Strzelec", "Koziorożec", "Wodnik", "Ryby"] # Tutaj nazwy znaków zodiaku
#MIEJSCA = ["Warszawa","Kraków","Gdańsk","Wrocław","Poznań","Katowice","Łódź","Szczecin","Bydgoszcz","Lublin"] maybe idk

# rasy
rasy = ["Syryjski", "Dżungarski", "Roborowskiego"]
# przeszkody, podłoża, kategorie
kategorie = ["naturalna", "formuła Ch"]
przeszkody = ["Labirynt", "Rury", "Klocki", "Podesty", "Ścianki"]
podloza = ["Trociny", "Trawa", "Ziemia", "Piasek", "Woda"]
producenci = ["Producent monopolista"]
#noete tabele bo jakbym zmienił stare to w innych tabelech co biorą info z tych tak by wyszło ('Stefan', ('Dżungarski',), 1536180195, 1565454281, 1623834960)
rasy_table = to_tuples(rasy)
kategorie_table = to_tuples(kategorie)
przeszkody_table = to_tuples(przeszkody)
podloza_table = to_tuples(podloza)
producenci_table = to_tuples(producenci)

modele = {
    "Producent monopolista": ["Model Model", "ROZKURWIACZ 5000"] #to musi być normalną listą jak reszta
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
    if random.choice([True, False]):
        imie = fake.first_name_male()
        nazwisko = fake.last_name_male()
    else:
        imie = fake.first_name_female()
        nazwisko = fake.last_name_female()
    nr_tel = random.randint(100000000, 999999999) #sprawdzić czy przypadkiem nie powtarzają się --- można zrobić random.sample
    zodiak = random.choice(ZODIAKI)                            #zodiak = random.choice ???
    wlasciciele.append((imie, nazwisko, nr_tel, zodiak))
# robimy tyle ile imion chomików:
# - imie
# - rasa
# - data urodzenia: od 2018 do 2024 (rozkład jednostajny)
# - data_dolaczenia: w wieku 0.5-1 lat (rozkład jednostajny)
# - data zakończenia aktywności: data urodzenia plus od 1.5 do 3 lat (bida rozkład normalny)
chomiki = []
for i in range(100):
    if random.choice([True, False]):
        imie = fake.first_name_male()
    else:
        imie = fake.first_name_female()
    id_rasa = random.choice(range(1, len(rasy)+1)) # rasa -> id_rasy
    data_urodzenia = random.randrange(1514761200, 1735686000)
    data_dolaczenia = int(data_urodzenia + random.uniform(0.5, 1)*SEKUNDY_W_ROKU)
    czas_kariery = int(bida_rozklad_normalny(1, 2.5)*SEKUNDY_W_ROKU)
    data_zakonczenia_aktywnosci = data_dolaczenia + czas_kariery
    id_wlasciciela = 1
    chomiki.append((imie,id_wlasciciela, id_rasa, data_urodzenia, data_dolaczenia, data_zakonczenia_aktywnosci)) #trzeba dodać id_właściciela

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
pracownicy_temp = []
chcemy_pracownikow = ["Koordynator zawodów"]*5 + ["Sędzia"]*8 + ["Sprzątacz"]*15
for stanowisko in chcemy_pracownikow:
    if random.choice([True, False]):  #nwm czy tu nie trzeba brać już imion co istnieją pracownicy czy o co tu chodzi, chyba albo imiona z pracowników zależą od tych albo na odwrót idk
        imie = fake.first_name_male()
        nazwisko = fake.last_name_male()
    else:
        imie = fake.first_name_female()
        nazwisko = fake.last_name_female()
    id_stanowiska = id_stanowisk[stanowisko]
    nr_tel = random.randint(100000000, 999999999)
    data_zatrudnienia = random.randrange(1514761200, 1735686000)
    if random.random() < 0.1: # 10% szans że już nie ma
        data_zwolnienia = random.randrange(data_zatrudnienia, 1735686000)
    else:
        data_zwolnienia = None
    pracownicy.append((imie, nazwisko, id_stanowiska, data_zatrudnienia, data_zwolnienia, nr_tel)) #niektóre rzeczy trzeba przeniesć do innej tabeli
    pracownicy_temp.append((imie, nazwisko, nr_tel))# tylko do tabeli tymczasowe


# pomocniczy słownik
osoby_na_stanowisku = {stanowisko: 
                       [i + 1 for i, (_, _, id_stanowiska, _, _, _) in enumerate(pracownicy) if id_stanowiska == id_stanowisk[stanowisko]]  #WAŻNE auto incerement zaczyna od 1 czyli id 0 nie istnieje
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
for i in range(20):
    liczba_przeszkod = random.randint(2, 5)
    temp = random.sample(range(1, len(przeszkody) + 1), k=liczba_przeszkod)
    temp.sort()
    for j in range(liczba_przeszkod):
        konkurencje_przeszkody.append((i + 1, temp[j])) #wypełniało konkurencje_przeszkody nazwami a nie id i źle w ogóle, to są 2 FK i PK i obydwa trzeba wygenerować
# konkurencje - 20 konkurencji losowych
# - nazwa konkurencji
# - id kategorii
# - id podloza
# - id przeszkod - odpowiednie id w konkurenje_przeszkody
# - długość trasy - od 10 do 100 metrów
konkurencje = []
for i in range(20):
    id_kategorii = random.randrange(1, len(kategorie) + 1) #znowu auto inc jest od 1
    id_podloza = random.randrange(1, len(podloza) + 1) #też
    # przeszkody
    #id_przeszkod = i  to do osobnej, jakoś rand id_konkurencji i id_przeszkody w konkurenje_przeszkody
    dlugosc_trasy = random.randint(10, 100)
    konkurencje.append((id_kategorii, id_podloza, dlugosc_trasy))

# generujemy rozgrywki dla każdych zawodów - od 10 do 50 na dzień dla każdych zawodów (rozkład normalny): # tam było że w poprzedmnim roku 
# - id zawodów
# - id konkurencji
# - data rozgrywki - po kolei dni
# - id sedzi
rozgrywki = []
for id_zawodow, (data_rozpoczecia, data_zakonczenia, liczba_widzow, koordynator) in enumerate(zawody): # w additional.py mas ztworzony UNIQUE (id_zawodow, id_konkurencji) --- ale w sumie lepiej wyjebać tamto, tu będzie więcej w tabeli a tam ten plik już niepotrzebny będzie
    czas_trwania = round((data_zakonczenia - data_rozpoczecia)/SEKUNDY_W_DNIU)
    for dzien in range(czas_trwania):
        liczba_rozgrywek = round(bida_rozklad_normalny(10, 50))
        data_rozgrywki = data_rozpoczecia + dzien*SEKUNDY_W_DNIU
        for _ in range(liczba_rozgrywek):
            id_konkurencji = random.randrange(0, len(konkurencje))
            id_sedzi = random.choice(osoby_na_stanowisku["Sędzia"])
            rozgrywki.append((id_zawodow + 1, id_konkurencji + 1, data_rozgrywki, id_sedzi)) 

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
# # - nazwa pojazdu: "Pojazd i" #w sumie nie ma sensu chyba dawać im nazw jak mają nazwe modelu
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

#for x in chomiki: print(int(1970+x[3]/60/60/24//365), int(x[3]/60/60/24%365 //31), int(x[3]/60/60/24%365 %31)) #mniej więcej daty

uczestnictwo = []
for id_rozgrywki, (id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi) in enumerate(rozgrywki):
    # trzeba wiedzieć czy będzie pojazd czy nie będzie pojazdu:
    rozgrywka = rozgrywki[id_rozgrywki]
    id_konkurencji = rozgrywka[1] # to 1 może się zmienić
    konkurencja = konkurencje[id_konkurencji - 1] #przez to że wcześniej zmieniłem bo auto inc to trzeba -1 bo nie działa
    id_kategorii = konkurencja[0] # to też --- z 1 na 0 bo brało id_podloza i było list index out of range
    kategoria = kategorie[id_kategorii - 1] #przez to że wcześniej zmieniłem bo auto inc to trzeba -1 bo nie działa
    if kategoria == "formuła Ch":
        id_pojazdu = 0 # NA RAZIE WSZYSCY JEŻDŻĄ TYM SAMYM NIEISTNIEJĄCYM POJAZDEM PÓKI NIE MA ZROBIONYCH !!! --- to gdzie indziej przenieść
    else:
        id_pojazdu = None

    # niech na razie około ćwierć możliwych chomików niech biegnie, potem trzeba to lepiej zrobić    #
    # chcemy mieć przynajmniej 2 chomiki w wyścigu bo jeden chomik sam ze sobą się nie będzie ścigał # Komentarze pisane dawno ale dalej aktualne - 
    # najpierw musimy wiedziec jakie chomiki mogą biegnąć                                            # - na razie git ale potem sie to lepiej zrobi
    ok_chomiki = [i for i, (_, _, _, _, data_dolaczenia, data_zakonczenia_aktywnosci) in enumerate(chomiki)
        if data_zakonczenia <= data_zakonczenia_aktywnosci
        and data_rozpoczecia >= data_dolaczenia
    ]
    ile_mamy_chomikow = len(ok_chomiki)
    ile_bierzemy_chomikow = max(2, round(bida_rozklad_normalny(ile_mamy_chomikow*0.125, ile_mamy_chomikow*0.375)))  # to chyba cały czas tylko = 2
    #jakie_chomiki_bierzemy = random.sample(ok_chomiki, k=ile_bierzemy_chomikow) #raise ValueError("Sample larger than population or is negative") -- ok.chomiki są puste, pewnie przez to że daty nie pasują i nic nie wchodzi do nich
    jakie_chomiki_bierzemy = random.sample(chomiki, k=ile_bierzemy_chomikow) #tymczasowe żeby było do tabeli
    id_chomika = random.sample(range(1,101), k=ile_bierzemy_chomikow)
    for i in range(len(jakie_chomiki_bierzemy)): 
        uczestnictwo.append((id_chomika[i], id_rozgrywki + 1)) # zmienna wynik usunięty --- id_pojazdu już nie tu --- +1 bo auto increment i tu id_chomika było całą krotką z danymi danego chomika 


# TEŻ NIEDOKOŃCZONE

# # sponsorzy (tyle ile nazw firm)
# # - nazwa firmy
# # - oferta: na razie "nic" --- i nic raczej nie będzie
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



""" #wszystkie
tables = [producenci_table, modele, pojazdy, czas_pojazdy, rasy_table, wlasciciele, chomiki, substancje, kontrole_antydopingowe, kontrola_substancji, sponsorzy, typy_zrodel_finansowania, stanowiska, pracownicy, zatrudnienie, zawody, rodzaje_kosztow, koszty_zawodow, finansowanie, kategorie_table, podloza_table, przeszkody_table, konkurencje, konkurencje_przeszkody, rozgrywki, uczestnictwo, wazenie]
databases = ["producenci", "modele", "pojazdy", "czas_pojazdy", "rasy", "wlasciciele", "chomiki", "substancje", "kontrole_antydopingowe", "kontrola_substancji", "sponsorzy", "typy_zrodel_finansowania", "stanowiska", "pracownicy", "zatrudnienie", "zawody", "rodzaje_kosztow", "koszty_zawodow", "finansowanie", "kategorie", "podloza", "przeszkody", "konkurencje", "konkurencje_przeszkody", "rozgrywki", "uczestnictwo", "wazenie"]
variables = ["(nazwa_producenta)", "(nazwa_modelu, cena_modelu, id_producenta)", "(id_modelu)", "(id_pojazdu, id_chomika, poczatek_uzywania, koniec_uzywania)", "(nazwa_rasy)", "(imie_wlasciciela, nazwisko_wlasciciela, numer_telefonu, zodiak_wlasciciela)", "(imie_chomika, id_wlasciciela, id_rasy, data_urodzenia, data_dolaczenia, data_odejscia)", "(nazwa_substancji)", "(id_chomika, data_kontroli)", "(id_kontroli, id_substancji, wynik_testu)", "(nazwa_firmy, dane_kontaktowe, rozpoczecie_wspolpracy, zakonczenie_wspolpracy)", "(nazwa_typu)", "(nazwa_stanowiska, wyplata)", "(imie_pracownika, nazwisko_pracownika, numer_telefonu)", "(id_stanowiska, id_pracownika, data_zatrudnienia, data_zwolnienia)", "(data_rozpoczecia, data_zakonczenia, liczba_widzow, id_koordynatora)", "(nazwa_kosztu)", "(id_zawodow, id_kosztu, kwota)", "(id_zawodow, id_typu, id_firmy, data_wplaty, kwota)", "(nazwa_kategorii)", "(nazwa_podloza)", "(rodzaj_przeszkody)", "(id_kategorii, id_podloza, dlugosc_trasy)", "(id_konkurencji, id_przeszkody)", "(id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi)", "(id_chomika, id_rozgrywki)", "(id_chomika, id_zawodow, waga, data_wazenia)"]
time_defs=[(0,),(0,0,0),(0,),(0,0,1,1),(0,),(0,0,0,0),(0,0,0,1,1,1),(0,),(0,2),(0,0,0),(0,0,1,1),(0,),(0,0),(0,0,0),(0,0,1,1),(2,2,0,0),(0,),(0,0,0),(0,0,0,2,0),(0,),(0,),(0,),(0,0,0),(0,0),(0,0,2,0),(0,0,0),(0,0,0,2)]




#na razie te co mają dane
tables = [producenci_table, rasy_table, wlasciciele, chomiki, stanowiska, pracownicy_temp, zawody, kategorie_table, podloza_table, przeszkody_table, konkurencje, konkurencje_przeszkody, rozgrywki, uczestnictwo]
databases = ["producenci", "rasy", "wlasciciele", "chomiki", "stanowiska", "pracownicy", "zawody", "kategorie", "podloza", "przeszkody", "konkurencje", "konkurencje_przeszkody", "rozgrywki", "uczestnictwo"]
variables = ["(nazwa_producenta)", "(nazwa_rasy)", "(imie_wlasciciela, nazwisko_wlasciciela, numer_telefonu, zodiak_wlasciciela)", "(imie_chomika, id_wlasciciela, id_rasy, data_urodzenia, data_dolaczenia, data_odejscia)", "(nazwa_stanowiska, wyplata)", "(imie_pracownika, nazwisko_pracownika, numer_telefonu)", "(data_rozpoczecia, data_zakonczenia, liczba_widzow, id_koordynatora)", "(nazwa_kategorii)", "(nazwa_podloza)", "(rodzaj_przeszkody)", "(id_kategorii, id_podloza, dlugosc_trasy)", "(id_konkurencji, id_przeszkody)", "(id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi)", "(id_chomika, id_rozgrywki)"]
time_defs=[(0,),(0,),(0,0,0,0),(0,0,0,1,1,1),(0,0),(0,0,0),(2,2,0,0),(0,),(0,),(0,),(0,0,0),(0,0),(0,0,2,0),(0,0)]



def convert_value(value, mode):
    if mode == 1:
        return datetime.fromtimestamp(value).date()
    if mode == 2:
        return datetime.fromtimestamp(value)
    return value 

def convert_table(table, time_def):
    new_table = []
    for row in table:
        new_row = tuple(convert_value(val, mode) for val, mode in zip(row, time_def))
        new_table.append(new_row)
    return new_table

def fill(table, database, variable, time_def):
    if not table: return
    table = convert_table(table, time_def)

    placeholders = ", ".join(["%s"] * len(table[0]))
    sql = f"INSERT INTO {database} {variable} VALUES ({placeholders})"
    print(sql)
    mycursor.executemany(sql, table)

for i in range(len(tables)):
    fill(tables[i], databases[i], variables[i], time_defs[i])


con.commit()
mycursor.close()
con.close()

"""