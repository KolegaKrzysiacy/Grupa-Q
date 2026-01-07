import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin"
)

mycursor = con.cursor()

mycursor.execute("DROP DATABASE IF EXISTS grupaq")

mycursor.fetchall()
mycursor.close()
con.close()