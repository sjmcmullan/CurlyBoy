import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE reminders(
                reminder_ID INTEGER PRIMARY KEY,
                time_started TEXT,
                time_end TEXT,
                creator TEXT,
                channel TEXT,
                public INTEGER,
                description TEXT            
                );''')
# c.execute('''INSERT INTO reminders(time_started, time_end, creator, public, description) VALUES (?,?,?,?,?)''')
conn.commit()
conn.close()
