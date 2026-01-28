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
    round(AVG(roznica_miesiecy), 1) AS srednia_roznica_miesiecy
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
