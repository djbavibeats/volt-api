import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    passwd="Aoc!8314",
)

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE onboarding")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)