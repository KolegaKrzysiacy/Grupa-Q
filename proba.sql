SELECT kategorie.id_kategorii,
       kategorie.nazwa_kategorii AS nazwa_kategorii,
       chomiki.id_chomika,
       chomiki.imie_chomika AS nazwa_chomika,
       count(chomiki.id_chomika) as liczba_zwycięstw
FROM kategorie 
JOIN konkurencje  ON kategorie.id_kategorii = konkurencje.id_kategorii
JOIN rozgrywki  ON konkurencje.id_konkurencji = rozgrywki.id_konkurencji
JOIN uczestnictwo  ON rozgrywki.id_rozgrywki = uczestnictwo.id_rozgrywki
JOIN chomiki  ON uczestnictwo.id_chomika = chomiki.id_chomika
where uczestnictwo.miejsce = 1
GROUP BY kategorie.id_kategorii, kategorie.nazwa_kategorii, chomiki.id_chomika, chomiki.imie_chomika
ORDER BY count(chomiki.id_chomika) desc
limit 2;


# szczyt kariery

select chomiki.id_chomika, rozgrywki.data_rozgrywki, uczestnictwo.miejsce

from rozgrywki
left join uczestnictwo 
on rozgrywki.id_rozgrywki = uczestnictwo.id_rozgrywki
left join chomiki
on uczestnictwo.id_chomika = chomiki.id_chomika
where uczestnictwo.miejsce in (1,2,3,4,5,6)
GROUP by chomiki.id_chomika, rozgrywki.data_rozgrywki

SELECT chomiki.id_chomika,
    TIMESTAMPDIFF(MONTH, MIN(rozgrywki.data_rozgrywki), MAX(rozgrywki.data_rozgrywki)) AS roznica_miesiecy
FROM rozgrywki
JOIN uczestnictwo 
      ON rozgrywki.id_rozgrywki = uczestnictwo.id_rozgrywki
JOIN chomiki
      ON uczestnictwo.id_chomika = chomiki.id_chomika
WHERE uczestnictwo.miejsce IN (1,2,3,4,5,6)
GROUP by chomiki.id_chomika
ORDER BY chomiki.id_chomika;

select avg(srednia_roznica_miesiecy)
from (
SELECT 
    TIMESTAMPDIFF(MONTH, MIN(rozgrywki.data_rozgrywki), MAX(rozgrywki.data_rozgrywki)) AS srednia_roznica_miesiecy
FROM rozgrywki
JOIN uczestnictwo 
      ON rozgrywki.id_rozgrywki = uczestnictwo.id_rozgrywki
JOIN chomiki
      ON uczestnictwo.id_chomika = chomiki.id_chomika
WHERE uczestnictwo.miejsce IN (1,2,3,4,5,6)
GROUP by chomiki.id_chomika);


SELECT 
    round(MEdian(roznica_miesiecy), 1) AS srednia_roznica_miesiecy
FROM (
    SELECT 
        TIMESTAMPDIFF(MONTH, MIN(rozgrywki.data_rozgrywki), MAX(rozgrywki.data_rozgrywki)) AS roznica_miesiecy
    FROM rozgrywki
    JOIN uczestnictwo 
          ON rozgrywki.id_rozgrywki = uczestnictwo.id_rozgrywki
    WHERE uczestnictwo.miejsce IN (1,2,3,4,5,6)
    GROUP BY uczestnictwo.id_chomika
) t;


select year(zawody.data_rozpoczecia) as rok,  COUNT(DISTINCT uczestnictwo.id_chomika) AS liczba_uczestnikow
from zawody
LEFT JOIN rozgrywki
on zawody.id_zawodow = rozgrywki.id_zawodow
left JOIN uczestnictwo 
      ON rozgrywki.id_rozgrywki = uczestnictwo.id_rozgrywki
left JOIN chomiki
      ON uczestnictwo.id_chomika = chomiki.id_chomika
GROUP BY YEAR(zawody.data_rozpoczecia)
ORDER BY rok;

SELECT 
    zawody.id_zawodow,
    zawody.data_rozpoczecia,
    COUNT(DISTINCT uczestnictwo.id_chomika) AS liczba_uczestnikow
FROM zawody
LEFT JOIN rozgrywki
      ON zawody.id_zawodow = rozgrywki.id_zawodow
LEFT JOIN uczestnictwo 
      ON rozgrywki.id_rozgrywki = uczestnictwo.id_rozgrywki
LEFT JOIN chomiki
      ON uczestnictwo.id_chomika = chomiki.id_chomika
GROUP BY zawody.id_zawodow, zawody.data_rozpoczecia
ORDER BY zawody.data_rozpoczecia;



select koszty_zawodow.id_zawodow, sum(koszty_zawodow.kwota) as wydane,
        sum(finansowanie.kwota) as dostane, sum(finansowanie.kwota) - sum(koszty_zawodow.kwota) as przychod,
            ROUND(
      (SUM(finansowanie.kwota) - SUM(koszty_zawodow.kwota)) 
      / SUM(koszty_zawodow.kwota) * 100
    , 2) AS rentownosc_procent
from koszty_zawodow
LEFT JOIN finansowanie
on koszty_zawodow.id_zawodow = finansowanie.id_zawodow
GROUP BY koszty_zawodow.id_zawodow

select avg(rentownosc_procent) from(
select koszty_zawodow.id_zawodow, sum(koszty_zawodow.kwota) as wydane,
        sum(finansowanie.kwota) as dostane, sum(finansowanie.kwota) - sum(koszty_zawodow.kwota) as przychod,
            ROUND(
      (SUM(finansowanie.kwota) - SUM(koszty_zawodow.kwota)) 
      / SUM(koszty_zawodow.kwota) * 100
    , 2) AS rentownosc_procent
from koszty_zawodow
LEFT JOIN finansowanie
on koszty_zawodow.id_zawodow = finansowanie.id_zawodow
GROUP BY koszty_zawodow.id_zawodow
) t;

select year(zawody.data_rozpoczecia), sum(finansowanie.kwota) - sum(koszty_zawodow.kwota) as przychod 
from zawody
left join koszty_zawodow
on zawody.id_zawodow = koszty_zawodow.id_zawodow
LEFT JOIN finansowanie
on koszty_zawodow.id_zawodow = finansowanie.id_zawodow
GROUP BY  year(zawody.data_rozpoczecia)
ORDER BY year(zawody.data_rozpoczecia);



SELECT ROUND(AVG(TIMESTAMPDIFF(MONTH, data_dolaczenia, data_odejscia)), 0) AS sredni_wiek_miesiace
FROM chomiki;


SELECT 
    konkurencje.id_konkurencji,
    sum(zawody.liczba_widzow) AS liczba_uczestnikow
FROM zawody
LEFT JOIN rozgrywki
      ON zawody.id_zawodow = rozgrywki.id_zawodow
left join konkurencje
on rozgrywki.id_konkurencji = konkurencje.id_konkurencji
GROUP by konkurencje.id_konkurencji
ORDER BY sum(zawody.liczba_widzow) DESC;

select 
    kategorie.id_kategorii,
    kategorie.nazwa_kategorii,
    COUNT(DISTINCT sponsorzy.id_firmy) AS liczba_sponsorow
from sponsorzy
left join finansowanie
on sponsorzy.id_firmy = finansowanie.id_firmy
left join zawody
on finansowanie.id_zawodow = zawody.id_zawodow
LEFT JOIN rozgrywki
      ON zawody.id_zawodow = rozgrywki.id_zawodow
left join konkurencje
on rozgrywki.id_konkurencji = konkurencje.id_konkurencji
left join kategorie
on konkurencje.id_kategorii = kategorie.id_kategorii
GROUP by kategorie.id_kategorii

SELECT 
    konkurencje.id_konkurencji,
    COUNT(DISTINCT sponsorzy.id_firmy) AS liczba_sponsorow
from sponsorzy
left join finansowanie
on sponsorzy.id_firmy = finansowanie.id_firmy
left join zawody
on finansowanie.id_zawodow = zawody.id_zawodow
LEFT JOIN rozgrywki
      ON zawody.id_zawodow = rozgrywki.id_zawodow
left join konkurencje
on rozgrywki.id_konkurencji = konkurencje.id_konkurencji
GROUP by konkurencje.id_konkurencji
ORDER BY sum(zawody.liczba_widzow) DESC;


select wlasciciele.zodiak_wlasciciela, avg(uczestnictwo.miejsce)
from uczestnictwo
left join chomiki
on uczestnictwo.id_chomika = chomiki.id_chomika
left join wlasciciele
on chomiki.id_wlasciciela = wlasciciele.id_wlasciciela
GROUP by wlasciciele.zodiak_wlasciciela

select wlasciciele.zodiak_wlasciciela, uczestnictwo.miejsce
from uczestnictwo
left join chomiki
on uczestnictwo.id_chomika = chomiki.id_chomika
left join wlasciciele
on chomiki.id_wlasciciela = wlasciciele.id_wlasciciela
order by wlasciciele.zodiak_wlasciciela

select producenci.nazwa_producenta, uczestnictwo.miejsce
from uczestnictwo
left join pojazdy 
on uczestnictwo.id_pojazdu = pojazdy.id_pojazdu
left join modele
on pojazdy.id_modelu = modele.id_model
left join producenci
on modele.id_producenta = producenci.id_producenta
WHERE producenci.nazwa_producenta IS NOT NULL
order by producenci.nazwa_producenta;

select kontrola_substancji.wynik_testu
from chomiki
left join kontrole_antydopingowe
on chomiki.id_chomika = kontrole_antydopingowe.id_chomika
left join kontrola_substancji
on kontrole_antydopingowe.id_kontroli = kontrola_substancji.id_kontroli
where wynik_testu = "1"
order by wynik_testu


select substancje.nazwa_substancji, avg(uczestnictwo.miejsce)
from uczestnictwo
left join chomiki
on uczestnictwo.id_chomika = chomiki.id_chomika
left join kontrole_antydopingowe
on chomiki.id_chomika = kontrole_antydopingowe.id_chomika
left join kontrola_substancji
on kontrole_antydopingowe.id_kontroli = kontrola_substancji.id_kontroli
left join substancje
on kontrola_substancji.id_substancji = substancje.id_substancji
GROUP by substancje.id_substancji

select rasy.nazwa_rasy, uczestnictwo.miejsce
from uczestnictwo
left join chomiki
on uczestnictwo.id_chomika = chomiki.id_chomika
left join rasy 
on chomiki.id_rasy = chomiki.id_rasy
order by rasy.id_rasy