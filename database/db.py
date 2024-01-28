import sqlite3

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

query = 'CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, text TEXT)'
cursor.execute(query)
