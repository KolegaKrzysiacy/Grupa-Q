
CREATE TABLE chomiki
(
  id_chomika      SMALLINT    NOT NULL AUTO_INCREMENT,
  imie_chomika    VARCHAR(50) NOT NULL,
  id_wlasciciela  SMALLINT    NOT NULL,
  id_rasy         SMALLINT    NOT NULL,
  data_urodzenia  DATE        NOT NULL,
  data_dolaczenia DATE        NOT NULL,
  data_odejscia   DATE        NULL     COMMENT 'może żyje tylko emerytowany, jak null to dalej biega',
  PRIMARY KEY (id_chomika)
);

CREATE TABLE finansowanie
(
  id_finansowania SMALLINT      NOT NULL AUTO_INCREMENT,
  id_zawodow      SMALLINT      NOT NULL,
  id_typu         SMALLINT      NOT NULL,
  id_firmy        SMALLINT      NULL     COMMENT 'może być null',
  data_wplaty     TIMESTAMP     NOT NULL,
  kwota           DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT 'kwota wpłaty w zł, nieujemna',
  PRIMARY KEY (id_finansowania)
) COMMENT 'źródła finansowania';

CREATE TABLE kategorie
(
  id_kategorii    SMALLINT    NOT NULL AUTO_INCREMENT,
  nazwa_kategorii VARCHAR(20) NOT NULL COMMENT 'naturalna albo formuła Ch',
  PRIMARY KEY (id_kategorii)
);

ALTER TABLE kategorie
  ADD CONSTRAINT UQ_nazwa_kategorii UNIQUE (nazwa_kategorii);

CREATE TABLE konkurencje
(
  id_konkurencji    SMALLINT    NOT NULL AUTO_INCREMENT,
  nazwa_konkurencji VARCHAR(50) NOT NULL,
  id_kategorii      SMALLINT    NOT NULL,
  id_podloza        SMALLINT    NOT NULL,
  id_przeszkody     SMALLINT    NULL     COMMENT 'null=brak',
  dlugosc_trasy     SMALLINT    NULL     COMMENT 'odleglosc wyscigu w m',
  PRIMARY KEY (id_konkurencji)
);

ALTER TABLE konkurencje
  ADD CONSTRAINT UQ_nazwa_konkurencji UNIQUE (nazwa_konkurencji);

CREATE TABLE kontrola_substancji
(
  id_kontroli   SMALLINT NOT NULL,
  id_substancji SMALLINT NOT NULL COMMENT 'sprawdzana substancja',
  wynik_testu   TINYINT  NOT NULL COMMENT '0-negatywny 1-pozytywny',
  PRIMARY KEY (id_kontroli, id_substancji)
);

CREATE TABLE kontrole_antydopingowe
(
  id_kontroli   SMALLINT  NOT NULL AUTO_INCREMENT,
  id_chomika    SMALLINT  NOT NULL,
  id_zawodow    SMALLINT  NOT NULL COMMENT 'na jakich zawodach',
  data_kontroli TIMESTAMP NOT NULL,
  PRIMARY KEY (id_kontroli)
);

CREATE TABLE koszty_zawodow
(
  id_kosztu    SMALLINT      NOT NULL AUTO_INCREMENT,
  id_zawodow   SMALLINT      NOT NULL,
  nazwa_kosztu VARCHAR(80)   NOT NULL COMMENT 'wynajem, nagrody itp',
  kwota        DECIMAL(10,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (id_kosztu)
);

CREATE TABLE modele
(
  id_model    SMALLINT      NOT NULL AUTO_INCREMENT,
  cena_modelu DECIMAL(10,2) NOT NULL COMMENT 'cena w zł, żeby w analize wykorzystać',
  PRIMARY KEY (id_model)
);

CREATE TABLE podloza
(
  id_podloza    SMALLINT    NOT NULL AUTO_INCREMENT,
  nazwa_podloza VARCHAR(30) NOT NULL COMMENT 'rózne podłoża',
  PRIMARY KEY (id_podloza)
);

ALTER TABLE podloza
  ADD CONSTRAINT UQ_nazwa_podloza UNIQUE (nazwa_podloza);

CREATE TABLE pojazdy
(
  id_pojazdu    SMALLINT    NOT NULL AUTO_INCREMENT,
  nazwa_pojazdu VARCHAR(30) NOT NULL COMMENT 'wybrana przez właściciela',
  id_model      SMALLINT    NOT NULL,
  PRIMARY KEY (id_pojazdu)
);

ALTER TABLE pojazdy
  ADD CONSTRAINT UQ_nazwa_pojazdu UNIQUE (nazwa_pojazdu);

CREATE TABLE pracownicy
(
  id_pracownika       SMALLINT     NOT NULL AUTO_INCREMENT,
  imie_pracownika     VARCHAR(100) NOT NULL COMMENT 'pierwsze imie',
  nazwisko_pracownika VARCHAR(50)  NOT NULL,
  id_stanowiska       SMALLINT     NOT NULL,
  data_zatrudnienia   DATE         NOT NULL,
  data_zwolnienia     DATE         NULL    ,
  numer_telefonu      VARCHAR(15)  NULL    ,
  PRIMARY KEY (id_pracownika)
) COMMENT 'pracownicy federacji';

ALTER TABLE pracownicy
  ADD CONSTRAINT UQ_numer_telefonu UNIQUE (numer_telefonu);

CREATE TABLE przeszkody
(
  id_przeszkody     SMALLINT    NOT NULL AUTO_INCREMENT COMMENT '1=rura, 2 itp',
  rodzaj_przeszkody VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_przeszkody)
);

ALTER TABLE przeszkody
  ADD CONSTRAINT UQ_rodzaj_przeszkody UNIQUE (rodzaj_przeszkody);

CREATE TABLE rasy
(
  id_rasy    SMALLINT    NOT NULL AUTO_INCREMENT,
  nazwa_rasy VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_rasy)
);

ALTER TABLE rasy
  ADD CONSTRAINT UQ_nazwa_rasy UNIQUE (nazwa_rasy);

CREATE TABLE rozgrywki
(
  id_rozgrywki   SMALLINT  NOT NULL AUTO_INCREMENT,
  id_zawodow     SMALLINT  NOT NULL,
  id_konkurencji SMALLINT  NOT NULL,
  data_rozgrywki TIMESTAMP NOT NULL,
  id_sedzi       SMALLINT  NOT NULL COMMENT 'id pracownika',
  PRIMARY KEY (id_rozgrywki)
);

CREATE TABLE sponsorzy
(
  id_firmy               SMALLINT     NOT NULL AUTO_INCREMENT,
  nazwa_firmy            VARCHAR(100) NOT NULL,
  oferta                 VARCHAR(255) NULL     COMMENT '"co oferują"',
  dane_kontaktowe        VARCHAR(255) NULL     COMMENT 'do reprezentanta firmy',
  rozpoczecie_wspolpracy TIMESTAMP    NULL    ,
  zakonczenie_wspolpracy TIMESTAMP    NULL    ,
  PRIMARY KEY (id_firmy)
);

ALTER TABLE sponsorzy
  ADD CONSTRAINT UQ_nazwa_firmy UNIQUE (nazwa_firmy);

CREATE TABLE stanowiska
(
  id_stanowiska    SMALLINT      NOT NULL AUTO_INCREMENT,
  nazwa_stanowiska VARCHAR(30)   NOT NULL,
  wyplata          DECIMAL(10,2) NULL     COMMENT 'null = wolontariat?',
  PRIMARY KEY (id_stanowiska)
);

ALTER TABLE stanowiska
  ADD CONSTRAINT UQ_nazwa_stanowiska UNIQUE (nazwa_stanowiska);

CREATE TABLE substancje
(
  id_substancji    SMALLINT     NOT NULL AUTO_INCREMENT,
  nazwa_substancji VARCHAR(100) NOT NULL,
  PRIMARY KEY (id_substancji)
) COMMENT 'niedozwolone substancje';

ALTER TABLE substancje
  ADD CONSTRAINT UQ_nazwa_substancji UNIQUE (nazwa_substancji);

CREATE TABLE typy_zrodel_finansowania
(
  id_typu    SMALLINT    NOT NULL AUTO_INCREMENT,
  nazwa_typu VARCHAR(50) NOT NULL,
  PRIMARY KEY (id_typu)
);

ALTER TABLE typy_zrodel_finansowania
  ADD CONSTRAINT UQ_nazwa_typu UNIQUE (nazwa_typu);

CREATE TABLE uczestnictwo
(
  id_chomika   SMALLINT     NOT NULL,
  id_rozgrywki SMALLINT     NOT NULL,
  czas         DECIMAL(6,2) NULL     COMMENT 'czas biegu nwm',
  miejsce      SMALLINT     NULL     COMMENT 'miejsce w wyścigu',
  id_pojazdu   SMALLINT     NULL     COMMENT 'może null bo nie uczestniczy w wyścigach aut, wtedy kategori musi być naturalna',
  PRIMARY KEY (id_chomika, id_rozgrywki)
) COMMENT 'uczestnictwo w rozgrywkach';

CREATE TABLE wazenie
(
  id_wazenia   SMALLINT      NOT NULL AUTO_INCREMENT,
  id_chomika   SMALLINT      NOT NULL,
  id_zawodow   SMALLINT      NOT NULL,
  waga         DECIMAL(10,2) NOT NULL COMMENT 'waga w gramach',
  data_wazenia TIMESTAMP     NULL    ,
  PRIMARY KEY (id_wazenia)
) COMMENT 'wazenie chomików';

CREATE TABLE wlasciciele
(
  id_wlasciciela       SMALLINT    NOT NULL AUTO_INCREMENT,
  imie_wlasciciela     VARCHAR(30) NOT NULL COMMENT 'pierwsze imie',
  nazwisko_wlasciciela VARCHAR(50) NOT NULL,
  numer_telefonu       VARCHAR(15) NULL    ,
  PRIMARY KEY (id_wlasciciela)
) COMMENT 'wlasciciele chomikow';

ALTER TABLE wlasciciele
  ADD CONSTRAINT UQ_numer_telefonu UNIQUE (numer_telefonu);

CREATE TABLE wyniki_zawodow
(
  id_chomika        SMALLINT NOT NULL,
  id_zawodow        SMALLINT NOT NULL,
  miejsce_generalne SMALLINT NOT NULL,
  PRIMARY KEY (id_chomika, id_zawodow)
);

CREATE TABLE zawody
(
  id_zawodow       SMALLINT NOT NULL AUTO_INCREMENT,
  data_rozpoczecia DATE     NOT NULL,
  data_zakonczenia DATE     NOT NULL,
  liczba_widzow    INT      NOT NULL DEFAULT 0,
  koordynator      SMALLINT NOT NULL COMMENT 'id pracownika',
  PRIMARY KEY (id_zawodow)
);

ALTER TABLE finansowanie
  ADD CONSTRAINT FK_sponsorzy_TO_finansowanie
    FOREIGN KEY (id_firmy)
    REFERENCES sponsorzy (id_firmy);

ALTER TABLE chomiki
  ADD CONSTRAINT FK_wlasciciele_TO_chomiki
    FOREIGN KEY (id_wlasciciela)
    REFERENCES wlasciciele (id_wlasciciela);

ALTER TABLE uczestnictwo
  ADD CONSTRAINT FK_chomiki_TO_uczestnictwo
    FOREIGN KEY (id_chomika)
    REFERENCES chomiki (id_chomika);

ALTER TABLE kontrole_antydopingowe
  ADD CONSTRAINT FK_chomiki_TO_kontrole_antydopingowe
    FOREIGN KEY (id_chomika)
    REFERENCES chomiki (id_chomika);

ALTER TABLE kontrole_antydopingowe
  ADD CONSTRAINT FK_zawody_TO_kontrole_antydopingowe
    FOREIGN KEY (id_zawodow)
    REFERENCES zawody (id_zawodow);

ALTER TABLE rozgrywki
  ADD CONSTRAINT FK_zawody_TO_rozgrywki
    FOREIGN KEY (id_zawodow)
    REFERENCES zawody (id_zawodow);

ALTER TABLE rozgrywki
  ADD CONSTRAINT FK_konkurencje_TO_rozgrywki
    FOREIGN KEY (id_konkurencji)
    REFERENCES konkurencje (id_konkurencji);

ALTER TABLE uczestnictwo
  ADD CONSTRAINT FK_rozgrywki_TO_uczestnictwo
    FOREIGN KEY (id_rozgrywki)
    REFERENCES rozgrywki (id_rozgrywki);

ALTER TABLE zawody
  ADD CONSTRAINT FK_pracownicy_TO_zawody
    FOREIGN KEY (koordynator)
    REFERENCES pracownicy (id_pracownika);

ALTER TABLE rozgrywki
  ADD CONSTRAINT FK_pracownicy_TO_rozgrywki
    FOREIGN KEY (id_sedzi)
    REFERENCES pracownicy (id_pracownika);

ALTER TABLE wazenie
  ADD CONSTRAINT FK_chomiki_TO_wazenie
    FOREIGN KEY (id_chomika)
    REFERENCES chomiki (id_chomika);

ALTER TABLE wazenie
  ADD CONSTRAINT FK_zawody_TO_wazenie
    FOREIGN KEY (id_zawodow)
    REFERENCES zawody (id_zawodow);

ALTER TABLE pracownicy
  ADD CONSTRAINT FK_stanowiska_TO_pracownicy
    FOREIGN KEY (id_stanowiska)
    REFERENCES stanowiska (id_stanowiska);

ALTER TABLE chomiki
  ADD CONSTRAINT FK_rasy_TO_chomiki
    FOREIGN KEY (id_rasy)
    REFERENCES rasy (id_rasy);

ALTER TABLE finansowanie
  ADD CONSTRAINT FK_typy_zrodel_finansowania_TO_finansowanie
    FOREIGN KEY (id_typu)
    REFERENCES typy_zrodel_finansowania (id_typu);

ALTER TABLE konkurencje
  ADD CONSTRAINT FK_kategorie_TO_konkurencje
    FOREIGN KEY (id_kategorii)
    REFERENCES kategorie (id_kategorii);

ALTER TABLE konkurencje
  ADD CONSTRAINT FK_podloza_TO_konkurencje
    FOREIGN KEY (id_podloza)
    REFERENCES podloza (id_podloza);

ALTER TABLE kontrola_substancji
  ADD CONSTRAINT FK_kontrole_antydopingowe_TO_kontrola_substancji
    FOREIGN KEY (id_kontroli)
    REFERENCES kontrole_antydopingowe (id_kontroli);

ALTER TABLE kontrola_substancji
  ADD CONSTRAINT FK_substancje_TO_kontrola_substancji
    FOREIGN KEY (id_substancji)
    REFERENCES substancje (id_substancji);

ALTER TABLE finansowanie
  ADD CONSTRAINT FK_zawody_TO_finansowanie
    FOREIGN KEY (id_zawodow)
    REFERENCES zawody (id_zawodow);

ALTER TABLE pojazdy
  ADD CONSTRAINT FK_modele_TO_pojazdy
    FOREIGN KEY (id_model)
    REFERENCES modele (id_model);

ALTER TABLE konkurencje
  ADD CONSTRAINT FK_przeszkody_TO_konkurencje
    FOREIGN KEY (id_przeszkody)
    REFERENCES przeszkody (id_przeszkody);

ALTER TABLE uczestnictwo
  ADD CONSTRAINT FK_pojazdy_TO_uczestnictwo
    FOREIGN KEY (id_pojazdu)
    REFERENCES pojazdy (id_pojazdu);

ALTER TABLE koszty_zawodow
  ADD CONSTRAINT FK_zawody_TO_koszty_zawodow
    FOREIGN KEY (id_zawodow)
    REFERENCES zawody (id_zawodow);

ALTER TABLE wyniki_zawodow
  ADD CONSTRAINT FK_chomiki_TO_wyniki_zawodow
    FOREIGN KEY (id_chomika)
    REFERENCES chomiki (id_chomika);

ALTER TABLE wyniki_zawodow
  ADD CONSTRAINT FK_zawody_TO_wyniki_zawodow
    FOREIGN KEY (id_zawodow)
    REFERENCES zawody (id_zawodow);
