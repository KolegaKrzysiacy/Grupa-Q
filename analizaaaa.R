
#wczytanie pakietu potrzebnego do połaczenia
library(RMariaDB)

#ustanowienie połaczenia z serwerem zajęciowym
con <- dbConnect(RMariaDB::MariaDB(),
                 dbname = "grupaq",
                 username = "admin",
                 password = "admin",
                 host = "localhost")

#przypisanie zapytania pod query
query <- "SELECT * FROM finansowanie"

#zapisanie uzyskanego wyniku, który jest ramką danych pod zmienną
df <- dbGetQuery(con, query)

#Sprawdzenie pierwszych obserwacji, aby nie wyświetlać całej tabeli
head(df)

#Podsumowanie dotyczące ramki danych
summary(df)

#Zamknięcie połączenia
dbDisconnect(con)

#Komendy działające na zapisanej ramce danych dalej działają
head(df)

#Jednak nie jesteśmy w stanie uzyskać już innego zapytania
# query2 <- "SELECT * FROM zawody"
# df2 <- dbGetQuery(con, query2)

#Należy ponownie otworzyć połączenie
con <- dbConnect(RMariaDB::MariaDB(),
                 dbname = "grupaq",
                 username = "admin",
                 password = "admin",
                 host = "localhost")

#I teraz można wywołać zapytanie
df2 <- dbGetQuery(con, query2)

#Możemy zobaczyć czy dobrze wczytało dane
head(df2)

#Można korzystać z tej ramki, jak ze standardowej ramki danych
df2$kwota

#Można na przykład narysować prosty histogram
hist(df$kwota)

#Do komendy SELECT używamy dbGetQuery, któej argumentami jest połączenie oraz zapytanie
dbGetQuery(con,"SELECT * from chomiki")

#Do komend CREATE oraz INSERT należy używać dbExecute
#Otrzymana wartość, to liczba wierszy, które zostały stworzone
#query3 <- "CREATE OR REPLACE TEMPORARY TABLE temp3 AS (SELECT * FROM actor WHERE first_name = 'PENELOPE')"
#dbExecute(con,query3)

#Pamiętamy na koniec zamknąć połaczenie
dbDisconnect(con)