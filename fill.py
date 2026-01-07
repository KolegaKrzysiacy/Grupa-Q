import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin",
  database="grupaq"
)

mycursor = con.cursor()


print("tu generowanie")



mycursor.fetchall()
mycursor.close()
con.close()


