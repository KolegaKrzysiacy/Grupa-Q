import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin",
  database="grupaq"
)

mycursor = con.cursor()

#Unique tutaj bo nie da się dać unique na dwóch kolumnach na raz w erd editor, można tylko np. UNIQUE (id_zawodow) i UNIQUE (id_konkurencji), a nie UNIQUE (id_zawodow, id_konkurencji)

mycursor.execute("ALTER TABLE rozgrywki ADD CONSTRAINT UQ_rozgrywki_zawody_konkurencja UNIQUE (id_zawodow, id_konkurencji);")     #żeby było tylko po jednej takiej samej konkurencji na jednych zawodach
mycursor.execute("ALTER TABLE wazenie ADD CONSTRAINT UQ_wazenie_chomik_zawody UNIQUE (id_chomika, id_zawodow);")                  #żeby było tylko jendo ważenie w jednych zawodach


mycursor.close()
con.close()


