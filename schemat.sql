
CREATE TABLE chomiki
(
  id_chomika                  SMALLINT    NOT NULL AUTO_INCREMENT,
  imie                        VARCHAR(50) NULL    ,
  id_wlasciciela              SMALLINT    NULL     COMMENT 'może być null - wolny chomik',
  data_urodzenia              DATE        NULL    ,
  rasa                        VARCHAR(50) NULL     COMMENT 'kilka możliwych wartości',
  data_zakonczenia_aktywnosci DATE        NULL     COMMENT 'może żyje tylko emerytowany, jak null to dalej biega',
  PRIMARY KEY (id_chomika)
);

CREATE TABLE finansowanie
(
  id_wplaty    SMALLINT     NOT NULL AUTO_INCREMENT,
  typ_zrodla   VARCHAR(50)  NULL     COMMENT 'kilka możliwych wartości',
  nazwa_zrodla VARCHAR(100) NULL    ,
  id_firmy     SMALLINT     NULL     COMMENT 'może być null',
  kwota        FLOAT        NOT NULL DEFAULT 0 COMMENT 'kwota wpłaty w zł',
  data_wplaty  TIMESTAMP    NULL    ,
  PRIMARY KEY (id_wplaty)
) COMMENT 'źródła finansowania';

CREATE TABLE konkurencje
(
  id_konkurencji    SMALLINT    NOT NULL AUTO_INCREMENT,
  nazwa_konkurencji VARCHAR(50) NULL    ,
  kategoria         VARCHAR(15) NOT NULL COMMENT 'naturalna albo formuła Ch',
  odleglosc         SMALLINT    NULL     COMMENT 'odleglosc wyscigu w m',
  podloze           VARCHAR(50) NULL     COMMENT 'kilka możliwych wartości',
  przeszkody        TINYINT     NULL     COMMENT '0 albo 1',
  PRIMARY KEY (id_konkurencji)
);

CREATE TABLE kontrole_antydopingowe
(
  id_kontroli   SMALLINT  NOT NULL AUTO_INCREMENT,
  id_substancji SMALLINT  NOT NULL COMMENT 'sprawdzana substancja',
  id_chomika    SMALLINT  NOT NULL,
  id_zawodow    SMALLINT  NOT NULL COMMENT 'na jakich zawodach',
  wynik_testu   TINYINT   NULL     COMMENT '0-negatywny 1-pozytywny',
  data_kontroli TIMESTAMP NULL    ,
  PRIMARY KEY (id_kontroli)
);

CREATE TABLE pracownicy
(
  id_pracownika       SMALLINT     NOT NULL AUTO_INCREMENT,
  pelne_imie          VARCHAR(100) NULL     COMMENT 'wszystkie imiona i nazwiska',
  krotkie_imie        VARCHAR(50)  NULL     COMMENT 'pierwsze imie',
  stanowisko          VARCHAR(100) NULL     COMMENT 'nazwa stanowiska, kilka możliwych wartości',
  wyplata             DECIMAL      NULL     DEFAULT 0 COMMENT 'wypłata brutto w zł',
  data_zatrudnienia   DATE         NULL    ,
  obecnie_zatrudniony TINYINT      NOT NULL DEFAULT 0 COMMENT '0 albo 1',
  PRIMARY KEY (id_pracownika)
) COMMENT 'pracownicy federacji';

CREATE TABLE rozgrywki
(
  id_rozgrywki   SMALLINT  NOT NULL AUTO_INCREMENT,
  id_zawodow     SMALLINT  NOT NULL,
  id_konkurencji SMALLINT  NOT NULL,
  data_rozgrywki TIMESTAMP NULL    ,
  sedzia         SMALLINT  NOT NULL COMMENT 'id pracownika',
  PRIMARY KEY (id_rozgrywki)
);

CREATE TABLE sponsorzy
(
  id_firmy               SMALLINT     NOT NULL AUTO_INCREMENT,
  nazwa_firmy            VARCHAR(100) NULL    ,
  oferta                 VARCHAR(255) NULL     COMMENT '"co oferują"',
  dane_kontaktowe        VARCHAR(255) NULL     COMMENT 'do reprezentanta firmy',
  rozpoczecie_wspolpracy TIMESTAMP    NULL    ,
  zakonczenie_wspolpracy TIMESTAMP    NULL    ,
  PRIMARY KEY (id_firmy)
);

CREATE TABLE substancje
(
  id_substancji    SMALLINT     NOT NULL AUTO_INCREMENT,
  nazwa_substancji VARCHAR(100) NULL    ,
  czy_zakazana     SMALLINT     NULL     DEFAULT 0 COMMENT '0 albo 1',
  PRIMARY KEY (id_substancji)
) COMMENT 'niedozwolone substancje';

CREATE TABLE uczestnictwo
(
  id_uczestnictwa SMALLINT NOT NULL AUTO_INCREMENT,
  id_chomika      SMALLINT NOT NULL,
  id_rozgrywki    SMALLINT NOT NULL,
  wynik           DECIMAL  NULL     COMMENT 'czas biegu nwm',
  PRIMARY KEY (id_uczestnictwa)
) COMMENT 'uczestnictwo w rozgrywkach';

CREATE TABLE wazenie
(
  id_wazenia   SMALLINT  NOT NULL AUTO_INCREMENT,
  id_chomika   SMALLINT  NOT NULL,
  id_zawodow   SMALLINT  NOT NULL,
  waga         DECIMAL   NOT NULL COMMENT 'waga w gramach',
  data_wazenia TIMESTAMP NULL    ,
  PRIMARY KEY (id_wazenia)
) COMMENT 'wazenie chomików';

CREATE TABLE wlasciciele
(
  id_wlasciciela SMALLINT     NOT NULL AUTO_INCREMENT,
  pelne_imie     VARCHAR(100) NULL     COMMENT 'wszystkie imiona i nazwiska',
  krotkie_imie   VARCHAR(50)  NULL     COMMENT 'pierwsze imie',
  PRIMARY KEY (id_wlasciciela)
) COMMENT 'wlasciciele chomikow';

CREATE TABLE zawody
(
  id_zawodow       SMALLINT  NOT NULL AUTO_INCREMENT,
  data_rozpoczecia TIMESTAMP NULL    ,
  data_zakonczenia TIMESTAMP NULL    ,
  glowny_sponsor   SMALLINT  NULL     COMMENT 'id firmy',
  koordynator      SMALLINT  NULL     COMMENT 'id pracownika',
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
  ADD CONSTRAINT FK_substancje_TO_kontrole_antydopingowe
    FOREIGN KEY (id_substancji)
    REFERENCES substancje (id_substancji);

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
  ADD CONSTRAINT FK_sponsorzy_TO_zawody
    FOREIGN KEY (glowny_sponsor)
    REFERENCES sponsorzy (id_firmy);

ALTER TABLE zawody
  ADD CONSTRAINT FK_pracownicy_TO_zawody
    FOREIGN KEY (koordynator)
    REFERENCES pracownicy (id_pracownika);

ALTER TABLE rozgrywki
  ADD CONSTRAINT FK_pracownicy_TO_rozgrywki
    FOREIGN KEY (sedzia)
    REFERENCES pracownicy (id_pracownika);

ALTER TABLE wazenie
  ADD CONSTRAINT FK_chomiki_TO_wazenie
    FOREIGN KEY (id_chomika)
    REFERENCES chomiki (id_chomika);

ALTER TABLE wazenie
  ADD CONSTRAINT FK_zawody_TO_wazenie
    FOREIGN KEY (id_zawodow)
    REFERENCES zawody (id_zawodow);
