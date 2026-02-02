import random
from datetime import datetime, time, timedelta

import mysql.connector
from faker import Faker

con = mysql.connector.connect(
    host="localhost", user="admin", password="admin", database="grupaq"
)

mycursor = con.cursor()

# resetuje baze danych i czyści auto increment, żeby zaczynało się od 1, bo inaczej jak się generuje FK z range() kod się wysypuję
databases = [
    "producenci",
    "rasy",
    "kategorie",
    "podloza",
    "przeszkody",
    "substancje",
    "typy_zrodel_finansowania",
    "rodzaje_kosztow",
    "stanowiska",
    "sponsorzy",
    "wlasciciele",
    "modele",
    "pracownicy",
    "pojazdy",
    "chomiki",
    "kontrole_antydopingowe",
    "kontrola_substancji",
    "konkurencje",
    "konkurencje_przeszkody",
    "zawody",
    "zatrudnienie",
    "koszty_zawodow",
    "finansowanie",
    "rozgrywki",
    "uczestnictwo",
    "wazenie",
]
mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
for x in databases:
    mycursor.execute(f"TRUNCATE TABLE {x}")
mycursor.execute("SET FOREIGN_KEY_CHECKS=1")
con.commit()

random.seed(123456)  # seed, żeby każdy miał te same dane po generacji
Faker.seed(42)  # tak samo tylko do imion
fake = Faker("pl_PL")  # imiona i nazwiska

# dane do generacji tabel
DNI_W_ROKU = 365.2425
SEKUNDY_W_DNIU = 86400
SEKUNDY_W_ROKU = DNI_W_ROKU * SEKUNDY_W_DNIU
# ta baz danych ma dane do końca 2025
POCZATEK_DZIALANOSCI = 1514761200  # 2018-01-01
KONIEC_DZIALANOSCI = 1767225600  # 2026-01-01

PRODUCENCI = [
    "Speedy Wheels",
    "TurboTech",
    "Nitro Labs",
    "Quantum Motors",
    "HyperDrive",
    "SuperSpeed",
]
MODELE = [
    "Swift X1",
    "Swift Pro",
    "RoadFlash",
    "Speedster",
    "Turbo ZR",
    "Turbo ZR Pro",
    "Boost GT",
    "Overdrive",
    "Nitro GT",
    "Nitro Sprint",
    "Nitro X",
    "Nitro Evo",
    "Quantum S",
    "Quantum One",
    "Quantum Prime",
    "Quantum RS",
    "Hyper V",
    "Hyper Max",
    "Hyper Pulse",
    "Hyper Core",
]  # Każde 5 kolejnych odpowiada jednemu z producentów
RASY = ["Syryjski", "Dżungarski", "Campbella", "Roborowskiego", "Chiński"]
PRZEDZIALY_WAG = [[85, 150], [20, 55], [20, 50], [17, 25], [30, 45]]
KATEGORIE = ["naturalna", "formuła Ch"]
PODLOZA = ["trociny", "trawa", "ziemia", "piasek", "woda"]
DLUGOSCI = [5, 10, 15, 20, 25]
PRZESZKODY = ["labirynt", "rury", "klocki", "podesty", "ścianki"]
SUBSTANCJE = [
    "mikstura siły",
    "mikstura szybkości",
    "mikstura wysokiego skoku",
    "mikstura niewidzialności",
    "mikstura widzenia w ciemności",
]
TYPY_ZRODEL_FINANSOWANIA = [
    "reklamy w przerwach",
    "lokowanie produktu",
    "reklamy na bandach",
    "reklamy na stronie wydarzenia",
    "reklamy na biletach",
    "reklamy na pojazdach",
    "dotacja",
]
RODZAJE_KOSZTOW = [
    "wynajem obiektu",
    "nagrody dla zawodników",
    "obsługa techniczna",
    "opieka weterynaryjna",
    "podłoża",
    "sprzęt",
    "inne",
]
NAZWY_FIRM = [
    "SpeedRun Media",
    "TurboAds",
    "NeonVision",
    "PowerPlay Group",
    "AdStorm",
    "PixelWave",
    "HyperPromo",
    "BrightLine",
    "MediaForge",
    "ClickZone",
    "EventSpark",
    "BrandShift",
    "FastTrack Ads",
    "PromoSphere",
    "VisionBoost",
    "AdPulse",
    "SpotLight Media",
    "MegaReach",
    "FocusPoint",
    "PrimeExposure",
]
ZODIAKI = [
    "Baran",
    "Byk",
    "Bliźnięta",
    "Rak",
    "Lew",
    "Panna",
    "Waga",
    "Skorpion",
    "Strzelec",
    "Koziorożec",
    "Wodnik",
    "Ryby",
]
CHCEMY_PRACOWNIKOW = [1] * 35 + [2] * 28 + [3] * 16  # id stanowisk

FEMALE = [
    "Ada",
    "Alga",
    "Arka",
    "Amfa",
    "Arwena",
    "Aida",
    "Agrafka",
    "Ayla",
    "Ami",
    "Andromeda",
    "Alma",
    "Alka",
    "Ana",
    "Ayah",
    "Anga",
    "Alimka",
    "Anja",
    "Ashlee",
    "Aniela",
    "Adelajda",
    "Ali",
    "Baryłka",
    "Bunia",
    "Bella",
    "Baja",
    "Bambi",
    "Berta",
    "Bianka",
    "Borówka",
    "Buba",
    "Buśka",
    "Buffy",
    "Blanka",
    "Bombelka",
    "Betty",
    "Boba",
    "Bela",
    "Baśka",
    "Bomba",
    "Brenia",
    "Biedronka",
    "Bunny",
    "Bajka",
    "Bloom",
    "Bubi",
    "Bibi",
    "Bijou",
    "Czarna",
    "Czaja",
    "Czarusia",
    "Cytrynka",
    "Chrumcia",
    "Chwila",
    "Cola",
    "Cynia",
    "Corni",
    "Cukierek",
    "Chmurka",
    "Ciapcia",
    "Czakra",
    "Cyrkonia",
    "Chrupcia",
    "Chomka",
    "Chomusia",
    "Czika",
    "Doris",
    "Dudusia",
    "Dragona",
    "Dixi",
    "Didi",
    "Delirka",
    "Dziuba",
    "Daisy",
    "Doty",
    "Doda",
    "Dolly",
    "Dynia",
    "Dafne",
    "Dania",
    "Dercia",
    "Duśka",
    "Dosia",
    "Diana",
    "Dżina",
    "Dresiara",
    "Elza",
    "Elma",
    "Enya",
    "Emma",
    "Estera",
    "Ebola",
    "Emka",
    "Efka",
    "Emi",
    "Echinacea",
    "Erka",
    "Emilia",
    "Eli",
    "Fufcia",
    "Fryga",
    "Fredzia",
    "Frytka",
    "Fifka",
    "Fiona",
    "Frania",
    "Felka",
    "Frela",
    "Fantazja",
    "Fenia",
    "Funia",
    "Fusia",
    "Franczi",
    "Fikuś",
    "Flora",
    "Fauna",
    "Fanta",
    "Gala",
    "Ganja",
    "Gryzia",
    "Glusia",
    "Grypa",
    "Gapa",
    "Grucha",
    "Gucia",
    "Gryzetka",
    "Gaja",
    "Gruba",
    "Gangsterka",
    "Halka",
    "Heidi",
    "Hafka",
    "Holka",
    "Hapka",
    "Hipka",
    "Igiełka",
    "Inia",
    "Inka",
    "Issa",
    "Irma",
    "Ixi",
    "Iluzja",
    "Iga",
    "Ina",
    "Itka",
    "Iwa",
    "Iskierka",
    "Isis",
    "Jaśmina",
    "Jędza",
    "Jadźka",
    "Japka",
    "Julka",
    "Jani",
    "Jerka",
    "Jagoda",
    "Julia",
    "Kokardka",
    "Kinia",
    "Kunia",
    "Kicia",
    "Kusia",
    "Kiki",
    "Kaja",
    "Kitty",
    "Klamka",
    "Kama",
    "Kiara",
    "Kira",
    "Kora",
    "Kredka",
    "Koka",
    "Kropka",
    "Kuczi",
    "Klucha",
    "Kluska",
    "Kruszynka",
    "Kudła",
    "Kika",
    "Kaśka",
    "Kinga",
    "Kate",
    "Klara",
    "Księżniczka",
    "Kundzia",
    "Kornelia",
    "Kordelia",
    "Lisa",
    "Lora",
    "Lizze",
    "Lalusia",
    "Lola",
    "Lizi",
    "Lusia",
    "Lili",
    "Lucky",
    "Luelle",
    "Lana",
    "Lula",
    "Lara",
    "Loona",
    "Lala",
    "Luna",
    "Luśka",
    "Laura",
    "Lubelka",
    "Lisee",
    "Łezka",
    "Łatka",
    "Łajka",
    "Łuna",
    "Łanka",
    "Łupinka",
    "Mysia",
    "Myszka",
    "Milunia",
    "Mini",
    "Misia",
    "Milusia",
    "Minia",
    "Mika",
    "Miłka",
    "Mizia",
    "Mona",
    "Mila",
    "Minako",
    "Micia",
    "Milka",
    "Musia",
    "Maja",
    "Maga",
    "Mysza",
    "Mycha",
    "Madi",
    "Mimi",
    "Mirabella",
    "Meg",
    "Mela",
    "Miga",
    "Mafia",
    "Malina",
    "Mitia",
    "Miśka",
    "Miziołka",
    "Misiunia",
    "Mara",
    "Mimbla",
    "Mozarella",
    "Miżu",
    "Mała",
    "Migotka",
    "Monia",
    "Nitka",
    "Niunia",
    "Niki",
    "Nel",
    "Niosia",
    "Ninuś",
    "Nancy",
    "Nonka",
    "Nastka",
    "Nerka",
    "Norka",
    "Nikita",
    "Nicola",
    "Olivka",
    "Orka",
    "Oda",
    "Ola",
    "Omka",
    "Omega",
    "Ostanka",
    "Opka",
    "Okarka",
    "Oska",
    "Oponka",
    "Prima",
    "Pusia",
    "Pentelka",
    "Pami",
    "Pati",
    "Perelka",
    "Pixi",
    "Poli",
    "Plumcia",
    "Pimpka",
    "Paja",
    "Puchata",
    "Psotka",
    "Pestka",
    "Ptysia",
    "Pucia",
    "Punia",
    "Pandzia",
    "Pulpa",
    "Paris",
    "Pinia",
    "Pysia",
    "Pepsi",
    "Perełka",
    "Rozetka",
    "Roksa",
    "Roborka",
    "Rosa",
    "Renia",
    "Ritka",
    "Rudzia",
    "Ruda",
    "Rutka",
    "Róża",
    "Rodzynka",
    "Roksana",
    "Rozalia",
    "Sasetka",
    "Sonia",
    "Sawka",
    "Saba",
    "Sabi",
    "Sissi",
    "Sali",
    "Sara",
    "Szpulka",
    "Stella",
    "Śnieżynka",
    "Śnieżka",
    "Teri",
    "Tusia",
    "Texa",
    "Taja",
    "Tupcia",
    "Topcia",
    "Tola",
    "Tequilla",
    "Tina",
    "Tinka",
    "Titinka",
    "Tarka",
    "Tosia",
    "Wróżka",
    "Walentynka",
    "Walcia",
    "Wania",
    "Wólka",
    "Wojka",
    "Właźka",
    "Wenka",
    "Wanilia",
    "Wiki",
    "Vena",
    "Vega",
    "Zuzia",
    "Zuza",
    "Zosia",
    "Zelda",
]
MALE = [
    "Anatol",
    "Arsen",
    "Ananas",
    "Albi",
    "Artis",
    "Aksel",
    "Aplauz",
    "Aster",
    "Afro",
    "Agrest",
    "Ares",
    "Amon",
    "Aresik",
    "Atłas",
    "Andy",
    "Arti",
    "Ali",
    "Alfred",
    "Alan",
    "Arnold",
    "Bary",
    "Bambo",
    "Bolek",
    "Baksik",
    "Bakuś",
    "Bubuś",
    "Buu",
    "Bobek",
    "Badi",
    "Beni",
    "Benio",
    "Bos",
    "Bubel",
    "Burczek",
    "Bunny",
    "Bingo",
    "Black",
    "Blue",
    "Brown",
    "Burczuś",
    "Boo",
    "Bob",
    "Boberek",
    "Bodzio",
    "Borys",
    "Czarny",
    "Czarlie",
    "Cymbał",
    "Cear",
    "Cynamon",
    "Czubek",
    "Cekin",
    "Chinsi",
    "Czaruś",
    "Ciapek",
    "Czupurek",
    "Cokół",
    "Cętek",
    "Ciapcio",
    "Cheops",
    "Chmurek",
    "Cheddar",
    "Czester",
    "Cheese",
    "Cytrus",
    "Chrumcio",
    "Cuduś",
    "Czapek",
    "Chrupek",
    "Cheep",
    "Chomek",
    "Cyryl",
    "Chum-Chum",
    "Chomiszczurek",
    "Dyzio",
    "Dozer",
    "Dudi",
    "Dymitr",
    "Dex",
    "Duduś",
    "Dziubek",
    "Domino",
    "Dexter",
    "Dabuś",
    "Dulek",
    "Donald",
    "Dewon",
    "Dołker",
    "Dred",
    "Dudek",
    "Dolar",
    "Dile",
    "Deil",
    "Dropek",
    "Drops",
    "Dżampi",
    "Dżet",
    "Dingo",
    "Dreptak",
    "Drapek",
    "Dodo",
    "Dziobak",
    "Eklerek",
    "Emuś",
    "Elfik",
    "Eukaliptus",
    "Edzio",
    "Emax",
    "Eni",
    "Eddie",
    "Forest",
    "Florek",
    "Frodo",
    "Filek",
    "Felix",
    "Farod",
    "Fiodor",
    "Fazzy",
    "Fluś",
    "Fafik",
    "Fafi",
    "Frosio",
    "Ferdek",
    "Fufel",
    "Fiki",
    "Fax",
    "Felek",
    "Fiszer",
    "Filutek",
    "Faraon",
    "Franek",
    "Gutek",
    "Guzik",
    "Groszek",
    "Gluś",
    "Gamoń",
    "Gumiś",
    "Grubas",
    "Gryzek",
    "Generał",
    "Gustlik",
    "Gambon",
    "Grizzli",
    "Gangster",
    "Gargamel",
    "Gucio",
    "Gumie",
    "Gapcio",
    "Głuptas",
    "Golfy",
    "Goguś",
    "Hamtaro",
    "Hopek",
    "Hantaro",
    "Homek",
    "Hamkuś",
    "Hipcio",
    "Idi",
    "Iki",
    "Irokez",
    "Irys",
    "Igloo",
    "Iksel",
    "Imbir",
    "Izet",
    "Izzy",
    "Imer",
    "Ix",
    "Ingo",
    "Jet",
    "Joe",
    "Junior",
    "Jazi",
    "Józek",
    "Jack",
    "Jakub",
    "Kubuś",
    "Karol",
    "Kajtuś",
    "Kacper",
    "Korek",
    "Kori",
    "Kuki",
    "Kropek",
    "Koki",
    "Kłapouszek",
    "Kieł",
    "Kokos",
    "Kaktus",
    "Kajzer",
    "Kajek",
    "Kopytko",
    "Kumpel",
    "Klops",
    "Keks",
    "Kovu",
    "Kulek",
    "Krecik",
    "Koksik",
    "Kajtek",
    "Lorek",
    "Lotek",
    "Lucky",
    "Lemming",
    "Leo",
    "Lolek",
    "Laser",
    "Lejek",
    "Lux",
    "Lasso",
    "Latex",
    "Lordi",
    "Lucek",
    "Luzak",
    "Łili",
    "Łoli",
    "Łatek",
    "Łaciak",
    "Łak",
    "Łubinek",
    "Łupuś",
    "Łosiek",
    "Miki",
    "Myszor",
    "Master",
    "Misio",
    "Myszorek",
    "Mars",
    "Mailo",
    "Mentos",
    "Miluś",
    "Moni",
    "Mikuś",
    "Mufcio",
    "Miś",
    "Milunio",
    "Miodzik",
    "Majonez",
    "Moryc",
    "Matrix",
    "Mordek",
    "Monty",
    "Merlin",
    "Milton",
    "Modi",
    "Madagaskar",
    "Miłek",
    "Magik",
    "Mokry",
    "Morte",
    "Mały",
    "Morda",
    "Mikołaj",
    "Morsik",
    "Michael",
    "Max",
    "Maurycy",
    "Norek",
    "Neli",
    "Nero",
    "Net",
    "Nosek",
    "Nemo",
    "Neo",
    "Neon",
    "Nutek",
    "Nerw",
    "Nicolas",
    "Orbit",
    "Ogryzek",
    "Opis",
    "Otto",
    "Ozzy",
    "Omar",
    "Opos",
    "Oset",
    "Pank",
    "Pimpuś",
    "Parszywek",
    "Pupil",
    "Piescioch",
    "Puszek",
    "Pixel",
    "Pikuś",
    "Pinki",
    "Papilot",
    "Puchatek",
    "Pionek",
    "Piknik",
    "Pyszczek",
    "Pysio",
    "Pinip",
    "Pucuś",
    "Pepsi",
    "Persil",
    "Rudi",
    "Redi",
    "Roi",
    "Roki",
    "Ron",
    "Rubiś",
    "Red",
    "Rafcio",
    "Rafio",
    "Rafiki",
    "Ramzes",
    "Romeo",
    "Stinki",
    "Sniki",
    "Szczurek",
    "Skin",
    "Skipi",
    "Skiper",
    "Spioszek",
    "Spagetti",
    "Skalar",
    "Smok",
    "Śliniak",
    "Smarkuś",
    "Supeł",
    "Shrek",
    "Śliwka",
    "Stefcio",
    "Szprot",
    "Śmierdziuszek",
    "Snoopy",
    "Stiuart",
    "Smerf",
    "Spider",
    "Sprite",
    "Stan",
    "Śpioch",
    "Tuptuś",
    "Tupcio",
    "Timor",
    "Tuptus",
    "Tobi",
    "Trix",
    "Totek",
    "Taiki",
    "Tonio",
    "Torek",
    "Traf",
    "Tiburek",
    "Tutuś",
    "Topik",
    "Tofik",
    "Thierry",
    "Tadek",
    "Węzeł",
    "Wani",
    "Wanil",
    "Wipi",
    "Wafel",
    "Worek",
    "Wolwo",
    "Wacuś",
    "Velvet",
    "Voy",
    "Znajduś",
    "Zygo",
    "Ziutek",
    "Zyzio",
    "Ząbek",
    "Żwirek",
    "Żelek",
]

ILE_WLASCICIELI = 100
ILE_PRACOWNIKOW = len(CHCEMY_PRACOWNIKOW)
WLASCICIELE_CHOMIKI = []

for i in range(ILE_WLASCICIELI):
    for _ in range(random.randrange(22) + 7):
        WLASCICIELE_CHOMIKI.append(i + 1)

ILE_CHOMIKOW = len(WLASCICIELE_CHOMIKI)
ILE_FIRM = len(NAZWY_FIRM)
ILE_NUMEROW = ILE_WLASCICIELI + ILE_PRACOWNIKOW + ILE_FIRM
ILE_KONTROL = ILE_CHOMIKOW * 4
ILE_KONKURENCJI = len(KATEGORIE) * len(PODLOZA) * len(DLUGOSCI)
ILE_ZAWODOW = 100
CZAS_TRWANIA_ZAWODOW = []
for _ in range(ILE_ZAWODOW):
    CZAS_TRWANIA_ZAWODOW.append(random.randint(1, 3))

JAKIE_KONKURENCJE = []
for i in range(ILE_ZAWODOW):
    ile_na_dzien = random.randint(6, 12)
    wszystkie = random.sample(
        range(1, ILE_KONKURENCJI + 1), CZAS_TRWANIA_ZAWODOW[i] * ile_na_dzien
    )
    temp2 = []
    for j in range(CZAS_TRWANIA_ZAWODOW[i]):
        temp1 = []
        for k in range(ile_na_dzien):
            temp1.append(wszystkie[j * ile_na_dzien + k])
        temp2.append(temp1)
    JAKIE_KONKURENCJE.append(temp2)

POJAZDY = []
ILE_POJAZDOW = 0
nr_pojazdu = 0
for i in range(ILE_CHOMIKOW):
    ile_dla_chomika = random.randint(1, 5)
    ILE_POJAZDOW += ile_dla_chomika
    temp4 = []
    for _ in range(ile_dla_chomika):
        nr_pojazdu += 1
        temp4.append(nr_pojazdu)
    POJAZDY.append(temp4)

NUMERY = random.sample(
    range(100000000, 999999999), ILE_NUMEROW
)  # żeby numery nie mogły się powtórzyć


# funkcje pomocnicze do generacji table
def to_tuples(
    lst,
):  # przemienia [x, y, z] na [(x,), (y,), (z,)], żeby sql nie brał x, y i z za str, tylko tuple
    return [(x,) for x in lst]


def to_date(value):
    if value == None:
        return None
    return datetime.fromtimestamp(value).date()


def to_timestamp(value):
    if value == None:
        return None
    return datetime.fromtimestamp(value)


def bida_rozklad_normalny(a, b):
    return (random.uniform(a, b) + random.uniform(a, b) + random.uniform(a, b)) / 3


def znajdz_koordynatorow(start, end, jobs):
    koordynatorzy = []
    for _, (id_stanowiska, id_pracownika, zatrudnienie, zwolnienie) in enumerate(jobs):
        if (
            id_stanowiska == 1
            and zatrudnienie < start
            and (zwolnienie == None or zwolnienie > end)
        ):
            koordynatorzy.append(id_pracownika)
    return koordynatorzy


def znajdz_sedziow(start, end, jobs):
    sedziowe = []
    for _, (id_stanowiska, id_pracownika, zatrudnienie, zwolnienie) in enumerate(jobs):
        if (
            id_stanowiska == 2
            and zatrudnienie < start
            and (zwolnienie == None or zwolnienie > end)
        ):
            sedziowe.append(id_pracownika)
    return sedziowe


def znajdz_chomiki(start, end, hamsters):
    chomiki = []
    for id_chomika, (_, _, _, _, doloczenie, odejscie) in enumerate(hamsters):
        if doloczenie < start and (odejscie == None or odejscie > end):
            chomiki.append(id_chomika + 1)
    return chomiki


# generacja tabel
# producenci
producenci = to_tuples(PRODUCENCI)

# rasy
rasy = to_tuples(RASY)

# kategorie
kategorie = to_tuples(KATEGORIE)

# podłoża
podloza = to_tuples(PODLOZA)

# przeszkody
przeszkody = to_tuples(PRZESZKODY)

# substancje
substancje = to_tuples(SUBSTANCJE)

# typy źródeł finansowania
typy_zrodel_finansowania = to_tuples(TYPY_ZRODEL_FINANSOWANIA)

# rodzaje kosztow
rodzaje_kosztow = to_tuples(RODZAJE_KOSZTOW)

# stanowiska
stanowiska = [("Koordynator zawodów", 6100), ("Sędzia", 5900), ("Sprzątacz", 4900)]

# sponsorzy
sponsorzy = []
for i in range(ILE_FIRM):
    nazwa_firmy = NAZWY_FIRM[i]
    dane_kontaktowe = NUMERY.pop()
    rozpoczecie_wspolpracy = random.randrange(POCZATEK_DZIALANOSCI, KONIEC_DZIALANOSCI)
    if random.random() < 0.1:  # 10% szans że już nie ma
        zakonczenie_wspolpracy = random.randrange(
            rozpoczecie_wspolpracy, KONIEC_DZIALANOSCI
        )
    else:
        zakonczenie_wspolpracy = None
    sponsorzy.append(
        (
            nazwa_firmy,
            dane_kontaktowe,
            to_date(rozpoczecie_wspolpracy),
            to_date(zakonczenie_wspolpracy),
        )
    )

# wlasciciele
wlasciciele = []
for _ in range(ILE_WLASCICIELI):
    if random.choice([True, False]):
        imie = fake.first_name_male()
        nazwisko = fake.last_name_male()
    else:
        imie = fake.first_name_female()
        nazwisko = fake.last_name_female()
    nr_tel = NUMERY.pop()
    zodiak = random.choice(ZODIAKI)
    wlasciciele.append((imie, nazwisko, nr_tel, zodiak))

# modele
modele = []
for i, nazwa in enumerate(MODELE):
    id_producenta = i // 4 + 1
    nazwa_modelu = nazwa
    cena_modelu = random.randint(10, 100)
    modele.append((id_producenta, nazwa_modelu, cena_modelu))

# pracownicy
pracownicy = []
for _ in CHCEMY_PRACOWNIKOW:
    if random.choice([True, False]):
        imie = fake.first_name_male()
        nazwisko = fake.last_name_male()
    else:
        imie = fake.first_name_female()
        nazwisko = fake.last_name_female()
    nr_tel = NUMERY.pop()
    pracownicy.append((imie, nazwisko, nr_tel))

# zatrudnienie
zatrudnienie = []
for i, j in enumerate(CHCEMY_PRACOWNIKOW):
    id_pracownika = i + 1
    id_stanowiska = j
    data_zatrudnienia = random.randrange(POCZATEK_DZIALANOSCI, KONIEC_DZIALANOSCI)
    if random.random() < 0.1:
        data_zwolnienia = random.randrange(data_zatrudnienia, KONIEC_DZIALANOSCI)
    else:
        data_zwolnienia = None
    zatrudnienie.append(
        (
            id_stanowiska,
            id_pracownika,
            to_date(data_zatrudnienia),
            to_date(data_zwolnienia),
        )
    )

# konkurencje
konkurencje = []
for id_kategorii in range(len(KATEGORIE)):
    for id_podloza in range(len(PODLOZA)):
        for dlugosc_trasy in DLUGOSCI:
            konkurencje.append((id_kategorii + 1, id_podloza + 1, dlugosc_trasy))

# konkurencje_przeszkody
konkurencje_przeszkody = []
for i in range(ILE_KONKURENCJI):
    if (
        konkurencje[i][0] == 1
    ):  # kategoria naturalna, żeby nie dawało przeskód dla pojazdów
        liczba_przeszkod = random.randint(2, 5)
        temp = random.sample(range(1, len(przeszkody) + 1), liczba_przeszkod)
        for j in range(liczba_przeszkod):
            konkurencje_przeszkody.append((i + 1, temp[j]))

# zawody
zawody = []
for i in range(ILE_ZAWODOW):
    data_rozpoczecia = random.randrange(
        int(POCZATEK_DZIALANOSCI + 0.5 * SEKUNDY_W_ROKU),
        KONIEC_DZIALANOSCI - 4 * SEKUNDY_W_DNIU,
    )
    czas_trwania = CZAS_TRWANIA_ZAWODOW[i]
    data_zakonczenia = int(data_rozpoczecia + czas_trwania * SEKUNDY_W_DNIU)
    liczba_widzow = int(
        random.randint(300, 500)
        * ((data_rozpoczecia - POCZATEK_DZIALANOSCI) / SEKUNDY_W_ROKU)
    )
    id_koordynatora = random.choice(
        znajdz_koordynatorow(
            to_date(data_rozpoczecia), to_date(data_zakonczenia), zatrudnienie
        )
    )
    zawody.append(
        (
            to_date(data_rozpoczecia),
            to_date(data_zakonczenia),
            liczba_widzow,
            id_koordynatora,
        )
    )

# rozgrywki
rozgrywki = []
for id_zawodow, (data_rozpoczecia, data_zakonczenia, _, _) in enumerate(zawody):
    for dzien in range(CZAS_TRWANIA_ZAWODOW[id_zawodow]):
        data = data_rozpoczecia + timedelta(days=dzien)
        liczba_rozgrywek = len(JAKIE_KONKURENCJE[id_zawodow][dzien])
        h, m = 12, 0
        for i in range(liczba_rozgrywek):
            data_rozgrywki = datetime.combine(data, time(h, m))
            id_konkurencji = random.randrange(0, len(konkurencje))
            id_sedzi = random.choice(
                znajdz_sedziow(data_rozpoczecia, data_zakonczenia, zatrudnienie)
            )
            rozgrywki.append(
                (
                    id_zawodow + 1,
                    JAKIE_KONKURENCJE[id_zawodow][dzien][i],
                    data_rozgrywki,
                    id_sedzi,
                )
            )
            m += 30
            if m == 60:
                m = 0
                h += 1

# pojazdy
pojazdy = []
for i in range(ILE_POJAZDOW):
    id_modelu = random.randrange(len(modele)) + 1
    pojazdy.append(id_modelu)
pojazdy = to_tuples(pojazdy)

# chomiki
chomiki = []
for i in range(ILE_CHOMIKOW):
    if random.choice([True, False]):
        imie = random.choice(MALE)
    else:
        imie = random.choice(FEMALE)
    id_rasy = random.randrange(len(RASY)) + 1
    data_urodzenia = random.randrange(
        int(POCZATEK_DZIALANOSCI - 0.5 * SEKUNDY_W_ROKU),
        int(KONIEC_DZIALANOSCI - 0.5 * SEKUNDY_W_ROKU),
    )
    dlugosc_zycia = bida_rozklad_normalny(1.5, 3)
    data_dolaczenia = random.randrange(
        max(POCZATEK_DZIALANOSCI, int(data_urodzenia + 0.5 * SEKUNDY_W_ROKU)),
        min(int(data_urodzenia + dlugosc_zycia * SEKUNDY_W_ROKU), KONIEC_DZIALANOSCI),
    )
    if data_urodzenia + dlugosc_zycia * SEKUNDY_W_ROKU < KONIEC_DZIALANOSCI:
        data_odejscia = int(data_urodzenia + dlugosc_zycia * SEKUNDY_W_ROKU)
    else:
        data_odejscia = None
    id_wlasciciela = WLASCICIELE_CHOMIKI[i]
    chomiki.append(
        (
            imie,
            id_wlasciciela,
            id_rasy,
            to_date(data_urodzenia),
            to_date(data_dolaczenia),
            to_date(data_odejscia),
        )
    )

# kontrole_antydopingowe
kontrole_antydopingowe = []
for _ in range(ILE_KONTROL):
    id_chomika = random.randint(1, len(chomiki))
    if chomiki[id_chomika - 1][5] == None:
        end = KONIEC_DZIALANOSCI
    else:
        end = int(datetime.combine(chomiki[id_chomika - 1][5], time.min).timestamp())
    data_kontroli = random.randrange(
        int(datetime.combine(chomiki[id_chomika - 1][4], time.min).timestamp()) - 1, end
    )
    kontrole_antydopingowe.append((id_chomika, to_date(data_kontroli)))

# kontrola_substancji
kontrola_substancji = []
for id_kontroli in range(ILE_KONTROL):
    for id_substancji in range(len(SUBSTANCJE)):
        kontrola_substancji.append(
            (id_kontroli + 1, id_substancji + 1, 0)
        )  # przez ilość kontroli boją się brać doping :)

# koszty_zawodow
koszty_zawodow = []
for id_zawodow, (
    data_rozpoczecia,
    data_zakonczenia,
    liczba_widzow,
    koordynator,
) in enumerate(zawody):
    ile_kosztow = random.randint(5, len(rodzaje_kosztow))
    temp3 = random.sample(range(1, len(rodzaje_kosztow) + 1), ile_kosztow)
    for i in range(ile_kosztow):
        id_typu_kosztu = temp3[i]
        kwota = int(10 ** random.uniform(2, 4))
        koszty_zawodow.append((id_zawodow + 1, id_typu_kosztu, kwota))

# finansowanie
finansowanie = []
for id_zawodow, (
    data_rozpoczecia,
    data_zakonczenia,
    liczba_widzow,
    koordynator,
) in enumerate(zawody):
    liczba_finansowan = random.randint(1, 3)
    jakie_firmy = random.sample(
        list(range(1, len(sponsorzy) + 1)) + [None], liczba_finansowan
    )
    for id_firmy in jakie_firmy:
        if id_firmy == None:
            id_typu_finansowania = 7  # dotacje
        else:
            id_typu_finansowania = random.randint(1, len(typy_zrodel_finansowania))

        data_wplaty = random.randrange(
            int(
                datetime.combine(data_rozpoczecia, time.min).timestamp()
                - random.randrange(30, 60) * SEKUNDY_W_DNIU
            ),
            int(datetime.combine(data_rozpoczecia, time.min).timestamp()),
        )
        kwota = random.randint(10000, 100000)
        finansowanie.append(
            (
                id_zawodow + 1,
                id_typu_finansowania,
                id_firmy,
                to_date(data_wplaty),
                kwota,
            )
        )

# uczestnictwo
uczestnictwo = []
for id_rozgrywki, (id_zawodow, id_konkurencji, _, _) in enumerate(rozgrywki):
    data_start = zawody[id_zawodow - 1][0]
    data_end = zawody[id_zawodow - 1][1]
    ok_chomiki = znajdz_chomiki(data_start, data_end, chomiki)
    jakie_chomiki_bierzemy = random.sample(
        ok_chomiki, int(bida_rozklad_normalny(2, len(ok_chomiki)))
    )
    ile_chomikow_bierzemy = len(jakie_chomiki_bierzemy)
    kategoria = konkurencje[id_konkurencji - 1][0]
    wyniki_chomikow = [
        (
            1.5 * random.random()
            if wlasciciele[chomiki[chomik_id - 1][1] - 1][3] == "Byk"
            else random.random()
        )
        for chomik_id in jakie_chomiki_bierzemy
    ]
    miejsca = [i + 1 for i, _ in sorted(enumerate(wyniki_chomikow), key=lambda k: k[1])]
    for i, (id_chomika) in enumerate(miejsca):
        miejsce = miejsca[i]
        if kategoria == 2:

            id_pojazdu = random.choice(POJAZDY[id_chomika - 1])
        else:
            id_pojazdu = None
        uczestnictwo.append((id_chomika, id_rozgrywki + 1, id_pojazdu, miejsce))

# wazenie
wazenie = []
wazenia = set()
for _, (id_chomika, id_rozgrywki, _, _) in enumerate(uczestnictwo):
    id_zawodow = rozgrywki[id_rozgrywki - 1][0]
    wazenia.add((id_chomika, id_zawodow))
for _, (id_chomika, id_zawodow) in enumerate(wazenia):
    data_rozpoczecia = zawody[id_zawodow - 1][0]
    id_rasy = chomiki[id_chomika - 1][2]
    bazowa_waga = bida_rozklad_normalny(
        PRZEDZIALY_WAG[id_rasy - 1][0], PRZEDZIALY_WAG[id_rasy - 1][1]
    )
    data_wazenia = datetime.combine(data_rozpoczecia, time(10, 0))
    wazenie.append(
        (
            id_chomika,
            id_zawodow,
            bazowa_waga * bida_rozklad_normalny(0.9, 1.1),
            data_wazenia,
        )
    )
# print(wazenie)

# wpisywanie do bazy danych
tables = [
    producenci,
    rasy,
    kategorie,
    podloza,
    przeszkody,
    substancje,
    typy_zrodel_finansowania,
    rodzaje_kosztow,
    stanowiska,
    sponsorzy,
    wlasciciele,
    modele,
    pracownicy,
    zatrudnienie,
    konkurencje,
    konkurencje_przeszkody,
    zawody,
    rozgrywki,
    pojazdy,
    chomiki,
    kontrole_antydopingowe,
    kontrola_substancji,
    koszty_zawodow,
    finansowanie,
    uczestnictwo,
    wazenie,
]
databases = [
    "producenci",
    "rasy",
    "kategorie",
    "podloza",
    "przeszkody",
    "substancje",
    "typy_zrodel_finansowania",
    "rodzaje_kosztow",
    "stanowiska",
    "sponsorzy",
    "wlasciciele",
    "modele",
    "pracownicy",
    "zatrudnienie",
    "konkurencje",
    "konkurencje_przeszkody",
    "zawody",
    "rozgrywki",
    "pojazdy",
    "chomiki",
    "kontrole_antydopingowe",
    "kontrola_substancji",
    "koszty_zawodow",
    "finansowanie",
    "uczestnictwo",
    "wazenie",
]
variables = [
    "(nazwa_producenta)",
    "(nazwa_rasy)",
    "(nazwa_kategorii)",
    "(nazwa_podloza)",
    "(rodzaj_przeszkody)",
    "(nazwa_substancji)",
    "(nazwa_typu)",
    "(nazwa_kosztu)",
    "(nazwa_stanowiska, wyplata)",
    "(nazwa_firmy, dane_kontaktowe, rozpoczecie_wspolpracy, zakonczenie_wspolpracy)",
    "(imie_wlasciciela, nazwisko_wlasciciela, numer_telefonu, zodiak_wlasciciela)",
    "(id_producenta, nazwa_modelu, cena_modelu)",
    "(imie_pracownika, nazwisko_pracownika, numer_telefonu)",
    "(id_stanowiska, id_pracownika, data_zatrudnienia, data_zwolnienia)",
    "(id_kategorii, id_podloza, dlugosc_trasy)",
    "(id_konkurencji, id_przeszkody)",
    "(data_rozpoczecia, data_zakonczenia, liczba_widzow, id_koordynatora)",
    "(id_zawodow, id_konkurencji, data_rozgrywki, id_sedzi)",
    "(id_modelu)",
    "(imie_chomika, id_wlasciciela, id_rasy, data_urodzenia, data_dolaczenia, data_odejscia)",
    "(id_chomika, data_kontroli)",
    "(id_kontroli, id_substancji, wynik_testu)",
    "(id_zawodow, id_typu_kosztu, kwota)",
    "(id_zawodow, id_typu, id_firmy, data_wplaty, kwota)",
    "(id_chomika, id_rozgrywki, id_pojazdu, miejsce)",
    "(id_chomika, id_zawodow, waga, data_wazenia)",
]


def fill(table, database, variable):
    if not table:
        return
    placeholders = ", ".join(["%s"] * len(table[0]))
    sql = f"INSERT INTO {database} {variable} VALUES ({placeholders})"
    print(sql)
    mycursor.executemany(sql, table)


for i in range(len(tables)):
    fill(tables[i], databases[i], variables[i])

con.commit()
mycursor.close()
con.close()
