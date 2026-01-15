import random
import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin",
  database="grupaq"
)

mycursor = con.cursor()

random.seed(42)

DNI_W_ROKU = 365.2425
SEKUNDY_W_DNIU = 86400
SEKUNDY_W_ROKU = DNI_W_ROKU*SEKUNDY_W_DNIU

def bida_rozklad_normalny(a, b): # tak sie serio robi ponoć (https://en.wikipedia.org/wiki/Irwin–Hall_distribution)
    dlugosc = b-a
    xd = (random.random()+random.random()+random.random())/3 # od 0 do 1
    return a + dlugosc*xd

# robimy 100 chomików:
# - imie (na razie "Chomik i")
# - rasa (na razie wszystkie syryjskie)
# - data urodzenia: od 2018 do 2024 (rozkład jednostajny)
# - data zakończenia aktywności: data urodzenia plus od 1.5 do 3 lat (bida rozkład normalny)
chomiki = []
for i in range(100):
    imie = f"Chomik {i}"
    rasa = "syryjski"
    data_urodzenia = random.randrange(1514761200, 1735686000)
    czas_kariery = int(bida_rozklad_normalny(1.5, 3)*SEKUNDY_W_ROKU)
    data_zakonczenia_aktywnosci = data_urodzenia + czas_kariery
    chomiki.append((imie, rasa, data_urodzenia, data_zakonczenia_aktywnosci)) 

# teraz 50 zawodów
# - data rozpoczęcia: od 2021 do 2025
# - data zakończenia: po od 3 do 7 dniach (rozkład jednostajny)
zawody = [] # ! zawody nie będą po kolei + zawody mogą się pokrywać
for _ in range(50):
    data_rozpoczecia = random.randrange(1514761200, 1735686000)
    czas_trwania = random.randint(3, 7)
    data_zakonczenia = data_rozpoczecia + czas_trwania*SEKUNDY_W_DNIU
    zawody.append((data_rozpoczecia, czas_trwania, data_zakonczenia))

# generujemy rozgrywki dla każdych zawodów - od 10 do 50 na dzień (rozkład normalny):
# - id_zawodów - indeks w liście po prostu
# - data rozgrywki - po kolei dni
rozgrywki = []
for id_zawodow, (data_rozpoczecia, czas_trwania, data_zakonczenia) in enumerate(zawody):
    for dzien in range(czas_trwania):
        liczba_rozgrywek = round(bida_rozklad_normalny(10, 50))
        data_rozgrywki = data_rozpoczecia + dzien*SEKUNDY_W_DNIU
        rozgrywki += liczba_rozgrywek * [(id_zawodow, data_rozgrywki)]

# uczestnictwo w chomikach - dla każdej rozgrywki w każdych zawodach
# jak chomik jest w tabeli to uczestniczył a jak nie jest to nie uczestniczył
# - id_rozgrywki
# - id_chomika
# - wynik - jak na razie nie mamy typów rozgrywek ani nic więc liczby od 0 do 1
uczestnictwo = []
for id_rozgrywki, (id_zawodow, data_rozgrywki) in enumerate(rozgrywki):
    # niech na razie około ćwierć możliwych chomików niech biegnie, potem trzeba to lepiej zrobić
    # chcemy mieć przynajmniej 2 chomiki w wyścigu bo jeden chomik sam ze sobą się nie będzie ścigał
    # najpierw musimy wiedziec jakie chomiki mogą biegnąć
    ok_chomiki = [i for i, (_, _, data_urodzenia, data_zakonczenia_aktywnosci) in enumerate(chomiki)
        if data_zakonczenia <= data_zakonczenia_aktywnosci
        and data_rozpoczecia >= data_urodzenia + 0.5*SEKUNDY_W_ROKU # nie zmuszajmy małych chomików do biegania !!!
    ]
    ile_mamy_chomikow = len(ok_chomiki)
    # UWAGA: mogą się powtarzać normalnie więc może się trafić kilka razy ten sam. celujmy w co najmniej 3 na zapas
    ile_bierzemy_chomikow = max(3, round(bida_rozklad_normalny(ile_mamy_chomikow*0.125, ile_mamy_chomikow*0.375)))
    jakie_chomiki_bierzemy = set(random.choices(ok_chomiki, k=ile_bierzemy_chomikow))
    assert(ile_bierzemy_chomikow >= 2) # jak sie wywali to coś trzeba zmienić, albo po prostu pech (wtedy też trzeba coś zmienić)
    for id_chomika in jakie_chomiki_bierzemy:
        wynik = random.random()
        uczestnictwo.append((id_rozgrywki, id_chomika, wynik))


# na razie nie ma:
# - właścicieli chomików
# - pracowników
# - testów antydopingowych
# - ważenia
# - typów rozgrywek (konkurencje)
# - ras chomików
# - sponsorów i finansowania

#for i in rozgrywki: # chomiki / zawody / rozgrywki / uczestnictwo, można testować sobie
#    print(i)






#to zostaw na razie
"""
tables = [chomiki, zawody, rozgrywki, uczestnictwo]
databases = ["chomiki", "zawody", "rozgrywki", "uczestnictwo"]
variables = ["(imie, rasa, data_urodzenia, data_zakonczenia_aktywnosci)", "(data_rozpoczecia, czas_trwania, data_zakonczenia)", "(id_rozgrywki, data_rozgrywki)", "(id_rozgrywki, id_chomika, wynik)"]
lenghts = [5, 4, 4, 3]
def fill(table, database, variable, lenght):
    sql = "INSERT INTO " + database + " " + variable + " VALUES (%s" + ", %s" * (lenght - 1) + ")"
    mycursor.executemany(sql, table)

for i in range(len(tables)):
    fill(tables[i], databases[i], variables[i], lenghts[i])


"""


mycursor.close()
con.close()