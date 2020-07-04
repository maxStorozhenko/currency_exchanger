import sqlite3


conn = sqlite3.connect('work_ua.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE vacancy
             (date text, name text, salary text, city text, description text)''')
