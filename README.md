1. Pobierz MySQL z 
https://www.mysql.com/downloads/ 
jest na samym dole strony
MySQL Community (GPL) Downloads

2. Stwórz lokalną bazę danych
Zależnie jakie login dacie przy ustawianiu SQL, będziecie musieli zmienić go w kodzie, polecam dać tak jak ja dałem - user="admin", password="admin", żeby każdemu kod działał

3. W gitbash:
pip install mysql-connector-python

4. Połącz się do bazy danych w VS 

5.1. Jak był zmieniany schemat bazy danych to eksportuj z projekt.vuerd.json z opcją Schema SQL (bo pewnie będzie się zmieniał) i nazwij go schemat.sql

5.2. Uruchomić w VS po kolei
create.py
schemat.sql
fill.py


fill.py jest do wypełnienia żeby generował dane ale na razie nic nie robi



6.1 Jak stworzycie serwer SQL to on będzie działał cały czas w tle, bo deafult jest żeby włączał się automatycznie po startup, można to zmienić albo go wyłączyć i włączyć w Services/Usługi, trzeba tylko znaleźć jego nazwę, mój miał deafult MySQL80










