import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin",
  database="grupaq"
)

mycursor = con.cursor()


print("na razie nic to nie robi, tu będzie generowanie danych")


mycursor.close()
con.close()


