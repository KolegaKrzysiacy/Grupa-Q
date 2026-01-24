import random
from faker import Faker         #pip install faker w gitbash # Jest coś takiego jak requirements.txt ale nwm czy to zadziała tutaj
from datetime import datetime
# import mysql.connector

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
fake = Faker("pl_PL") #imiona i nazwiska
NAZWY_FIRM = [f"Firma {i}" for i in range(20)] # tyle ile nazw tyle firm
ZODIAKI = ["Baran", "Byk", "Bliźnięta", "Rak", "Lew", "Panna", "Waga", "Skorpion", "Strzelec", "Koziorożec", "Wodnik", "Ryby"]
#MIEJSCA = ["Warszawa","Kraków","Gdańsk","Wrocław","Poznań","Katowice","Łódź","Szczecin","Bydgoszcz","Lublin"] maybe idk

# rasy
rasy = ["Syryjski", "Dżungarski", "Roborowskiego"]
# przeszkody, podłoża, kategorie
kategorie = ["naturalna", "formuła Ch"]
przeszkody = ["Labirynt", "Rury", "Klocki", "Podesty", "Ścianki"]
podloza = ["Trociny", "Trawa", "Ziemia", "Piasek", "Woda"]
producenci = ["Producent monopolista"]
zakazane_substancje = ["mikstura siły", "mikstura szybkości", "mikstura wysokiego skoku", "mikstura niewidzialności", "mikstura widzenia w ciemności"]
typy_zrodel_finansowania = ["pls", "cos", "wymysl"]
rodzaje_kosztow = ["pls", "tu", "tez"]
#noete tabele bo jakbym zmienił stare to w innych tabelech co biorą info z tych tak by wyszło ('Stefan', ('Dżungarski',), 1536180195, 1565454281, 1623834960)
rasy_table = to_tuples(rasy)
kategorie_table = to_tuples(kategorie)
przeszkody_table = to_tuples(przeszkody)
podloza_table = to_tuples(podloza)
producenci_table = to_tuples(producenci)

modele_producenci_pom = {
    "Producent monopolista": ["Model Model", "ROZKURWIACZ 5000"]
}
modele_producenci = list(modele_producenci_pom.values())
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
    nr_tel = random.randint(100000000, 999999999) #sprawdzić czy przypadkiem nie powtarzają się <<< Mało szans jest że się powtórzą XD. hazard.
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
        imie = fake.first_name_male() # Znalazłem stronke co ma dosyć dużo imion dla chomikóœ https://bloggerchomik.blogspot.com/2013/04/imiona-dla-chomikow.html
    else:
        imie = fake.first_name_female()
    id_rasa = random.choice(range(1, len(rasy)+1)) # rasa -> id_rasy
    data_urodzenia = random.randrange(1514761200, 1735686000)
    data_dolaczenia = int(data_urodzenia + random.uniform(0.5, 1)*SEKUNDY_W_ROKU)
    czas_kariery = int(bida_rozklad_normalny(1, 2.5)*SEKUNDY_W_ROKU)
    data_zakonczenia_aktywnosci = data_dolaczenia + czas_kariery
    id_wlasciciela = random.randrange(len(wlasciciele)) # Można by zrobić żeby była większa wariancja ilości chomików
    chomiki.append((imie, id_wlasciciela, id_rasa, data_urodzenia, data_dolaczenia, data_zakonczenia_aktywnosci))

# pomocniczy słownik
id_stanowisk = {}
for i, (stanowisko, _) in enumerate(stanowiska):
    id_stanowisk[stanowisko] = i

# pracownicy
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
# - liczba widzow: od 100 do 1000 jednostajny RAZY ROK-2020 żeby był coraz bardziej popularny
# - id_koordynatora
zawody = [] # ! zawody nie będą po kolei + zawody mogą się pokrywać
for _ in range(50):
    data_rozpoczecia = random.randrange(1514761200, 1735686000)
    czas_trwania = random.randint(3, 7)
    data_zakonczenia = data_rozpoczecia + czas_trwania*SEKUNDY_W_DNIU
    liczba_widzow = random.randint(100, 1000) * (data_rozpoczecia / SEKUNDY_W_ROKU - 50) # 2020-1970=50
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

# modele pojazdów (10)
# - producent
# - nazwa modelu: "Model i" 
# - cena modelu: od 10 do 100zł
modele = []
for i in range(10):
    id_producenta = random.randint(1, len(producenci))
    nazwa_modelu = random.choice(modele_producenci[id_producenta-1])
    cena_modelu = random.randint(10, 100)
    modele.append((id_producenta, nazwa_modelu, cena_modelu))

# pojazdy (od 1*liczba właścicieli do 3*liczba właścicieli)
# - id_modelu: losowy
pojazdy = []
liczba_pojazdow = random.randrange(100*len(wlasciciele), 300*len(wlasciciele))
for i in range(liczba_pojazdow):
    id_modelu = random.randrange(1, len(modele)+1)
    pojazdy.append((id_modelu,))

#for x in chomiki: print(int(1970+x[3]/60/60/24//365), int(x[3]/60/60/24%365 //31), int(x[3]/60/60/24%365 %31)) #mniej więcej daty

pom_do_wazenia = {chomik: set() for chomik in range(1, len(chomiki)+1)} # jaki chomik brał udział w jakich zawodach

# uczestnictwo (i wyniki) - dla każdej rozgrywki w każdych zawodach
# jak chomik jest w tabeli to uczestniczył a jak nie jest to nie uczestniczył
# - id_rozgrywki
# - id_chomika
# - wynik - jak na razie nie mamy typów rozgrywek ani nic więc liczby od 0 do 1 (Trzeba zrobić czas i miejsce z tego)
# - id_pojazdu
# przy okazji testy antydopingowe
uczestnictwo = []
kontrole_antydopingowe = []
kontrola_substancji = []
for id_rozgrywki, (id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi) in enumerate(rozgrywki):
    # trzeba wiedzieć czy będzie pojazd czy nie będzie pojazdu:
    rozgrywka = rozgrywki[id_rozgrywki]
    id_konkurencji = rozgrywka[1] # to 1 może się zmienić
    konkurencja = konkurencje[id_konkurencji - 1] #przez to że wcześniej zmieniłem bo auto inc to trzeba -1 bo nie działa
    id_kategorii = konkurencja[0] # to też --- z 1 na 0 bo brało id_podloza i było list index out of range
    kategoria = kategorie[id_kategorii - 1] #przez to że wcześniej zmieniłem bo auto inc to trzeba -1 bo nie działa
    if kategoria == "formuła Ch":
        id_pojazdu = pojazdy.pop() # Może sie wyjebać, wtedy trzeba zrobić więcej pojazdów
    else:
        id_pojazdu = None

    # niech na razie około ćwierć możliwych chomików niech biegnie, potem trzeba to lepiej zrobić    #
    # chcemy mieć przynajmniej 2 chomiki w wyścigu bo jeden chomik sam ze sobą się nie będzie ścigał # Komentarze pisane dawno ale dalej aktualne - 
    # najpierw musimy wiedziec jakie chomiki mogą biegnąć                                            # - na razie git ale potem sie to lepiej zrobi
    ok_chomiki = [i for i, (_, _, _, _, data_dolaczenia, data_zakonczenia_aktywnosci) in enumerate(chomiki)
        if data_rozgrywki <= data_zakonczenia_aktywnosci
        and data_rozpoczecia >= data_dolaczenia
    ]
    ile_mamy_chomikow = len(ok_chomiki)
    ile_bierzemy_chomikow = max(2, round(bida_rozklad_normalny(ile_mamy_chomikow*0.125, ile_mamy_chomikow*0.375))) # to chyba cały czas tylko = 2 <<< Trzeba więcej chomików zrobić
    #jakie_chomiki_bierzemy = random.sample(ok_chomiki, k=ile_bierzemy_chomikow) #raise ValueError("Sample larger than population or is negative") -- ok.chomiki są puste, pewnie przez to że daty nie pasują i nic nie wchodzi do nich
    jakie_chomiki_bierzemy = random.sample(chomiki, k=ile_bierzemy_chomikow) #tymczasowe żeby było do tabeli
    id_chomika = random.sample(range(1,len(chomiki)+1), k=ile_bierzemy_chomikow)
    for i in range(len(jakie_chomiki_bierzemy)): 
        pom_do_wazenia[id_chomika[i]].add(id_zawodow)
        # testy antydopingowe
        if random.random() < 0.05:
            kontrole_antydopingowe.append((id_chomika[i], data_rozgrywki))
            id_kontroli = len(kontrole_antydopingowe)
            for id_substancji in range(1, len(zakazane_substancje)):
                kontrola_substancji.append((id_kontroli, id_substancji, 0)) # Robimy że chomiki nie używają dopingu i chuj
        uczestnictwo.append((id_chomika[i], id_rozgrywki + 1)) # zmienna wynik usunięty <<< Czemu?

# ważenie
# - id chomika
# - id zawodów
# - waga
wazenie = []
for id_chomika, idy_zawodow in pom_do_wazenia.items():
    przedzialy_wag = {'Syryjski': (85, 150), 'Dżungarski': (30, 55), 'Roborowskiego': (20, 30)}
    przedzial_wagi = przedzialy_wag[rasy[chomiki[id_chomika-1][2]-1]] # może sie zmienić to 2!
    bazowa_waga = bida_rozklad_normalny(*przedzial_wagi)
    # Można by posortować datami zawodów żeby to miało jakiś sens ale komu by sie chciało, wyjebane
    for id_zawodow in idy_zawodow:
        wazenie.append((id_chomika, id_zawodow, bazowa_waga*bida_rozklad_normalny(0.95, 1.05)))

# TEŻ NIEDOKOŃCZONE

# sponsorzy (tyle ile nazw firm)
# - nazwa firmy
# - dane kontaktowe: numer telefonu
# - rozpoczęcie współpracy: od 2021 do 2025
# - zakończenie współpracy: od rozpoczęcia do 2025 albo wcale
sponsorzy = []
for i in range(len(NAZWY_FIRM)):
    nazwa_firmy = NAZWY_FIRM[i]
    dane_kontaktowe = random.randint(100000000, 999999999)
    rozpoczecie_wspolpracy = random.randrange(1514761200, 1735686000)
    if random.random() < 0.1: # 10% szans że już nie ma
        zakonczenie_wspolpracy = random.randrange(rozpoczecie_wspolpracy, 1735686000)
    else:
        zakonczenie_wspolpracy = None
    sponsorzy.append((nazwa_firmy, dane_kontaktowe, rozpoczecie_wspolpracy, zakonczenie_wspolpracy))

# finansowanie - dla każdych zawodów od 1 do 3 sponsorów
# - id_zawodow
# - id typu finansowania
# - id_firmy, lub null
# - data wpłaty - w przeciągu 60 dni przed zawodami
# - kwota - od 10000 do 100000
finansowanie = []
for id_zawodow, (data_rozpoczecia, data_zakonczenia, liczba_widzow, koordynator) in enumerate(zawody):
    liczba_finansowan = random.randint(1, 3)
    jakie_firmy = random.sample(list(range(1, len(sponsorzy)+1)) + [None], k=liczba_finansowan)
    for id_firmy in jakie_firmy:
        id_typu_finansowania = random.randint(1, len(typy_zrodel_finansowania))
        data_wplaty = random.randrange(data_rozpoczecia - 60*SEKUNDY_W_DNIU, data_rozpoczecia)
        kwota = random.randint(10000, 100000)
        finansowanie.append((id_zawodow+1, id_typu_finansowania, id_firmy, data_wplaty, kwota))

# koszty zawodów - od 5 do 10 dla każdych zawodów
# - id_zawodow
# - id typu kosztu
# - kwota - od 100 do 10000 złotych (rozkład wykładniczy)
koszty_zawodow = []
for id_zawodow, (data_rozpoczecia, data_zakonczenia, liczba_widzow, koordynator) in enumerate(zawody):
    ile_kosztow = random.randint(5, 10)
    for _ in range(ile_kosztow):
        id_typu_kosztu = random.randint(1, len(rodzaje_kosztow))
        kwota = 10**random.uniform(2, 4)
        koszty_zawodow.append((id_zawodow+1, id_typu_kosztu, kwota))
    

# for i in rozgrywki: # chomiki / zawody / rozgrywki / uczestnictwo, można testować sobie
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