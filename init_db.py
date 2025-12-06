import sqlite3

connection = sqlite3.connect('databases/database.db')

with open("instance/schema.sql", "r", encoding="utf-8-sig") as f:
    connection.executescript(f.read())

connection.commit()
connection.close()